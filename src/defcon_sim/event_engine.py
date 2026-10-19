from dataclasses import dataclass
from typing import Callable
from random import Random

from .models import WorldState
from .consequence_ledger import ConsequenceLedger
from. world_state import apply_world_changes

Condition = Callable[[WorldState], bool]
Weight = Callable[[WorldState], int]

@dataclass(frozen=True)
class EventOutcome:
	outcome_id: str
	description: str
	changes: dict[str, int]
	weight: Weight = lambda world: 1



@dataclass(frozen=True)
class EventDefinition:
	event_id: str
	title: str
	description: str
	condition: Condition
	weight: Weight
	outcomes: tuple[EventOutcome, ...]
	cooldown_minutes: int = 30
	max_occurrences: int = 3



@dataclass(frozen=True)
class EventResult:
	event_id: str
	title: str
	outcome_id: str
	description: str
	changes: dict[str, int]
	simulation_time_minutes: int


class AutonomousEventEngine:
	# Select and Resolve events via Current World State

	TURN_MINUTES = 15


	def __init__(self, events: tuple[EventDefinition, ...], ledger: ConsequenceLedger, seed: int | None = None):
		self.events = events
		self.ledger = ledger
		self.rng = Random(seed)


	def _event_history(self, event_id: str) -> list[dict]:
		return [
			entry for entry in self.ledger.entries()
			if entry["payload"].get("metadata", {}).get("event_id") == event_id
		]

	def _eligible(self, world: WorldState) -> list[EventDefinition]:
		eligble = []
		for event in self.events:
			history = self._event_history(event.event_id)

			if len(history) >= event.max_occurrences: continue
			if history:
				last_time = history[-1]["simulation_time_minutes"]
				if (world.simulation_time_minutes - last_time < event.cooldown_minutes): continue

			if not event.condition(world): continue
			if event.weight(world) <= 0: continue
			if not any(outcome.weight(world) > 0 for outcome in event.outcomes): continue

			eligble.append(event)

		return eligble

	def _weighted_choice(self, items, weight_function):
		weights = [max(0, weight_function(item)) for item in items]
		total = sum(weights)

		if total <= 0: raise ValueError("Weighted choice requires a positive weight.")

		return self.rng.choices(items, weights=weights, k=1)[0]


	def advance_turn(self, world: WorldState) -> EventResult | None:
		# Advance by 1 turn
		# Returns the resolved event, or none if no major event occurs
		
		world.validate()
		eligible = self._eligible(world)

		if not eligible:
			apply_world_changes(world=world, ledger=self.ledger, event_type="quiet_period",
				description="No major incident occurred this turn.", changes={}, 
				advance_minutes=self.TURN_MINUTES, metadata={"event_kind": "quiet_period"})
			return None

		event = self._weighted_choice(eligible, lambda item: item.weight(world))
		outcome = self._weighted_choice([outcome for outcome in event.outcomes if outcome.weight(world) > 0],
					lambda item: item.weight(world))

		apply_world_changes(
			world=world,
			ledger=self.ledger,
			event_type="world_event",
			description=f"{event.title}: {outcome.description}",
			changes=outcome.changes,
			advance_minutes=self.TURN_MINUTES,
			metadata={
				"event_id": event.event_id,
				"event_title": event.title,
				"outcome_id": outcome.outcome_id,
				"event_description": event.description
			}
		)

		return EventResult(
			event_id=event.event_id,
			title=event.title,
			outcome_id=outcome.outcome_id,
			description=outcome.description,
			changes=dict(outcome.changes),
			simulation_time_minutes=world.simulation_time_minutes
		)




