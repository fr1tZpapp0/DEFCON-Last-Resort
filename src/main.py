from pathlib import Path
from defcon_sim.consequence_ledger import ConsequenceLedger
from defcon_sim.defcon_assessment import assess_DEFCON_level
from defcon_sim.scenario import create_initial_world
from defcon_sim.world_state import apply_world_changes

def display_status(world, ledger):
	assessment = assess_DEFCON_level(world)
	print("\n" + "=" * 52)
	print("         DEFCON: LAST RESORT")
	print("=" * 52)
	print(f"Scenario: {world.scenario_id}")
	print(f"Simulation time: {world.simulation_time_minutes} minutes")
	print(f"Global tension: {world.global_tension}/100")
	print(f"Diplomatic stability: {world.diplomatic_stability}/100")
	print(f"Intelligence confidence: {world.intelligence_confidence}/100")
	print(f"Active incidents: {world.active_incidents}")
	print(f"Crisis score: {assessment.crisis_score}/100")
	print(f"Alert level: {assessment.level.name}")

	print("\nAssessment reasons:")
	for reason in assessment.reasons: print(f" - {reason}")

	print(f"\nLedger integrity: {'VALID' if ledger.verify() else 'INVALID'}")
	print(f"Ledger entries: {len(ledger.entries())}")
	print("=" * 52)


def main():
	project_root = Path(__file__).resolve().parent.parent
	save_dir = project_root / "data" / "saves"
	save_dir.mkdir(parents=True, exist_ok=True)


	world = create_initial_world()
	ledger_path = save_dir / "milestone1_demo.sqlite3"
	if ledger_path.exists(): ledger_path.unlink()


	ledger = ConsequenceLedger(ledger_path)
	ledger.record(simulation_time_minutes=world.simulation_time_minutes, event_type="scenario_started", 
	              description="The IRON VEIL scenario has begun.", payload={
					  "scenario_id": world.scenario_id,
					  "initial_global_tension": world.global_tension
					})

	display_status(world, ledger)
	print("\nA new incident has occurred.")
	print("Emergency negotiations have failed.")

	apply_world_changes(world=world, ledger=ledger, event_type="diplomatic_breakdown", 
	                    description="Emergency negotiations failed.", changes={
							"global_tension": 18,
							"diplomatic_stability": -12,
							"intelligence_confidence": -8,
							"active_incidents": 1
						}, advance_minutes=30)

	display_status(world, ledger)
	print("\nMost recent ledger entry:")
	print(ledger.entries()[-1])


if __name__ == "__main__":
	main()
