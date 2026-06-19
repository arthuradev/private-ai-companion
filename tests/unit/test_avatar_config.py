from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import AvatarConfigError, load_avatar_config


def test_load_avatar_config_reads_default_file() -> None:
    config = load_avatar_config()

    assert config.provider_id == "fake-avatar"
    assert config.enabled is True
    assert config.vtube_studio.host == "localhost"
    assert config.vtube_studio.port == 8001
    assert config.vtube_studio.authentication_token_env
    assert config.expression_hotkeys == ()
    assert config.idle.expression == "idle"
    assert config.lipsync.parameter_name == "MouthOpen"


def test_load_avatar_config_reads_custom_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "avatar.toml"
    config_path.write_text(
        """
[avatar]
provider_id = "vtube-studio"
enabled = true

[avatar.vtube_studio]
host = "127.0.0.1"
port = 9001
plugin_name = "test companion"
plugin_developer = "test developer"
authentication_token_env = "TEST_VTS_TOKEN"
request_token_on_connect = true

[avatar.expression_hotkeys]
happy = "hotkey-happy"
speaking = "hotkey-speaking"
idle = ""

[avatar.idle]
enabled = true
expression = "neutral"
interval_seconds = 12.0

[avatar.lipsync]
enabled = true
parameter_name = "ParamMouthOpenY"
weight = 0.5
""".strip(),
        encoding="utf-8",
    )

    config = load_avatar_config(config_path)

    assert config.provider_id == "vtube-studio"
    assert config.vtube_studio.host == "127.0.0.1"
    assert config.vtube_studio.request_token_on_connect is True
    assert config.expression_hotkeys[0].expression == "happy"
    assert config.expression_hotkeys[0].hotkey_id == "hotkey-happy"
    assert config.lipsync.weight == 0.5


def test_load_avatar_config_rejects_unknown_expression(tmp_path: Path) -> None:
    config_path = tmp_path / "avatar.toml"
    config_path.write_text(
        """
[avatar]
provider_id = "fake-avatar"
enabled = true

[avatar.vtube_studio]
host = "localhost"
port = 8001
plugin_name = "test companion"
plugin_developer = "test developer"
authentication_token_env = "TEST_VTS_TOKEN"
request_token_on_connect = false

[avatar.expression_hotkeys]
sparkly = "hotkey"

[avatar.idle]
enabled = true
expression = "idle"
interval_seconds = 30.0

[avatar.lipsync]
enabled = true
parameter_name = "MouthOpen"
weight = 1.0
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(AvatarConfigError):
        load_avatar_config(config_path)
