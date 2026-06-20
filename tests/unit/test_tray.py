from __future__ import annotations

import asyncio
from pathlib import Path

from rich.console import Console

from private_ai_companion.bootstrap import (
    Application,
    ApplicationConfigPaths,
    create_application,
)
from private_ai_companion.memory import (
    MemoryCandidate,
    MemorySensitivity,
    MemorySource,
)
from private_ai_companion.ui import (
    RichTrayStatusApp,
    build_dashboard_snapshot,
    build_tray_snapshot,
)


def test_tray_snapshot_exposes_status_and_menu(tmp_path: Path) -> None:
    application = _create_application_with_memory(tmp_path)
    application.memory_review.submit_candidate(
        MemoryCandidate(
            content="User wants memory review from tray.",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.LOW,
            confidence=0.9,
        )
    )

    tray = build_tray_snapshot(build_dashboard_snapshot(application))

    assert tray.status == "created"
    assert "private-ai-companion" in tray.tooltip
    assert [item.command for item in tray.menu_items] == [
        "dashboard",
        "chat",
        "memory-review",
        "permissions",
        "quit",
    ]
    assert tray.menu_items[2].enabled is True


def test_rich_tray_status_app_renders_menu(tmp_path: Path) -> None:
    console = Console(record=True, width=120, force_terminal=False)
    app = RichTrayStatusApp(
        application=_create_application_with_memory(tmp_path),
        console=console,
    )

    exit_code = asyncio.run(app.run_once())
    output = console.export_text()

    assert exit_code == 0
    assert "Tray status" in output
    assert "Abrir dashboard" in output
    assert "Ver permissoes" in output


def _create_application_with_memory(tmp_path: Path) -> Application:
    config_path = tmp_path / "memory.toml"
    database_path = tmp_path / "memory.sqlite3"
    config_path.write_text(
        f"""
[memory]
database_path = "{database_path.as_posix()}"
auto_approve_low_sensitivity = false
retention_days = 365

[memory.policy]
reject_sensitive_by_default = true
minimum_confidence = 0.40
""".strip(),
        encoding="utf-8",
    )
    return create_application(config_paths=ApplicationConfigPaths(memory=config_path))
