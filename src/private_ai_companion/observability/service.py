from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core import BaseEvent, EventBus, Subscription
from private_ai_companion.observability.health import HealthCheckService
from private_ai_companion.observability.metrics import EventMetricsCollector
from private_ai_companion.observability.models import DiagnosticsSnapshot
from private_ai_companion.observability.replay import EventReplayRecorder
from private_ai_companion.observability.structured_log import (
    InMemoryStructuredLogSink,
    StructuredEventLogger,
)


@dataclass(slots=True)
class ObservabilityService:
    metrics: EventMetricsCollector
    replay_recorder: EventReplayRecorder
    structured_logger: StructuredEventLogger
    log_sink: InMemoryStructuredLogSink
    enabled: bool = True
    _subscription: Subscription | None = None

    def subscribe_to(self, event_bus: EventBus) -> None:
        if self._subscription is None:
            self._subscription = event_bus.subscribe(BaseEvent, self.record_event)

    def record_event(self, event: BaseEvent) -> None:
        if not self.enabled:
            return

        self.metrics.record(event)
        self.replay_recorder.record(event)
        self.structured_logger.record(event)

    def diagnostics(self, health_checks: HealthCheckService) -> DiagnosticsSnapshot:
        return DiagnosticsSnapshot(
            health=health_checks.run(),
            metrics=self.metrics.snapshot(),
            replay_records=self.replay_recorder.replay(),
            log_records=self.log_sink.list_records(),
        )
