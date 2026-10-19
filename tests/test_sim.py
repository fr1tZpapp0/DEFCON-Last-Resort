import tempfile, unittest
from pathlib import Path

from src.defcon_sim.models import WorldState
from src.defcon_sim.defcon_assessment import assess_DEFCON_level
from src.defcon_sim.consequence_ledger import ConsequenceLedger
from src.defcon_sim.scenario import create_initial_world
from src.defcon_sim.world_state import apply_world_changes


class SimulationTests(unittest.TestCase):
	def setUp(self):
		self.temp_dir = tempfile.TemporaryDirectory()
		database = Path(self.temp_dir.name) / "test.sqlite3"

		self.world = create_initial_world()
		self.ledger = ConsequenceLedger(database)

	def tearDown(self):
		self.temp_dir.cleanup()

	def test_initial_world_is_valid(self):
		self.world.validate()
		assessment = assess_DEFCON_level(self.world)

		self.assertGreaterEqual(assessment.crisis_score, 0)
		self.assertLessEqual(assessment.crisis_score, 100)

	def test_changes_are_recorded(self):
		original_tension = self.world.global_tension

		apply_world_changes(self.world, self.ledger, "test_event", "a test event occurred", {"global_tension": 10}, advance_minutes=5)

		self.assertEqual(self.world.global_tension, original_tension + 10)
		self.assertEqual(len(self.ledger.entries()), 1)
		self.assertTrue(self.ledger.verify())

	def test_invalid_change_rolls_back(self):
		original_tension = self.world.global_tension

		with self.assertRaises(ValueError):
			apply_world_changes(self.world, self.ledger, "invalid_event", "this event should fail", {"global_tension": 500})

		self.assertEqual(self.world.global_tension, original_tension)
		self.assertEqual(len(self.ledger.entries()), 0)

	def test_ledger_detects_modified_entries(self):
		self.ledger.record(0, "test_event", "Original event", {"value": 10})

		with self.ledger._connect() as connection:
			connection.execute("""
				UPDATE ledger_entries
				SET description = ?
				WHERE sequence = 1
			""", ("Modified event.",))

		self.assertFalse(self.ledger.verify())


if __name__ == "__main__":
	unittest.main()
