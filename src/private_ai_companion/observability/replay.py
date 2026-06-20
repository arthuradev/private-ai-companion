from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from private_ai_companion.core import BaseEvent
from private_ai_companion.observability.models import EventReplayRecord
from private_ai_companion.observability.redaction import sanitize_event


def _empty_replay_records() -> deque[EventReplayRecord]:
    return deque()


@dataclass(slots=True)
class EventReplayRecorder:
    max_records: int
    enabled: bool = True
    _records: deque[EventReplayRecord] = field(default_factory=_empty_replay_records)

    def record(self, event: BaseEvent) -> EventReplayRecord | None:
        if not self.enabled:
            return None

        payload = sanitize_event(event)
        record = EventReplayRecord(
            event_name=event.name,
            event_id=event.metadata.event_id,
            occurred_at=event.metadata.occurred_at,
            source=event.metadata.source,
            sensitivity=event.metadata.sensitivity.value,
            fields=payload.fields,
            redacted_fields=payload.redacted_fields,
        )
        self._records.append(record)
        while len(self._records) > self.max_records:
            self._records.popleft()
        return record

    def replay(self) -> tuple[EventReplayRecord, ...]:
        return tuple(self._records)

    def clear(self) -> None:
        self._records.clear()
