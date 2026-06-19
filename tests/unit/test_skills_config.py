from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import (
    SkillsConfigError,
    default_skills_config,
    load_skills_config,
)


def test_default_skills_config_enables_builtin_skills() -> None:
    config = default_skills_config()

    assert config.enabled is True
    assert [skill.skill_id for skill in config.skills] == [
        "builtin.status",
        "builtin.local_note",
        "builtin.open_allowed_app",
    ]
    assert config.skills[1].allowed_action_types == ("desktop.create_note",)


def test_load_skills_config_from_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "skills.toml"
    config_path.write_text(
        """
[skills]
enabled = true

[[skills.skill]]
skill_id = "builtin.status"
enabled = true
permissions = ["status.read"]
allowed_action_types = []
""",
        encoding="utf-8",
    )

    config = load_skills_config(config_path)

    assert len(config.skills) == 1
    assert config.skills[0].skill_id == "builtin.status"


def test_load_skills_config_rejects_unknown_permission(tmp_path: Path) -> None:
    config_path = tmp_path / "skills.toml"
    config_path.write_text(
        """
[skills]
enabled = true

[[skills.skill]]
skill_id = "builtin.status"
enabled = true
permissions = ["secrets.read"]
allowed_action_types = []
""",
        encoding="utf-8",
    )

    with pytest.raises(SkillsConfigError, match="unknown skill permissions"):
        load_skills_config(config_path)
