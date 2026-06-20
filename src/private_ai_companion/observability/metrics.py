from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from private_ai_companion.core import BaseEvent
from private_ai_companion.observability.models import MetricsSnapshot


def _empty_counter() -> Counter[str]:
    return Counter()


@dataclass(slots=True)
class EventMetricsCollector:
    enabled: bool = True
    _events_by_name: Counter[str] = field(default_factory=_empty_counter)
    _events_by_source: Counter[str] = field(default_factory=_empty_counter)
    _events_by_sensitivity: Counter[str] = field(default_factory=_empty_counter)

    def record(self, event: BaseEvent) -> None:
        if not self.enabled:
            return

        self._events_by_name[event.name] += 1
        self._events_by_source[event.metadata.source] += 1
        self._events_by_sensitivity[event.metadata.sensitivity.value] += 1

    def snapshot(self) -> MetricsSnapshot:
        return MetricsSnapshot(
            total_events=sum(self._events_by_name.values()),
            events_by_name=dict(self._events_by_name),
            events_by_source=dict(self._events_by_source),
            events_by_sensitivity=dict(self._events_by_sensitivity),
        )

    def clear(self) -> None:
        self._events_by_name.clear()
        self._events_by_source.clear()
        self._events_by_sensitivity.clear()
