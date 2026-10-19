from pathlib import Path

from defcon_sim.consequence_ledger import ConsequenceLedger
from defcon_sim.defcon_assessment import assess_DEFCON_level
from defcon_sim.scenario import create_initial_world
from defcon_sim.world_state import apply_world_changes
from defcon_sim.event_catalog import build_event_catalog
from defcon_sim.event_engine import AutonomousEventEngine

from random import randint



def main():
	TEST_RANDOM_SEED = randint(1, 357159)
	TEST_SEED = 42

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

	engine = AutonomousEventEngine(events=build_event_catalog(), ledger=ledger, seed=TEST_RANDOM_SEED)
	for turn in range(1, 20):
		result = engine.advance_turn(world)
		assessment = assess_DEFCON_level(world)

		print(f"\n--- TURN: {turn} ---")
		print(f"Time: {world.simulation_time_minutes} minutes")
		print(f"DEFCON LEVEL: {assessment.level.name}")
		print(f"CRISIS SCORE: {assessment.crisis_score}/100")

		if result is None: print("No major incident")
		else:
			print(f"EVENT: {result.title}")
			print(result.description)
			print(f"Outcome: {result.outcome_id}")
			print(f"Changes: {result.changes}")

	print("\n--- FINAL STATE ---")
	print(f"SEED: {TEST_RANDOM_SEED}")
	print(f"DEFCON Level: {assessment.level.name}")
	print(f"Crisis Score: {assessment.crisis_score}/100")
	print("\n")
	print(f"Global Tension: {world.global_tension}")
	print(f"Diplomatic Stability: {world.diplomatic_stability}")
	print(f"Intelligence Confidence: {world.intelligence_confidence}")
	print(f"Infrastructure Integrity: {world.infrastructure_integrity}")
	print(f"Civilian Welfare: {world.civilian_welfare}")

	print(f"Ledger entries: {len(ledger.entries())}")
	print(f"Ledger valid: {ledger.verify()}")



if __name__ == "__main__":
	main()
