from __future__ import annotations

import asyncio

import pytest

from private_ai_companion.core import (
    AppStarted,
    BaseEvent,
    EventBus,
    RuntimePhase,
    RuntimeStateStore,
)
from private_ai_companion.core.errors import LifecycleError
from private_ai_companion.core.lifecycle import ApplicationIdentity, LifecycleManager


def test_lifecycle_start_and_stop_publish_events_and_update_state() -> None:
    bus = EventBus()
    state_store = RuntimeStateStore()
    lifecycle = LifecycleManager(
        event_bus=bus,
        state_store=state_store,
        identity=ApplicationIdentity(name="test-app", version="0.0.0"),
    )
    received: list[str] = []

    def record_event(event: BaseEvent) -> None:
        received.append(event.name)

    bus.subscribe(BaseEvent, record_event)

    async def run_lifecycle() -> None:
        await lifecycle.start()
        assert state_store.current.phase is RuntimePhase.RUNNING
        await lifecycle.stop(reason="test_complete")

    asyncio.run(run_lifecycle())

    assert received == ["AppStarted", "AppStopping", "AppStopped"]
    assert state_store.current.phase is RuntimePhase.STOPPED
    assert state_store.current.started_at is not None
    assert state_store.current.stopped_at is not None


def test_lifecycle_event_contains_application_identity() -> None:
    bus = EventBus()
    state_store = RuntimeStateStore()
    lifecycle = LifecycleManager(
        event_bus=bus,
        state_store=state_store,
        identity=ApplicationIdentity(name="test-app", version="1.2.3"),
    )
    received: list[AppStarted] = []

    def record_started(event: BaseEvent) -> None:
        assert isinstance(event, AppStarted)
        received.append(event)

    bus.subscribe(AppStarted, record_started)

    asyncio.run(lifecycle.start())

    assert len(received) == 1
    assert received[0].app_name == "test-app"
    assert received[0].version == "1.2.3"


def test_runtime_state_rejects_invalid_transition() -> None:
    state_store = RuntimeStateStore()

    with pytest.raises(LifecycleError):
        state_store.transition_to(RuntimePhase.RUNNING)
