from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from private_ai_companion.desktop import (
    DesktopActionDryRun,
    DesktopActionExecutionResult,
    DesktopActionType,
)
from private_ai_companion.safety import (
    ActionExecutionStatus,
    ActionIntent,
    RiskLevel,
)


@dataclass(frozen=True, slots=True)
class SafeLocalDesktopExecutor:
    notes_directory: Path
    allowed_apps: dict[str, str]
    executor_id: str = "safe-local-desktop"
    fake_active_window_title: str = "Private AI Companion"
    max_note_bytes: int = 4096

    async def dry_run(
        self,
        intent: ActionIntent,
        risk: RiskLevel,
    ) -> DesktopActionDryRun:
        if intent.action_type == DesktopActionType.READ_ACTIVE_WINDOW_TITLE:
            return DesktopActionDryRun(
                action_id=intent.action_id,
                action_type=intent.action_type,
                risk=risk,
                summary="Read the active window title through the safe desktop port",
                side_effects=(),
            )

        if intent.action_type == DesktopActionType.CREATE_NOTE:
            title = intent.parameters.get("title", "").strip()
            return DesktopActionDryRun(
                action_id=intent.action_id,
                action_type=intent.action_type,
                risk=risk,
                summary=f"Create one local note titled {title!r}",
                side_effects=("create_file_in_notes_directory",),
            )

        if intent.action_type == DesktopActionType.OPEN_ALLOWED_APP:
            app_id = intent.parameters.get("app_id", "").strip()
            display_name = self.allowed_apps.get(app_id, app_id)
            return DesktopActionDryRun(
                action_id=intent.action_id,
                action_type=intent.action_type,
                risk=risk,
                summary=f"Open allowed app {display_name!r} using a safe adapter",
                side_effects=("simulated_app_launch",),
            )

        return DesktopActionDryRun(
            action_id=intent.action_id,
            action_type=intent.action_type,
            risk=risk,
            summary="Unknown desktop action would be blocked",
            side_effects=(),
            safe_to_execute=False,
        )

    async def execute(
        self,
        intent: ActionIntent,
        risk: RiskLevel,
    ) -> DesktopActionExecutionResult:
        _ = risk
        if intent.action_type == DesktopActionType.READ_ACTIVE_WINDOW_TITLE:
            return DesktopActionExecutionResult(
                action_id=intent.action_id,
                action_type=intent.action_type,
                status=ActionExecutionStatus.EXECUTED,
                message="active_window_title_read",
                output={"title": self.fake_active_window_title},
            )

        if intent.action_type == DesktopActionType.CREATE_NOTE:
            return self._create_note(intent)

        if intent.action_type == DesktopActionType.OPEN_ALLOWED_APP:
            app_id = intent.parameters.get("app_id", "").strip()
            display_name = self.allowed_apps.get(app_id, app_id)
            return DesktopActionExecutionResult(
                action_id=intent.action_id,
                action_type=intent.action_type,
                status=ActionExecutionStatus.EXECUTED,
                message="allowed_app_launch_simulated",
                output={"app_id": app_id, "display_name": display_name},
            )

        return DesktopActionExecutionResult(
            action_id=intent.action_id,
            action_type=intent.action_type,
            status=ActionExecutionStatus.DENIED,
            message="unknown_desktop_action",
        )

    def _create_note(self, intent: ActionIntent) -> DesktopActionExecutionResult:
        title = intent.parameters.get("title", "").strip()
        body = intent.parameters.get("body", "")
        if len(body.encode("utf-8")) > self.max_note_bytes:
            return DesktopActionExecutionResult(
                action_id=intent.action_id,
                action_type=intent.action_type,
                status=ActionExecutionStatus.FAILED,
                message="note_body_too_large",
            )

        notes_root = self.notes_directory.resolve()
        notes_root.mkdir(parents=True, exist_ok=True)
        note_path = (
            notes_root / self._note_filename(intent.action_id, title)
        ).resolve()
        try:
            note_path.relative_to(notes_root)
        except ValueError:
            return DesktopActionExecutionResult(
                action_id=intent.action_id,
                action_type=intent.action_type,
                status=ActionExecutionStatus.DENIED,
                message="note_path_outside_allowed_directory",
            )

        note_path.write_text(
            f"# {title}\n\n{body.strip()}\n",
            encoding="utf-8",
        )
        return DesktopActionExecutionResult(
            action_id=intent.action_id,
            action_type=intent.action_type,
            status=ActionExecutionStatus.EXECUTED,
            message="local_note_created",
            output={"note_path": str(note_path)},
        )

    @staticmethod
    def _note_filename(action_id: str, title: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", title.strip().lower()).strip("-")
        if not slug:
            slug = "note"
        short_id = action_id.split("-", maxsplit=1)[0]
        return f"{short_id}-{slug[:48]}.md"
