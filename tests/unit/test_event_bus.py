from __future__ import annotations

import asyncio
from dataclasses import dataclass

import pytest

from private_ai_companion.core import BaseEvent, EventBus
from private_ai_companion.core.errors import EventHandlerError


@dataclass(frozen=True, slots=True)
class ExampleEvent(BaseEvent):
    value: str = "example"


def test_event_bus_dispatches_sync_and_async_handlers_in_order() -> None:
    bus = EventBus()
    received: list[str] = []

    def sync_handler(event: BaseEvent) -> None:
        assert isinstance(event, ExampleEvent)
        received.append(f"sync:{event.value}")

    async def async_handler(event: BaseEvent) -> None:
        assert isinstance(event, ExampleEvent)
        received.append(f"async:{event.value}")

    bus.subscribe(ExampleEvent, sync_handler)
    bus.subscribe(ExampleEvent, async_handler)

    asyncio.run(bus.publish(ExampleEvent(value="hello")))

    assert received == ["sync:hello", "async:hello"]


def test_event_bus_unsubscribe_removes_handler() -> None:
    bus = EventBus()
    received: list[str] = []

    def handler(event: BaseEvent) -> None:
        assert isinstance(event, ExampleEvent)
        received.append(event.value)

    subscription = bus.subscribe(ExampleEvent, handler)
    bus.unsubscribe(subscription)

    asyncio.run(bus.publish(ExampleEvent(value="ignored")))

    assert received == []


def test_event_bus_wraps_handler_errors() -> None:
    bus = EventBus()

    def broken_handler(event: BaseEvent) -> None:
        assert isinstance(event, ExampleEvent)
        raise RuntimeError("boom")

    bus.subscribe(ExampleEvent, broken_handler)

    with pytest.raises(EventHandlerError) as exc_info:
        asyncio.run(bus.publish(ExampleEvent()))

    assert exc_info.value.event_name == "ExampleEvent"
    assert "broken_handler" in exc_info.value.handler_name
