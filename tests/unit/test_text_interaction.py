from __future__ import annotations

import asyncio

from private_ai_companion.core import (
    AssistantTextReady,
    BaseEvent,
    EventBus,
    EventSensitivity,
    UserTextReceived,
)
from private_ai_companion.interaction import TextInteractionService


def test_text_interaction_publishes_user_and_assistant_events() -> None:
    bus = EventBus()
    service = TextInteractionService(event_bus=bus)
    received: list[BaseEvent] = []

    def record_event(event: BaseEvent) -> None:
        received.append(event)

    bus.subscribe(BaseEvent, record_event)

    turn = asyncio.run(service.handle_user_text(" hello "))

    assert turn.user.text == "hello"
    assert "LLM configuravel" in turn.assistant.text
    assert [event.name for event in received] == [
        "UserTextReceived",
        "AssistantTextReady",
    ]

    user_event = received[0]
    assistant_event = received[1]
    assert isinstance(user_event, UserTextReceived)
    assert user_event.text == "hello"
    assert user_event.metadata.sensitivity is EventSensitivity.PRIVATE
    assert isinstance(assistant_event, AssistantTextReady)
    assert assistant_event.metadata.sensitivity is EventSensitivity.INTERNAL


def test_text_interaction_handles_empty_text_without_persistence() -> None:
    service = TextInteractionService(event_bus=EventBus())

    turn = asyncio.run(service.handle_user_text("   "))

    assert turn.user.text == ""
    assert "Nao recebi texto" in turn.assistant.text
