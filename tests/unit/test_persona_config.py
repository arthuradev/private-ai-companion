from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import PersonaConfigError, load_persona_profile


def test_load_persona_profile_uses_default_when_file_is_missing(tmp_path: Path) -> None:
    profile = load_persona_profile(tmp_path / "missing.toml")

    assert profile.display_name == "Companion"
    assert profile.primary_language == "pt-BR"


def test_load_persona_profile_reads_custom_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "persona.toml"
    config_path.write_text(
        """
[persona]
display_name = "Local Friend"
short_description = "A test persona."
primary_language = "en-US"
tone = "calm"
speaking_style = ["brief", "curious"]
proactivity = "low"
boundaries = ["Ask before storing memories."]
voice_id = "voice-local"
avatar_id = "avatar-local"
""".strip(),
        encoding="utf-8",
    )

    profile = load_persona_profile(config_path)

    assert profile.display_name == "Local Friend"
    assert profile.speaking_style == ("brief", "curious")
    assert profile.boundaries == ("Ask before storing memories.",)
    assert profile.voice_id == "voice-local"
    assert profile.avatar_id == "avatar-local"


def test_load_persona_profile_rejects_invalid_toml_shape(tmp_path: Path) -> None:
    config_path = tmp_path / "persona.toml"
    config_path.write_text("[persona]\ndisplay_name = ''\n", encoding="utf-8")

    with pytest.raises(PersonaConfigError):
        load_persona_profile(config_path)
