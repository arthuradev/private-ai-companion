from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.safety.models import (
    ActionDecisionStatus,
    ActionIntent,
    ActionPolicyDecision,
    RiskClassification,
    RiskLevel,
)


@dataclass(frozen=True, slots=True)
class ActionPolicy:
    allowed_action_types: tuple[str, ...]
    require_confirmation_for: tuple[RiskLevel, ...] = (
        RiskLevel.MEDIUM,
        RiskLevel.HIGH,
    )
    allow_high_risk: bool = False
    allow_critical_risk: bool = False

    def evaluate(
        self,
        intent: ActionIntent,
        classification: RiskClassification,
    ) -> ActionPolicyDecision:
        if classification.risk is RiskLevel.CRITICAL and not self.allow_critical_risk:
            return self._deny(
                intent,
                classification,
                "critical_actions_prohibited",
            )

        if classification.risk is RiskLevel.HIGH and not self.allow_high_risk:
            return self._deny(intent, classification, "high_risk_actions_disabled")

        if intent.action_type not in self.allowed_action_types:
            return self._deny(intent, classification, "action_type_not_allowed")

        if (
            classification.risk in self.require_confirmation_for
            and not intent.user_confirmed
        ):
            return ActionPolicyDecision(
                action_id=intent.action_id,
                action_type=intent.action_type,
                risk=classification.risk,
                status=ActionDecisionStatus.REQUIRES_CONFIRMATION,
                reason="user_confirmation_required",
                requires_confirmation=True,
            )

        return ActionPolicyDecision(
            action_id=intent.action_id,
            action_type=intent.action_type,
            risk=classification.risk,
            status=ActionDecisionStatus.ALLOWED,
            reason="allowed",
            requires_confirmation=classification.risk in self.require_confirmation_for,
        )

    @staticmethod
    def _deny(
        intent: ActionIntent,
        classification: RiskClassification,
        reason: str,
    ) -> ActionPolicyDecision:
        return ActionPolicyDecision(
            action_id=intent.action_id,
            action_type=intent.action_type,
            risk=classification.risk,
            status=ActionDecisionStatus.DENIED,
            reason=reason,
            requires_confirmation=False,
        )
