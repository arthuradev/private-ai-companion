from __future__ import annotations

import asyncio

from private_ai_companion.core import (
    AppStarted,
    AssistantTextReady,
    EventBus,
    EventMetadata,
    EventSensitivity,
    UserTextReceived,
)
from private_ai_companion.observability import (
    ComponentHealthCheck,
    EventMetricsCollector,
    EventReplayRecorder,
    HealthCheckService,
    HealthStatus,
    InMemoryStructuredLogSink,
    ObservabilityService,
    StructuredEventLogger,
    pass_check,
)


def test_observability_service_records_sanitized_events() -> None:
    event_bus = EventBus()
    log_sink = InMemoryStructuredLogSink(max_records=10)
    service = ObservabilityService(
        metrics=EventMetricsCollector(),
        replay_recorder=EventReplayRecorder(max_records=10),
        structured_logger=StructuredEventLogger(sink=log_sink),
        log_sink=log_sink,
    )
    service.subscribe_to(event_bus)

    asyncio.run(
        event_bus.publish(
            UserTextReceived(
                text="secret user text",
                metadata=EventMetadata(
                    source="interaction",
                    sensitivity=EventSensitivity.PRIVATE,
                ),
            )
        )
    )
    asyncio.run(
        event_bus.publish(
            AssistantTextReady(
                text="private assistant response",
                metadata=EventMetadata(source="interaction"),
            )
        )
    )

    replay_text = repr(service.replay_recorder.replay())
    log_text = "\n".join(record.to_json_line() for record in log_sink.list_records())

    assert "secret user text" not in replay_text
    assert "private assistant response" not in replay_text
    assert "secret user text" not in log_text
    assert "private assistant response" not in log_text
    assert service.metrics.snapshot().events_by_name["UserTextReceived"] == 1
    assert service.metrics.snapshot().events_by_name["AssistantTextReady"] == 1


def test_event_replay_recorder_applies_retention() -> None:
    recorder = EventReplayRecorder(max_records=2)

    recorder.record(AppStarted(app_name="one"))
    recorder.record(AppStarted(app_name="two"))
    recorder.record(AppStarted(app_name="three"))

    records = recorder.replay()

    assert len(records) == 2
    assert [record.fields["app_name"] for record in records] == ["two", "three"]


def test_health_check_service_reports_overall_status() -> None:
    health = HealthCheckService(
        checks=(
            ComponentHealthCheck(
                component_id="runtime",
                check=lambda: pass_check("runtime", "ok"),
            ),
        )
    )

    report = health.run()

    assert report.status is HealthStatus.PASS
    assert report.checks[0].message == "ok"
