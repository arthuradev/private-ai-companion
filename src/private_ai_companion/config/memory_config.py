from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_MEMORY_CONFIG_PATH = Path("configs/memory.default.toml")


class MemoryConfigError(ConfigError):
    """Raised when memory configuration is invalid."""


@dataclass(frozen=True, slots=True)
class MemoryPolicyConfig:
    reject_sensitive_by_default: bool
    minimum_confidence: float


@dataclass(frozen=True, slots=True)
class MemoryConfig:
    database_path: Path
    auto_approve_low_sensitivity: bool
    retention_days: int
    policy: MemoryPolicyConfig


def load_memory_config(path: Path | None = None) -> MemoryConfig:
    config_path = path or DEFAULT_MEMORY_CONFIG_PATH
    if not config_path.exists():
        return default_memory_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    memory_raw = _required_mapping(raw, "memory")
    policy_raw = _required_mapping(memory_raw, "policy")
    return MemoryConfig(
        database_path=Path(_required_text(memory_raw, "database_path")),
        auto_approve_low_sensitivity=_required_bool(
            memory_raw,
            "auto_approve_low_sensitivity",
        ),
        retention_days=_required_int(memory_raw, "retention_days"),
        policy=MemoryPolicyConfig(
            reject_sensitive_by_default=_required_bool(
                policy_raw,
                "reject_sensitive_by_default",
            ),
            minimum_confidence=_required_float(policy_raw, "minimum_confidence"),
        ),
    )


def default_memory_config() -> MemoryConfig:
    return MemoryConfig(
        database_path=Path("data/memory.sqlite3"),
        auto_approve_low_sensitivity=False,
        retention_days=365,
        policy=MemoryPolicyConfig(
            reject_sensitive_by_default=True,
            minimum_confidence=0.40,
        ),
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise MemoryConfigError(f"memory config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise MemoryConfigError(f"memory config field {key!r} must be text")
    return value.strip()


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise MemoryConfigError(f"memory config field {key!r} must be boolean")
    return value


def _required_int(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or value < 1:
        raise MemoryConfigError(f"memory config field {key!r} must be positive integer")
    return value


def _required_float(mapping: Mapping[str, object], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, int | float):
        raise MemoryConfigError(f"memory config field {key!r} must be number")
    result = float(value)
    if not 0 <= result <= 1:
        raise MemoryConfigError(f"memory config field {key!r} must be between 0 and 1")
    return result
