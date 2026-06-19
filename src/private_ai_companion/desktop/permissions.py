from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.desktop.models import DesktopActionType
from private_ai_companion.safety import ActionIntent


@dataclass(frozen=True, slots=True)
class DesktopPermissionDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True, slots=True)
class DesktopPermissionPolicy:
    allowed_action_types: tuple[str, ...]
    allowed_app_ids: tuple[str, ...] = ()
    notes_enabled: bool = True
    active_window_title_enabled: bool = True

    def evaluate(self, intent: ActionIntent) -> DesktopPermissionDecision:
        if intent.action_type not in self.allowed_action_types:
            return self._deny("desktop_action_not_allowed")

        evaluators = {
            DesktopActionType.READ_ACTIVE_WINDOW_TITLE.value: (
                self._evaluate_active_window_title
            ),
            DesktopActionType.CREATE_NOTE.value: self._evaluate_create_note,
            DesktopActionType.OPEN_ALLOWED_APP.value: self._evaluate_open_allowed_app,
        }
        evaluator = evaluators.get(intent.action_type)
        if evaluator is None:
            return self._deny("unknown_desktop_action")
        return evaluator(intent)

    def _evaluate_active_window_title(
        self,
        intent: ActionIntent,
    ) -> DesktopPermissionDecision:
        _ = intent
        if not self.active_window_title_enabled:
            return self._deny("active_window_title_disabled")
        return self._allow()

    def _evaluate_create_note(
        self,
        intent: ActionIntent,
    ) -> DesktopPermissionDecision:
        if not self.notes_enabled:
            return self._deny("local_notes_disabled")
        if not intent.parameters.get("title", "").strip():
            return self._deny("note_title_required")
        return self._allow()

    def _evaluate_open_allowed_app(
        self,
        intent: ActionIntent,
    ) -> DesktopPermissionDecision:
        app_id = intent.parameters.get("app_id", "").strip()
        if not app_id:
            return self._deny("app_id_required")
        if app_id not in self.allowed_app_ids:
            return self._deny("app_not_allowlisted")
        return self._allow()

    @staticmethod
    def _allow() -> DesktopPermissionDecision:
        return DesktopPermissionDecision(allowed=True, reason="allowed")

    @staticmethod
    def _deny(reason: str) -> DesktopPermissionDecision:
        return DesktopPermissionDecision(allowed=False, reason=reason)
