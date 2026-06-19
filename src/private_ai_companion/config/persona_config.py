from __future__ import annotations

import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import cast

from private_ai_companion.brain import PersonaProfile, default_persona_profile
from private_ai_companion.config.errors import PersonaConfigError

DEFAULT_PERSONA_CONFIG_PATH = Path("configs/persona.default.toml")


def load_persona_profile(path: Path | None = None) -> PersonaProfile:
    config_path = path or DEFAULT_PERSONA_CONFIG_PATH
    if not config_path.exists():
        return default_persona_profile()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    persona_raw = _required_mapping(raw, "persona")
    return PersonaProfile(
        display_name=_required_text(persona_raw, "display_name"),
        short_description=_required_text(persona_raw, "short_description"),
        primary_language=_required_text(persona_raw, "primary_language"),
        tone=_required_text(persona_raw, "tone"),
        speaking_style=_required_text_tuple(persona_raw, "speaking_style"),
        proactivity=_required_text(persona_raw, "proactivity"),
        boundaries=_required_text_tuple(persona_raw, "boundaries"),
        voice_id=_optional_text(persona_raw, "voice_id"),
        avatar_id=_optional_text(persona_raw, "avatar_id"),
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise PersonaConfigError(f"persona config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PersonaConfigError(f"persona config field {key!r} must be text")
    return value.strip()


def _optional_text(mapping: Mapping[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise PersonaConfigError(f"persona config field {key!r} must be text")
    stripped = value.strip()
    return stripped or None


def _required_text_tuple(mapping: Mapping[str, object], key: str) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, list):
        raise PersonaConfigError(f"persona config field {key!r} must be a text list")

    result: list[str] = []
    items = cast(list[object], value)
    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise PersonaConfigError(
                f"persona config field {key!r} must contain only text"
            )
        result.append(item.strip())

    if not result:
        raise PersonaConfigError(f"persona config field {key!r} cannot be empty")
    return tuple(result)
