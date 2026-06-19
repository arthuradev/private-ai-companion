from __future__ import annotations

import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_SKILLS_CONFIG_PATH = Path("configs/skills.default.toml")
SUPPORTED_SKILL_IDS = {
    "builtin.status",
    "builtin.local_note",
    "builtin.open_allowed_app",
}
SUPPORTED_SKILL_PERMISSIONS = {
    "status.read",
    "desktop.action",
}
SUPPORTED_SKILL_ACTION_TYPES = {
    "desktop.create_note",
    "desktop.open_allowed_app",
}


class SkillsConfigError(ConfigError):
    """Raised when skills configuration is invalid."""


@dataclass(frozen=True, slots=True)
class SkillConfig:
    skill_id: str
    enabled: bool
    permissions: tuple[str, ...]
    allowed_action_types: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SkillsConfig:
    enabled: bool
    skills: tuple[SkillConfig, ...]


def load_skills_config(path: Path | None = None) -> SkillsConfig:
    config_path = path or DEFAULT_SKILLS_CONFIG_PATH
    if not config_path.exists():
        return default_skills_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    skills_raw = _required_mapping(raw, "skills")
    return SkillsConfig(
        enabled=_required_bool(skills_raw, "enabled"),
        skills=_skill_configs(skills_raw),
    )


def default_skills_config() -> SkillsConfig:
    return SkillsConfig(
        enabled=True,
        skills=(
            SkillConfig(
                skill_id="builtin.status",
                enabled=True,
                permissions=("status.read",),
                allowed_action_types=(),
            ),
            SkillConfig(
                skill_id="builtin.local_note",
                enabled=True,
                permissions=("desktop.action",),
                allowed_action_types=("desktop.create_note",),
            ),
            SkillConfig(
                skill_id="builtin.open_allowed_app",
                enabled=True,
                permissions=("desktop.action",),
                allowed_action_types=("desktop.open_allowed_app",),
            ),
        ),
    )


def _skill_configs(mapping: Mapping[str, object]) -> tuple[SkillConfig, ...]:
    value = mapping.get("skill")
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        raise SkillsConfigError("skills config field 'skill' must be a table list")

    configs: list[SkillConfig] = []
    seen: set[str] = set()
    for item in cast(Sequence[object], value):
        if not isinstance(item, Mapping):
            raise SkillsConfigError("skills config skill entries must be tables")
        raw = cast(Mapping[str, object], item)
        skill_id = _skill_id(_required_text(raw, "skill_id"))
        if skill_id in seen:
            raise SkillsConfigError(f"duplicate skill config {skill_id!r}")
        seen.add(skill_id)
        configs.append(
            SkillConfig(
                skill_id=skill_id,
                enabled=_required_bool(raw, "enabled"),
                permissions=_permissions(_required_text_sequence(raw, "permissions")),
                allowed_action_types=_action_types(
                    _required_text_sequence(raw, "allowed_action_types")
                ),
            )
        )
    return tuple(configs)


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise SkillsConfigError(f"skills config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SkillsConfigError(f"skills config field {key!r} must be text")
    return value.strip()


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise SkillsConfigError(f"skills config field {key!r} must be boolean")
    return value


def _required_text_sequence(
    mapping: Mapping[str, object],
    key: str,
) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        raise SkillsConfigError(f"skills config field {key!r} must be a list")
    items: list[str] = []
    for item in cast(Sequence[object], value):
        if not isinstance(item, str) or not item.strip():
            raise SkillsConfigError(
                f"skills config field {key!r} must contain text values"
            )
        items.append(item.strip())
    if len(set(items)) != len(items):
        raise SkillsConfigError(f"skills config field {key!r} must be unique")
    return tuple(items)


def _skill_id(value: str) -> str:
    if value not in SUPPORTED_SKILL_IDS:
        raise SkillsConfigError(f"unknown skill id {value!r}")
    return value


def _permissions(values: tuple[str, ...]) -> tuple[str, ...]:
    unknown = sorted(set(values) - SUPPORTED_SKILL_PERMISSIONS)
    if unknown:
        raise SkillsConfigError(f"unknown skill permissions {unknown!r}")
    return values


def _action_types(values: tuple[str, ...]) -> tuple[str, ...]:
    unknown = sorted(set(values) - SUPPORTED_SKILL_ACTION_TYPES)
    if unknown:
        raise SkillsConfigError(f"unknown skill action types {unknown!r}")
    return values
