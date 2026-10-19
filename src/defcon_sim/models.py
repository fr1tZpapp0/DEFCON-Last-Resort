from dataclasses import dataclass, field
from enum import IntEnum

class DEFCONLevel(IntEnum):	# The actual DEFCON levels, the lower the number, the worse
	DEFCON_1 = 1
	DEFCON_2 = 2
	DEFCON_3 = 3
	DEFCON_4 = 4
	DEFCON_5 = 5


@dataclass
class Nation:	# The fictional nation / geopolitical actor
	faction_id: str
	name: str
	diplomatic_level: int = 50
	stability: int = 75
	military_readiness: int = 25


@dataclass
class WorldState:
	scenario_id: str