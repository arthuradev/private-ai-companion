from __future__ import annotations

from private_ai_companion.safety import (
    ActionDecisionStatus,
    ActionIntent,
    ActionPolicy,
    RiskClassifier,
    RiskLevel,
)


def test_risk_classifier_marks_desktop_note_as_medium() -> None:
    intent = ActionIntent(action_type="desktop.create_note")

    classification = RiskClassifier().classify(intent)

    assert classification.risk is RiskLevel.MEDIUM
    assert classification.reason == "configured_action_risk"


def test_risk_classifier_marks_unknown_action_as_critical() -> None:
    intent = ActionIntent(action_type="desktop.unknown")

    classification = RiskClassifier().classify(intent)

    assert classification.risk is RiskLevel.CRITICAL
    assert classification.reason == "unknown_action_type"


def test_action_policy_requires_confirmation_for_medium_risk() -> None:
    intent = ActionIntent(action_type="desktop.create_note")
    classification = RiskClassifier().classify(intent)
    policy = ActionPolicy(allowed_action_types=("desktop.create_note",))

    decision = policy.evaluate(intent, classification)

    assert decision.status is ActionDecisionStatus.REQUIRES_CONFIRMATION
    assert decision.requires_confirmation is True


def test_action_policy_allows_confirmed_medium_risk() -> None:
    intent = ActionIntent(action_type="desktop.create_note", user_confirmed=True)
    classification = RiskClassifier().classify(intent)
    policy = ActionPolicy(allowed_action_types=("desktop.create_note",))

    decision = policy.evaluate(intent, classification)

    assert decision.status is ActionDecisionStatus.ALLOWED
    assert decision.allowed is True


def test_action_policy_denies_critical_actions() -> None:
    intent = ActionIntent(
        action_type="system.run_shell",
        parameters={"command": "echo unsafe"},
        user_confirmed=True,
    )
    classification = RiskClassifier().classify(intent)
    policy = ActionPolicy(allowed_action_types=("system.run_shell",))

    decision = policy.evaluate(intent, classification)

    assert decision.status is ActionDecisionStatus.DENIED
    assert decision.reason == "critical_actions_prohibited"
