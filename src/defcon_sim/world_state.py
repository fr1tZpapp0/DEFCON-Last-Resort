from .models import WorldState
from .consequence_ledger import ConsequenceLedger
from .defcon_assessment import assess_DEFCON_level

ALLOWED_CHANGES = {
	"global_tension",
	"diplomatic_stability",
	"intelligence_confidence",
	"infrastructure_integrity",
	"civilian_welfare",
	"active_incidents"
}

def apply_world_changes(world: WorldState, ledger: ConsequenceLedger, 
            event_type: str, description: str, changes: dict[str, int], advance_minutes: int = 0) -> None:
	# Apply a group of state changes
	#! IF VALIDATION FAILS: RESTORE ORIGINAL VALUES
	#* A SUCCESSFUL UPDATE IS RECORDED TO CONSEQUENCE LEDGER


	if advance_minutes < 0: raise ValueError("Cannot move simulation time backwards")

	unknown_fields = set(changes) - ALLOWED_CHANGES
	if unknown_fields: raise ValueError(f"Unsupported world-state fields: {sorted(unknown_fields)}")
	if any(type(value) is not int for value in changes.values()): raise TypeError("All state changes must be ints")

	before_assessment = assess_DEFCON_level(world)
	previous_values = {name: getattr(world, name) for name in changes}

	try:
		for name, delta in changes.items(): setattr(world, name, getattr(world, name) + delta)

		world.simulation_time_minutes += advance_minutes
		world.validate()

	except Exception:
		for name, value in previous_values.items(): setattr(world, name, value)
		world.simulation_time_minutes = previous_values
		raise

	after_assessment = assess_DEFCON_level(world)
	recorded_changes = {name: {"before": previous_values[name], "after": getattr(world, name)} for name in changes}

	ledger.record(
		simulation_time_minutes=world.simulation_time_minutes,
		event_type=event_type,
		description=description,
		payload={
			"changes": recorded_changes,
			"time_advanced_minutes": advance_minutes,
			"defcon_before": before_assessment.level.name,
			"defcon_after": after_assessment.level.name,
			"crisis_score_before": before_assessment.crisis_score,
			"crisis_score_after": after_assessment.crisis_score
		}
	)





