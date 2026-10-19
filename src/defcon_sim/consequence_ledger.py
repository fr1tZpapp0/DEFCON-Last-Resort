import hashlib, json, sqlite3

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENESIS_HASH = "0" * 64


class ConsequenceLedger:
	# THIS IS APPEND-ONLY, HASH-CHAINED SIMULATION EVENT HISTORY

	def __init__(self, database_path: str | Path):
		self.database_path = str(database_path)		

		with self._connect() as connection:
			connection.execute("""
				CREATE TABLE IF NOT EXISTS ledger_entries (
					sequence INTEGER PRIMARY KEY AUTOINCREMENT,
					recorded_at TEXT NOT NULL,
					simulation_time_minutes INTEGER NOT NULL,
					event_type TEXT NOT NULL,
					description TEXT NOT NULL,
					payload_json TEXT NOT NULL,
					previous_hash TEXT NOT NULL,
					entry_hash TEXT NOT NULL UNIQUE
				)
			""")


	def _connect(self):
		connection = sqlite3.connect(self.database_path)
		connection.row_factory = sqlite3.Row
		return connection

	@staticmethod
	def _canonical_json(value: Any) -> str:
		return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


	@staticmethod
	def _calculate_hash(sequence: int, recorded_at: str, simulation_time_minutes: int, 
	                    event_type: str, description: str, payload_json: str, previous_hash: str) -> str:

		content = ConsequenceLedger._canonical_json({
			"sequence": sequence,
			"recored_at": recorded_at,
			"simulation_time_minutes": simulation_time_minutes,
			"event_type": event_type,
			"description": description,
			"payload_json": payload_json,
			"previous_hash": previous_hash
			})

		return hashlib.sha256(content.encode("utf-8")).hexdigest()


	def record(self, simulation_time_minutes: int, 
	           event_type: str, description: str, payload: dict[str, Any] | None = None) -> int:
		# Record an event and return the sequence number

		if simulation_time_minutes < 0: raise ValueError("Simulation time cannot be negative")


		payload_json = self._canonical_json(payload or {})
		recorded_at = datetime.now(timezone.utc).isoformat()

		with self._connect() as connection:
			previous = connection.execute("""
			SELECT sequence, entry_hash
				FROM ledger_entries
				ORDER BY sequence DESC
				LIMIT 1
            """).fetchone()

			previous_hash = (previous["entry_hash"] if previous else GENESIS_HASH)
			sequence = (previous["sequence"] + 1 if previous else 1)
			entry_hash = (self._calculate_hash(sequence, recorded_at, simulation_time_minutes, event_type, 
												description, payload_json, previous_hash))

			connection.execute("""
				INSERT INTO ledger_entries (
						sequence, recorded_at, simulation_time_minutes,
						event_type, description, payload_json,
						previous_hash, entry_hash
					) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sequence, recorded_at, simulation_time_minutes, event_type, 
					description, payload_json, previous_hash, entry_hash))

		return sequence


	def entries(self) -> list[dict[str, Any]]:
		# Return all ledger entries in order
		with self._connect() as connection:
			rows = connection.execute("""
				SELECT * FROM ledger_entries ORDER BY sequence		
			""").fetchall()

		result = []
		for row in rows:
			entry = dict(row)
			entry["payload"] = json.loads(entry.pop("payload_json"))
			result.append(entry)


		return result


	def verify(self) -> bool:
		# Check entry hashes and links between consecutive entries
		previous_hash = GENESIS_HASH
		expected_sequence = 1

		for entry in self.entries():
			payload_json = self._canonical_json(entry["payload"])

			if entry["sequence"] != expected_sequence: return False
			if entry["previous_hash"] != previous_hash: return False

			expected_hash = self._calculate_hash(entry["sequence"], entry["recorded_at"], 
			    entry["simulation_time_minutes"], entry["event_type"], entry["description"], payload_json, previous_hash)

			if entry["entry_hash"] != expected_hash: return False

			previous_hash = entry["entry_hash"]
			expected_sequence += 1

		return True

	