from dataclasses import dataclass
from .models import DEFCONLevel, WorldState


@dataclass(frozen=True)
class DEFCONAssessment:
	level: DEFCONLevel
	crisis_score: int
	reasons: tuple[str, ...]


def assess_DEFCON_level(world: WorldState) -> DEFCONAssessment:
	# Calculate DEFCON Level based on internal ranges
	# 0-19: DEFCON 5
	# 20-39: DEFCON 4
	# 40-59: DEFCON 3
	# 60-79: DEFCON 2
	# 80-100: DEFCON 1

	world.validate()

	diplomatic_instability = 100 - world.diplomatic_stability
	intelligence_uncertainty = 100 - world.intelligence_confidence

	# ! Score isn't really a score, nobody wins
	# Each component contributes to a score between 0 and 100
	assessed_score = round(world.global_tension * 0.45 
	        + diplomatic_instability * 0.25
			+ intelligence_uncertainty * 0.20
			+ min(world.active_incidents, 5) * 2)

	assessed_score = max(0, min(100, assessed_score))
	if assessed_score >=  80: level = DEFCONLevel.DEFCON_1
	elif assessed_score >= 60: level = DEFCONLevel.DEFCON_2
	elif assessed_score >= 40: level = DEFCONLevel.DEFCON_3
	elif assessed_score >= 20: level = DEFCONLevel.DEFCON_4
	else: level = DEFCONLevel.DEFCON_5

	reasons = []

	if world.global_tension >= 60: reasons.append("Global tensions are elevated.")
	if world.diplomatic_stability <= 40: reasons.append("Diplomatic stability is critically weak.")
	if world.intelligence_confidence <= 40: reasons.append("Intelligence confidence is low.")
	if world.active_incidents >= 3: reasons.append("Multiple incidents remain unsolved")
	if not reasons: reasons.append("No individual crisis indicator has crossed its warning threshold")


	return DEFCONAssessment(level=level, crisis_score=assessed_score, reasons=tuple(reasons))
