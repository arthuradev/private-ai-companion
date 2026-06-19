from __future__ import annotations

import asyncio
from pathlib import Path

from private_ai_companion.adapters.desktop import SafeLocalDesktopExecutor
from private_ai_companion.desktop import DesktopActionType
from private_ai_companion.safety import ActionExecutionStatus, ActionIntent, RiskLevel


def test_safe_local_desktop_executor_creates_note_inside_allowed_directory(
    tmp_path: Path,
) -> None:
    executor = SafeLocalDesktopExecutor(
        notes_directory=tmp_path,
        allowed_apps={"calculator": "Calculator"},
    )
    intent = ActionIntent(
        action_type=DesktopActionType.CREATE_NOTE,
        parameters={"title": "Hello Note", "body": "local only"},
    )

    result = asyncio.run(executor.execute(intent, RiskLevel.MEDIUM))

    assert result.status is ActionExecutionStatus.EXECUTED
    note_path = Path(result.output["note_path"])
    assert note_path.is_file()
    assert note_path.parent == tmp_path.resolve()
    assert "local only" in note_path.read_text(encoding="utf-8")


def test_safe_local_desktop_executor_rejects_large_note(tmp_path: Path) -> None:
    executor = SafeLocalDesktopExecutor(
        notes_directory=tmp_path,
        allowed_apps={},
        max_note_bytes=4,
    )
    intent = ActionIntent(
        action_type=DesktopActionType.CREATE_NOTE,
        parameters={"title": "too big", "body": "12345"},
    )

    result = asyncio.run(executor.execute(intent, RiskLevel.MEDIUM))

    assert result.status is ActionExecutionStatus.FAILED
    assert result.message == "note_body_too_large"


def test_safe_local_desktop_executor_simulates_allowed_app_launch(
    tmp_path: Path,
) -> None:
    executor = SafeLocalDesktopExecutor(
        notes_directory=tmp_path,
        allowed_apps={"calculator": "Calculator"},
    )
    intent = ActionIntent(
        action_type=DesktopActionType.OPEN_ALLOWED_APP,
        parameters={"app_id": "calculator"},
    )

    result = asyncio.run(executor.execute(intent, RiskLevel.MEDIUM))

    assert result.status is ActionExecutionStatus.EXECUTED
    assert result.message == "allowed_app_launch_simulated"
    assert result.output["display_name"] == "Calculator"
