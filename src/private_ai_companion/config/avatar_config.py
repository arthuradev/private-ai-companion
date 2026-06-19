from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_AVATAR_CONFIG_PATH = Path("configs/avatar.default.toml")
SUPPORTED_AVATAR_PROVIDER_IDS = {"fake-avatar", "vtube-studio"}
SUPPORTED_AVATAR_EXPRESSIONS = {
    "idle",
    "listening",
    "thinking",
    "speaking",
    "interrupted",
    "happy",
    "curious",
    "concerned",
    "confused",
    "neutral",
}


class AvatarConfigError(ConfigError):
    """Raised when avatar configuration is invalid."""


@dataclass(frozen=True, slots=True)
class AvatarExpressionHotkeyConfig:
    expression: str
    hotkey_id: str


@dataclass(frozen=True, slots=True)
class VTubeStudioConfig:
    host: str
    port: int
    plugin_name: str
    plugin_developer: str
    authentication_token_env: str
    request_token_on_connect: bool


@dataclass(frozen=True, slots=True)
class AvatarIdleConfig:
    enabled: bool
    expression: str
    interval_seconds: float


@dataclass(frozen=True, slots=True)
class AvatarLipsyncConfig:
    enabled: bool
    parameter_name: str
    weight: float


@dataclass(frozen=True, slots=True)
class AvatarConfig:
    provider_id: str
    enabled: bool
    vtube_studio: VTubeStudioConfig
    expression_hotkeys: tuple[AvatarExpressionHotkeyConfig, ...]
    idle: AvatarIdleConfig
    lipsync: AvatarLipsyncConfig


def load_avatar_config(path: Path | None = None) -> AvatarConfig:
    config_path = path or DEFAULT_AVATAR_CONFIG_PATH
    if not config_path.exists():
        return default_avatar_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    avatar_raw = _required_mapping(raw, "avatar")
    vtube_raw = _required_mapping(avatar_raw, "vtube_studio")
    hotkeys_raw = _required_mapping(avatar_raw, "expression_hotkeys")
    idle_raw = _required_mapping(avatar_raw, "idle")
    lipsync_raw = _required_mapping(avatar_raw, "lipsync")

    return AvatarConfig(
        provider_id=_provider_id(_required_text(avatar_raw, "provider_id")),
        enabled=_required_bool(avatar_raw, "enabled"),
        vtube_studio=VTubeStudioConfig(
            host=_required_text(vtube_raw, "host"),
            port=_port(vtube_raw, "port"),
            plugin_name=_plugin_text(vtube_raw, "plugin_name"),
            plugin_developer=_plugin_text(vtube_raw, "plugin_developer"),
            authentication_token_env=_required_text(
                vtube_raw,
                "authentication_token_env",
            ),
            request_token_on_connect=_required_bool(
                vtube_raw,
                "request_token_on_connect",
            ),
        ),
        expression_hotkeys=_expression_hotkeys(hotkeys_raw),
        idle=AvatarIdleConfig(
            enabled=_required_bool(idle_raw, "enabled"),
            expression=_expression(_required_text(idle_raw, "expression")),
            interval_seconds=_positive_float(idle_raw, "interval_seconds"),
        ),
        lipsync=AvatarLipsyncConfig(
            enabled=_required_bool(lipsync_raw, "enabled"),
            parameter_name=_required_text(lipsync_raw, "parameter_name"),
            weight=_ratio(lipsync_raw, "weight"),
        ),
    )


def default_avatar_config() -> AvatarConfig:
    return AvatarConfig(
        provider_id="fake-avatar",
        enabled=True,
        vtube_studio=VTubeStudioConfig(
            host="localhost",
            port=8001,
            plugin_name="private-ai-companion",
            plugin_developer="private-ai-companion",
            authentication_token_env="PRIVATE_AI_COMPANION_VTS_TOKEN",
            request_token_on_connect=False,
        ),
        expression_hotkeys=(),
        idle=AvatarIdleConfig(
            enabled=True,
            expression="idle",
            interval_seconds=30.0,
        ),
        lipsync=AvatarLipsyncConfig(
            enabled=True,
            parameter_name="MouthOpen",
            weight=1.0,
        ),
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise AvatarConfigError(f"avatar config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AvatarConfigError(f"avatar config field {key!r} must be text")
    return value.strip()


def _plugin_text(mapping: Mapping[str, object], key: str) -> str:
    value = _required_text(mapping, key)
    if len(value) < 3 or len(value) > 32:
        raise AvatarConfigError(
            f"avatar config field {key!r} must be 3 to 32 characters"
        )
    return value


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise AvatarConfigError(f"avatar config field {key!r} must be boolean")
    return value


def _provider_id(value: str) -> str:
    if value not in SUPPORTED_AVATAR_PROVIDER_IDS:
        raise AvatarConfigError(f"unknown avatar provider {value!r}")
    return value


def _expression(value: str) -> str:
    if value not in SUPPORTED_AVATAR_EXPRESSIONS:
        raise AvatarConfigError(f"unknown avatar expression {value!r}")
    return value


def _expression_hotkeys(
    mapping: Mapping[str, object],
) -> tuple[AvatarExpressionHotkeyConfig, ...]:
    hotkeys: list[AvatarExpressionHotkeyConfig] = []
    for expression_name, hotkey_value in sorted(mapping.items()):
        expression = _expression(expression_name)
        if hotkey_value is None:
            continue
        if not isinstance(hotkey_value, str):
            raise AvatarConfigError(
                f"avatar hotkey for {expression_name!r} must be text or null"
            )
        hotkey_id = hotkey_value.strip()
        if hotkey_id:
            hotkeys.append(
                AvatarExpressionHotkeyConfig(
                    expression=expression,
                    hotkey_id=hotkey_id,
                )
            )
    return tuple(hotkeys)


def _port(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int):
        raise AvatarConfigError(f"avatar config field {key!r} must be an integer")
    if value < 1 or value > 65535:
        raise AvatarConfigError(f"avatar config field {key!r} must be a TCP port")
    return value


def _ratio(mapping: Mapping[str, object], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, int | float):
        raise AvatarConfigError(f"avatar config field {key!r} must be a number")
    ratio = float(value)
    if ratio < 0.0 or ratio > 1.0:
        raise AvatarConfigError(f"avatar config field {key!r} must be between 0 and 1")
    return ratio


def _positive_float(mapping: Mapping[str, object], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, int | float):
        raise AvatarConfigError(f"avatar config field {key!r} must be a number")
    number = float(value)
    if number <= 0.0:
        raise AvatarConfigError(f"avatar config field {key!r} must be positive")
    return number
