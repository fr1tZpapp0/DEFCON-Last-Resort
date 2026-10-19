from .models import Faction, WorldState


def create_initial_world() -> WorldState:
	return WorldState(
		scenario_id="IRON_VEIL",
		simulation_time_minutes=0,

		global_tension=25,
		diplomatic_stability=75,
		intelligence_confidence=70,
		infrastructure_integrity=95,
		civilian_welfare=95,
		active_incidents=0,

		factions={
			"valedorn": Faction(
				faction_id="valedorn",
				name="Republic of the Democratic Valedorn",
				diplomatic_trust=60,
				stability=80,
				military_readiness=30
			),
			"orska": Faction(
				faction_id="orska",
				name="Orskan Federation",
				diplomatic_trust=45,
				stability=70,
				military_readiness=44
			),
			"morthalia": Faction(
				faction_id="morthalia",
				name="Compact of Morthalia Protectorates",
				diplomatic_trust=55,
				stability=75,
				military_readiness=20
			)
		}
	)