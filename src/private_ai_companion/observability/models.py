from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

JsonScalar = str | int | float | bool | None


def _empty_fields() -> dict[str, JsonScalar]:
    return {}


def _empty_string_tuple() -> tuple[str, ...]:
    return ()


@dataclass(frozen=True, slots=True)
class SanitizedEventPayload:
    fields: dict[str, JsonScalar] = field(default_factory=_empty_fields)
    redacted_fields: tuple[str, ...] = field(default_factory=_empty_string_tuple)


@dataclass(frozen=True, slots=True)
class EventReplayRecord:
    event_name: str
    event_id: str
    occurred_at: datetime
    source: str
    sensitivity: str
    fields: dict[str, JsonScalar] = field(default_factory=_empty_fields)
    redacted_fields: tuple[str, ...] = field(default_factory=_empty_string_tuple)


class StructuredLogLevel(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class StructuredLogRecord:
    level: StructuredLogLevel
    message: str
    event_name: str
    event_id: str
    source: str
    sensitivity: str
    fields: dict[str, JsonScalar] = field(default_factory=_empty_fields)
    redacted_fields: tuple[str, ...] = field(default_factory=_empty_string_tuple)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_json_line(self) -> str:
        payload = {
            "created_at": self.created_at.isoformat(),
            "level": self.level.value,
            "message": self.message,
            "event_name": self.event_name,
            "event_id": self.event_id,
            "source": self.source,
            "sensitivity": self.sensitivity,
            "fields": self.fields,
            "redacted_fields": list(self.redacted_fields),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class MetricsSnapshot:
    total_events: int
    events_by_name: dict[str, int]
    events_by_source: dict[str, int]
    events_by_sensitivity: dict[str, int]


class HealthStatus(StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass(frozen=True, slots=True)
class HealthCheckResult:
    component_id: str
    status: HealthStatus
    message: str
    details: dict[str, JsonScalar] = field(default_factory=_empty_fields)


@dataclass(frozen=True, slots=True)
class HealthReport:
    status: HealthStatus
    checks: tuple[HealthCheckResult, ...]
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class DiagnosticsSnapshot:
    health: HealthReport
    metrics: MetricsSnapshot
    replay_records: tuple[EventReplayRecord, ...]
    log_records: tuple[StructuredLogRecord, ...]
