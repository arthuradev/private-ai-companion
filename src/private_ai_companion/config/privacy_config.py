from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_PRIVACY_CONFIG_PATH = Path("configs/privacy.default.toml")
SUPPORTED_CAPTURE_PROVIDER_IDS = {"fake-screen-capture"}
SUPPORTED_VISION_PROVIDER_IDS = {"fake-vision"}


class PrivacyConfigError(ConfigError):
    """Raised when privacy configuration is invalid."""


@dataclass(frozen=True, slots=True)
class ScreenCaptureConfig:
    enabled: bool
    provider_id: str
    require_user_authorization: bool
    allow_continuous_capture: bool
    persist_screenshots_by_default: bool
    allow_external_analysis: bool


@dataclass(frozen=True, slots=True)
class RedactionConfig:
    enabled: bool
    redact_text_metadata: bool


@dataclass(frozen=True, slots=True)
class VisionProviderConfig:
    provider_id: str
    local_only: bool


@dataclass(frozen=True, slots=True)
class PrivacyConfig:
    screen_capture: ScreenCaptureConfig
    redaction: RedactionConfig
    vision: VisionProviderConfig


def load_privacy_config(path: Path | None = None) -> PrivacyConfig:
    config_path = path or DEFAULT_PRIVACY_CONFIG_PATH
    if not config_path.exists():
        return default_privacy_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    privacy_raw = _required_mapping(raw, "privacy")
    screen_capture_raw = _required_mapping(privacy_raw, "screen_capture")
    redaction_raw = _required_mapping(privacy_raw, "redaction")
    vision_raw = _required_mapping(privacy_raw, "vision")

    return PrivacyConfig(
        screen_capture=ScreenCaptureConfig(
            enabled=_required_bool(screen_capture_raw, "enabled"),
            provider_id=_capture_provider_id(
                _required_text(screen_capture_raw, "provider_id")
            ),
            require_user_authorization=_required_bool(
                screen_capture_raw,
                "require_user_authorization",
            ),
            allow_continuous_capture=_required_bool(
                screen_capture_raw,
                "allow_continuous_capture",
            ),
            persist_screenshots_by_default=_required_bool(
                screen_capture_raw,
                "persist_screenshots_by_default",
            ),
            allow_external_analysis=_required_bool(
                screen_capture_raw,
                "allow_external_analysis",
            ),
        ),
        redaction=RedactionConfig(
            enabled=_required_bool(redaction_raw, "enabled"),
            redact_text_metadata=_required_bool(redaction_raw, "redact_text_metadata"),
        ),
        vision=VisionProviderConfig(
            provider_id=_vision_provider_id(_required_text(vision_raw, "provider_id")),
            local_only=_required_bool(vision_raw, "local_only"),
        ),
    )


def default_privacy_config() -> PrivacyConfig:
    return PrivacyConfig(
        screen_capture=ScreenCaptureConfig(
            enabled=True,
            provider_id="fake-screen-capture",
            require_user_authorization=True,
            allow_continuous_capture=False,
            persist_screenshots_by_default=False,
            allow_external_analysis=False,
        ),
        redaction=RedactionConfig(enabled=True, redact_text_metadata=True),
        vision=VisionProviderConfig(provider_id="fake-vision", local_only=True),
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise PrivacyConfigError(f"privacy config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PrivacyConfigError(f"privacy config field {key!r} must be text")
    return value.strip()


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise PrivacyConfigError(f"privacy config field {key!r} must be boolean")
    return value


def _capture_provider_id(value: str) -> str:
    if value not in SUPPORTED_CAPTURE_PROVIDER_IDS:
        raise PrivacyConfigError(f"unknown screen capture provider {value!r}")
    return value


def _vision_provider_id(value: str) -> str:
    if value not in SUPPORTED_VISION_PROVIDER_IDS:
        raise PrivacyConfigError(f"unknown vision provider {value!r}")
    return value
