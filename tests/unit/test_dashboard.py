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
from private_ai_companion.ui import RichDashboardApp, build_dashboard_snapshot


def test_dashboard_snapshot_includes_config_memory_and_permissions(
    tmp_path: Path,
) -> None:
    application = _create_application_with_memory(tmp_path)
    application.memory_review.submit_candidate(
        MemoryCandidate(
            content="User likes local dashboards.",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.LOW,
            confidence=0.9,
        )
    )

    snapshot = build_dashboard_snapshot(application)

    assert snapshot.runtime_phase == "created"
    assert snapshot.persona_display_name == "Companion"
    assert snapshot.pending_memory_count == 1
    assert "desktop.open_allowed_app" in snapshot.allowed_action_types
    assert "medium" in snapshot.confirmation_risk_levels
    assert "builtin.status" in snapshot.enabled_skill_ids


def test_rich_dashboard_app_renders_sections(tmp_path: Path) -> None:
    console = Console(record=True, width=120, force_terminal=False)
    application = _create_application_with_memory(tmp_path)
    app = RichDashboardApp(application=application, console=console)

    exit_code = asyncio.run(app.run_once())
    output = console.export_text()

    assert exit_code == 0
    assert "Dashboard local" in output
    assert "Configuracao e status" in output
    assert "Memoria local" in output
    assert "Permissoes e acoes locais" in output
    assert "builtin.status" in output


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
