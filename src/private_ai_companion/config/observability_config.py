from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_OBSERVABILITY_CONFIG_PATH = Path("configs/observability.default.toml")


class ObservabilityConfigError(ConfigError):
    """Raised when observability configuration is invalid."""


@dataclass(frozen=True, slots=True)
class ObservabilityConfig:
    enabled: bool
    structured_logging_enabled: bool
    max_log_records: int
    event_replay_enabled: bool
    max_replay_events: int
    metrics_enabled: bool
    health_checks_enabled: bool


def load_observability_config(path: Path | None = None) -> ObservabilityConfig:
    config_path = path or DEFAULT_OBSERVABILITY_CONFIG_PATH
    if not config_path.exists():
        return default_observability_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    observability_raw = _required_mapping(raw, "observability")
    return ObservabilityConfig(
        enabled=_required_bool(observability_raw, "enabled"),
        structured_logging_enabled=_required_bool(
            observability_raw,
            "structured_logging_enabled",
        ),
        max_log_records=_required_positive_int(
            observability_raw,
            "max_log_records",
        ),
        event_replay_enabled=_required_bool(
            observability_raw,
            "event_replay_enabled",
        ),
        max_replay_events=_required_positive_int(
            observability_raw,
            "max_replay_events",
        ),
        metrics_enabled=_required_bool(observability_raw, "metrics_enabled"),
        health_checks_enabled=_required_bool(
            observability_raw,
            "health_checks_enabled",
        ),
    )


def default_observability_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        enabled=True,
        structured_logging_enabled=True,
        max_log_records=500,
        event_replay_enabled=True,
        max_replay_events=500,
        metrics_enabled=True,
        health_checks_enabled=True,
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise ObservabilityConfigError(
            f"observability config section {key!r} must be a table"
        )
    return cast(Mapping[str, object], value)


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ObservabilityConfigError(
            f"observability config field {key!r} must be boolean"
        )
    return value


def _required_positive_int(mapping: Mapping[str, object], key: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or value < 1:
        raise ObservabilityConfigError(
            f"observability config field {key!r} must be positive integer"
        )
    return value
