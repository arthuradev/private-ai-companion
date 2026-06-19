from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.safety.models import (
    ActionIntent,
    RiskClassification,
    RiskLevel,
)

DEFAULT_ACTION_RISK_BY_TYPE = {
    "avatar.set_expression": RiskLevel.LOW,
    "speech.speak_response": RiskLevel.LOW,
    "ui.open_panel": RiskLevel.LOW,
    "desktop.open_allowed_app": RiskLevel.MEDIUM,
    "desktop.create_note": RiskLevel.MEDIUM,
    "desktop.read_active_window_title": RiskLevel.MEDIUM,
    "vision.capture_manual_screenshot": RiskLevel.MEDIUM,
    "desktop.open_url": RiskLevel.HIGH,
    "desktop.read_file": RiskLevel.HIGH,
    "desktop.clipboard_read": RiskLevel.HIGH,
    "desktop.clipboard_write": RiskLevel.HIGH,
    "system.delete_file": RiskLevel.CRITICAL,
    "system.install_program": RiskLevel.CRITICAL,
    "system.run_shell": RiskLevel.CRITICAL,
    "system.change_settings": RiskLevel.CRITICAL,
    "secrets.read": RiskLevel.CRITICAL,
    "desktop.freeform_mouse_keyboard": RiskLevel.CRITICAL,
}


@dataclass(frozen=True, slots=True)
class RiskClassifier:
    action_risk_by_type: dict[str, RiskLevel] | None = None

    def classify(self, intent: ActionIntent) -> RiskClassification:
        risk_by_type = self.action_risk_by_type or DEFAULT_ACTION_RISK_BY_TYPE
        risk = risk_by_type.get(intent.action_type, RiskLevel.CRITICAL)
        reason = (
            "configured_action_risk"
            if intent.action_type in risk_by_type
            else "unknown_action_type"
        )
        return RiskClassification(
            action_id=intent.action_id,
            action_type=intent.action_type,
            risk=risk,
            reason=reason,
        )
