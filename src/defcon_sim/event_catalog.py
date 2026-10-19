from .models import WorldState
from .event_engine import EventDefinition, EventOutcome

def build_event_catalog() -> tuple[EventDefinition, ...]:
	return (
		# 1. Intelligence uncertainty
		EventDefinition(
			event_id="conflicting_reports",
			title="Conflicting Intelligence Reports",
			description=("Two fictional sources provide contradictory accounts of a developing regional incident."),
			condition=lambda w: w.intelligence_confidence < 85,
			weight=lambda w: max(1, (100 - w.intelligence_confidence) // 10),
			cooldown_minutes=45,
			max_occurrences=3,
			outcomes=(
				EventOutcome(
					outcome_id="reports_conflict",
					description=("The conflicting reports remain unsolved."),
					changes={
						"intelligence_confidence": -7,
						"global_tension": 4,
						"active_incidents": 1
					},
					weight=lambda w: 3
				),
				EventOutcome(
					outcome_id="independent_verification",
					description=("Independent verification resolves part of the discrepancy."),
					changes={
						"intelligence_confidence": 5,
						"global_tension": -2
					},
					weight=lambda w: 2
				)
			)
		),

		# 2. Diplomatic backchannel
		EventDefinition(
			event_id="emergency_backchannel",
			title="Emergency Diplomatic Backchannel",
			description=("Officials establish a private communication channel \
			             to clarify intentions and reduce uncertainty."),
			condition=lambda w: (w.global_tension >= 25 and w.diplomatic_stability >=15),
			weight=lambda w: max(1, w.global_tension // 15),
			cooldown_minutes=60,
			max_occurrences=3,
			outcomes=(
				EventOutcome(
					outcome_id="talks_progress",
					description=("The parties agree to continue direct talks."),
					changes={
						"global_tension": -8,
						"diplomatic_stability": 5,
						"intelligence_confidence": 2
					},
					weight=lambda w: max(1, w.diplomatic_stability //15)
				),
				EventOutcome(
					outcome_id="talks_stall",
					description=("The partices exchange demands but make no meaningful progress"),
					changes={
						"global_tension": 4,
						"diplomatic_stability": -4
					},
					weight=lambda w: max(1, (100 - w.diplomatic_stability) // 15)
				)
			)
		),

		# 3. Infrastructure disruption
		EventDefinition(
			event_id="infrastructure_disruption",
			title="Regional Infrastructure Disruption",
			description=("A fictional region experiences a disruption affecting \
			             essential civilian services."),
			condition=lambda w: (w.global_tension >= 40 or w.infrastructure_integrity < 80),
			weight=lambda w: max(1, w.global_tension // 20 + (100 - w.infrastructure_integrity) // 25),
			cooldown_minutes=60,
			max_occurrences=2,
			outcomes=(
				EventOutcome(
					outcome_id="major_disruption",
					description=("Service interruptions delay emergency and civilian operations"),
					changes={
						"infrastructure_integrity": -5,
						"civilian_welfare": -4
					},
					weight=lambda w: 2
				),
				EventOutcome(
					outcome_id="limited_disruption",
					description=("The disruption is contained before widespread effects develop"),
					changes={
						"infrastructure_integrity": -2,
						"civilian_welfare": -1
					},
					weight=lambda w: 3
				),
			)
		),
		# 4. Humanitarian Response
		EventDefinition(
			event_id="humanitarian_emergency",
			title="Humanitarian Emergency",
			description=("Civilian needs increases, promptin pressure for coordinated \
			             relief operations."),
			condition=lambda w: w.civilian_welfare < 90,
			weight=lambda w: max(1, (100 - w.civilian_welfare) // 10),
			cooldown_minutes=45,
			max_occurrences=3,
			outcomes=(
				EventOutcome(
					outcome_id="relief_coordination",
					description=("Regional authorities coordinate relief and restor \
					             access to essential services."),
					changes={
						"civilian_welfare": 4,
						"diplomatic_stability": 2
					},
					weight=lambda w: 3
				),
				EventOutcome(
					outcome_id="relief_delayed",
					description=("Access and coordination problems delay assistance to affected civilians."),
					changes={
						"civilian_welfare": -4,
						"diplomatic_stability": -2
					},
					weight=lambda w: 2
				),
			)
		),
		# 5. Diplomatic De-escalation
		EventDefinition(
			event_id="deescilation_initiative",
			title="De-escelation Initiative",
			description=("A third-party mediator proposes measures to reduce the immediate \
			             risk of confrontation"),
			condition=lambda w: (w.global_tension >= 35 and w.diplomatic_stability >= 25),
			weight=lambda w: max(1, w.diplomatic_stability // 20),
			cooldown_minutes=60,
			max_occurrences=2,
			outcomes=(
				EventOutcome(
					outcome_id="initiative_accepted",
					description=("The parties agree to a limited confidence-building measure"),
					changes={
						"global_tension": -10,
						"diplomatic_stability": 6
					},
					weight=lambda w: max(1, w.diplomatic_stability // 20)
				),
				EventOutcome(
					outcome_id="initiative_rejected",
					description=("The proposal is rejected, increasing doubts about \
					             diplomatic progress"),
					changes={
						"global_tension": 5,
						"diplomatic_stability": -5
					},
					weight=lambda w: max(1, (100 - w.diplomatic_stability) // 20)
				),
			)
		)
	)
