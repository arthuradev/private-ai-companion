from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from private_ai_companion.core import BaseEvent
from private_ai_companion.observability.models import (
    StructuredLogLevel,
    StructuredLogRecord,
)
from private_ai_companion.observability.redaction import sanitize_event


def _empty_log_records() -> deque[StructuredLogRecord]:
    return deque()


@dataclass(slots=True)
class InMemoryStructuredLogSink:
    max_records: int
    _records: deque[StructuredLogRecord] = field(default_factory=_empty_log_records)

    def append(self, record: StructuredLogRecord) -> None:
        self._records.append(record)
        while len(self._records) > self.max_records:
            self._records.popleft()

    def list_records(self) -> tuple[StructuredLogRecord, ...]:
        return tuple(self._records)

    def clear(self) -> None:
        self._records.clear()


@dataclass(frozen=True, slots=True)
class StructuredEventLogger:
    sink: InMemoryStructuredLogSink
    enabled: bool = True

    def record(self, event: BaseEvent) -> StructuredLogRecord | None:
        if not self.enabled:
            return None

        payload = sanitize_event(event)
        record = StructuredLogRecord(
            level=StructuredLogLevel.INFO,
            message=f"event.{event.name}",
            event_name=event.name,
            event_id=event.metadata.event_id,
            source=event.metadata.source,
            sensitivity=event.metadata.sensitivity.value,
            fields=payload.fields,
            redacted_fields=payload.redacted_fields,
        )
        self.sink.append(record)
        return record
