from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import (
    DesktopConfigError,
    default_desktop_config,
    load_desktop_config,
)


def test_default_desktop_config_is_safe() -> None:
    config = default_desktop_config()

    assert config.actions.enabled is True
    assert config.actions.executor_id == "safe-local-desktop"
    assert config.actions.allow_high_risk is False
    assert config.actions.allow_critical_risk is False
    assert config.actions.require_confirmation_for == ("medium", "high")
    assert "desktop.create_note" in config.actions.allowed_action_types
    assert config.notes.directory == "data/notes"
    assert config.allowed_apps["calculator"] == "Calculator"


def test_load_desktop_config_from_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "desktop.toml"
    config_path.write_text(
        """
[desktop.actions]
enabled = true
executor_id = "safe-local-desktop"
allowed_action_types = ["desktop.read_active_window_title"]
require_confirmation_for = ["medium"]
allow_high_risk = false
allow_critical_risk = false

[desktop.notes]
enabled = false
directory = "data/notes"
max_note_bytes = 1024

[desktop.window]
active_window_title_enabled = true
fake_active_window_title = "Test Window"

[desktop.allowed_apps]
calculator = "Calculator"
""",
        encoding="utf-8",
    )

    config = load_desktop_config(config_path)

    assert config.actions.allowed_action_types == ("desktop.read_active_window_title",)
    assert config.notes.enabled is False
    assert config.window.fake_active_window_title == "Test Window"


def test_load_desktop_config_rejects_critical_risk_typo(tmp_path: Path) -> None:
    config_path = tmp_path / "desktop.toml"
    config_path.write_text(
        """
[desktop.actions]
enabled = true
executor_id = "safe-local-desktop"
allowed_action_types = ["desktop.read_active_window_title"]
require_confirmation_for = ["mediumish"]
allow_high_risk = false
allow_critical_risk = false

[desktop.notes]
enabled = true
directory = "data/notes"
max_note_bytes = 1024

[desktop.window]
active_window_title_enabled = true
fake_active_window_title = "Test Window"

[desktop.allowed_apps]
calculator = "Calculator"
""",
        encoding="utf-8",
    )

    with pytest.raises(DesktopConfigError, match="unknown risk levels"):
        load_desktop_config(config_path)
