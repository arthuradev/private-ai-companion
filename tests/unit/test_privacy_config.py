from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import (
    PrivacyConfigError,
    default_privacy_config,
    load_privacy_config,
)


def test_default_privacy_config_is_conservative() -> None:
    config = default_privacy_config()

    assert config.screen_capture.enabled is True
    assert config.screen_capture.provider_id == "fake-screen-capture"
    assert config.screen_capture.require_user_authorization is True
    assert config.screen_capture.allow_continuous_capture is False
    assert config.screen_capture.persist_screenshots_by_default is False
    assert config.screen_capture.allow_external_analysis is False
    assert config.redaction.enabled is True
    assert config.vision.provider_id == "fake-vision"
    assert config.vision.local_only is True


def test_load_privacy_config_from_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "privacy.toml"
    config_path.write_text(
        """
[privacy.screen_capture]
enabled = true
provider_id = "fake-screen-capture"
require_user_authorization = true
allow_continuous_capture = false
persist_screenshots_by_default = false
allow_external_analysis = false

[privacy.redaction]
enabled = true
redact_text_metadata = true

[privacy.vision]
provider_id = "fake-vision"
local_only = true
""",
        encoding="utf-8",
    )

    config = load_privacy_config(config_path)

    assert config.screen_capture.provider_id == "fake-screen-capture"
    assert config.vision.provider_id == "fake-vision"


def test_load_privacy_config_rejects_unknown_provider(tmp_path: Path) -> None:
    config_path = tmp_path / "privacy.toml"
    config_path.write_text(
        """
[privacy.screen_capture]
enabled = true
provider_id = "real-screen"
require_user_authorization = true
allow_continuous_capture = false
persist_screenshots_by_default = false
allow_external_analysis = false

[privacy.redaction]
enabled = true
redact_text_metadata = true

[privacy.vision]
provider_id = "fake-vision"
local_only = true
""",
        encoding="utf-8",
    )

    with pytest.raises(PrivacyConfigError, match="unknown screen capture provider"):
        load_privacy_config(config_path)
