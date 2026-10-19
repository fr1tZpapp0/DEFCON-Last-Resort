from dataclasses import dataclass, field
from enum import IntEnum

class DEFCONLevel(IntEnum):	# The actual DEFCON levels, the lower the number, the worse
	DEFCON_1 = 1
	DEFCON_2 = 2
	DEFCON_3 = 3
	DEFCON_4 = 4
	DEFCON_5 = 5


@dataclass
class Faction:	# The fictional faction / nation / geopolitical actor
	faction_id: str
	name: str
	diplomatic_trust: int = 50
	stability: int = 75
	military_readiness: int = 25


@dataclass
class WorldState:
	scenario_id: str
	simulation_time_minutes: int = 0
	global_tension: int = 20
	diplomatic_stability: int = 80
	intelligence_confidence: int = 75
	infrastructure_integrity: int = 100
	civilian_welfare: int = 95

	active_incidents: int = 0


	factions: dict[str, Faction] = field(default_factory=dict)




	def validate(self) -> None:	# Reject invalid world-state values BEFORE being committed
		bounded_fields = ("global_tension", "diplomatic_stability", "intelligence_confidence", 
			"infrastructure_integrity", "civilian_welfare")

		for field_name in bounded_fields:
			value = getattr(self, field_name)
			if not 0 <= value <= 100: raise ValueError(f"{field_name} must be between 0 and 100")


		if self.simulation_time_minutes < 0: raise ValueError("Simulation time cannot be negative")
		if self.active_incidents < 0: raise ValueError("Active incidents cannot be negative")

		for faction in self.factions.values():
			for field_name in ("diplomatic_trust", "stability", "military_readiness"):
				value = getattr(faction, field_name)
				if not 0 <= value <=100: raise ValueError(f"{faction.name}: {field_name} must be between 0 and 100")

