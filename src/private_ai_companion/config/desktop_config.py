from __future__ import annotations

import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_DESKTOP_CONFIG_PATH = Path("configs/desktop.default.toml")
SUPPORTED_DESKTOP_EXECUTOR_IDS = {"safe-local-desktop"}
SUPPORTED_DESKTOP_ACTION_TYPES = {
    "desktop.read_active_window_title",
    "desktop.create_note",
    "desktop.open_allowed_app",
}
SUPPORTED_RISK_LEVELS = {"low", "medium", "high", "critical"}


class DesktopConfigError(ConfigError):
    """Raised when desktop action configuration is invalid."""


@dataclass(frozen=True, slots=True)
class DesktopActionsConfig:
    enabled: bool
    executor_id: str
    allowed_action_types: tuple[str, ...]
    require_confirmation_for: tuple[str, ...]
    allow_high_risk: bool
    allow_critical_risk: bool


@dataclass(frozen=True, slots=True)
class DesktopNotesConfig:
    enabled: bool
    directory: str
    max_note_bytes: int


@dataclass(frozen=True, slots=True)
class DesktopWindowConfig:
    active_window_title_enabled: bool
    fake_active_window_title: str


@dataclass(frozen=True, slots=True)
class DesktopConfig:
    actions: DesktopActionsConfig
    notes: DesktopNotesConfig
    window: DesktopWindowConfig
    allowed_apps: dict[str, str]


def load_desktop_config(path: Path | None = None) -> DesktopConfig:
    config_path = path or DEFAULT_DESKTOP_CONFIG_PATH
    if not config_path.exists():
        return default_desktop_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    desktop_raw = _required_mapping(raw, "desktop")
    actions_raw = _required_mapping(desktop_raw, "actions")
    notes_raw = _required_mapping(desktop_raw, "notes")
    window_raw = _required_mapping(desktop_raw, "window")
    allowed_apps_raw = _required_mapping(desktop_raw, "allowed_apps")

    return DesktopConfig(
        actions=DesktopActionsConfig(
            enabled=_required_bool(actions_raw, "enabled"),
            executor_id=_executor_id(_required_text(actions_raw, "executor_id")),
            allowed_action_types=_action_types(
                _required_text_sequence(actions_raw, "allowed_action_types")
            ),
            require_confirmation_for=_risk_levels(
                _required_text_sequence(actions_raw, "require_confirmation_for")
            ),
            allow_high_risk=_required_bool(actions_raw, "allow_high_risk"),
            allow_critical_risk=_required_bool(actions_raw, "allow_critical_risk"),
        ),
        notes=DesktopNotesConfig(
            enabled=_required_bool(notes_raw, "enabled"),
            directory=_required_text(notes_raw, "directory"),
            max_note_bytes=_positive_int(notes_raw, "max_note_bytes"),
        ),
        window=DesktopWindowConfig(
            active_window_title_enabled=_required_bool(
                window_raw,
                "active_window_title_enabled",
            ),
            fake_active_window_title=_required_text(
                window_raw,
                "fake_active_window_title",
            ),
        ),
        allowed_apps=_allowed_apps(allowed_apps_raw),
    )


def default_desktop_config() -> DesktopConfig:
    return DesktopConfig(
        actions=DesktopActionsConfig(
            enabled=True,
            executor_id="safe-local-desktop",
            allowed_action_types=(
                "desktop.read_active_window_title",
                "desktop.create_note",
                "desktop.open_allowed_app",
            ),
            require_confirmation_for=("medium", "high"),
            allow_high_risk=False,
            allow_critical_risk=False,
        ),
        notes=DesktopNotesConfig(
            enabled=True,
            directory="data/notes",
            max_note_bytes=4096,
        ),
        window=DesktopWindowConfig(
            active_window_title_enabled=True,
            fake_active_window_title="Private AI Companion",
        ),
        allowed_apps={
            "calculator": "Calculator",
            "notepad": "Notepad",
        },
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise DesktopConfigError(f"desktop config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DesktopConfigError(f"desktop config field {key!r} must be text")
    return value.strip()


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise DesktopConfigError(f"desktop config field {key!r} must be boolean")
    return value


def _required_text_sequence(
    mapping: Mapping[str, object],
    key: str,
) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        raise DesktopConfigError(f"desktop config field {key!r} must be a list")
    raw_items = cast(Sequence[object], value)
    items: list[str] = []
    for item in raw_items:
        if not isinstance(item, str) or not item.strip():
            raise DesktopConfigError(
                f"desktop config field {key!r} must contain text values"
            )
        items.append(item.strip())
    return tuple(items)


def _executor_id(value: str) -> str:
    if value not in SUPPORTED_DESKTOP_EXECUTOR_IDS:
        raise DesktopConfigError(f"unknown desktop executor {value!r}")
    return value


def _action_types(values: tuple[str, ...]) -> tuple[str, ...]:
    unknown = sorted(set(values) - SUPPORTED_DESKTOP_ACTION_TYPES)
    if unknown:
        raise DesktopConfigError(f"unknown desktop action types {unknown!r}")
    return values


def _risk_levels(values: tuple[str, ...]) -> tuple[str, ...]:
    unknown = sorted(set(values) - SUPPORTED_RISK_LEVELS)
    if unknown:
        raise DesktopConfigError(f"unknown risk levels {unknown!r}")
    return values


def _positive_int(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int):
        raise DesktopConfigError(f"desktop config field {key!r} must be an integer")
    if value <= 0:
        raise DesktopConfigError(f"desktop config field {key!r} must be positive")
    return value


def _allowed_apps(mapping: Mapping[str, object]) -> dict[str, str]:
    allowed_apps: dict[str, str] = {}
    for app_id, display_name in sorted(mapping.items()):
        if not isinstance(display_name, str) or not display_name.strip():
            raise DesktopConfigError(
                f"desktop allowed app {app_id!r} display name must be text"
            )
        allowed_apps[str(app_id)] = display_name.strip()
    return allowed_apps
