from __future__ import annotations

import asyncio
from dataclasses import fields

from private_ai_companion.adapters.vision import (
    FakeScreenCaptureProvider,
    FakeVisionProvider,
)
from private_ai_companion.core import BaseEvent, EventBus
from private_ai_companion.vision import (
    MetadataTextRedactor,
    ScreenCaptureMode,
    ScreenCapturePolicy,
    ScreenCaptureRequest,
    VisionService,
)


def test_policy_blocks_continuous_capture_even_when_user_authorized() -> None:
    request = ScreenCaptureRequest(
        purpose="watch_screen",
        mode=ScreenCaptureMode.CONTINUOUS,
        user_authorized=True,
    )

    decision = ScreenCapturePolicy().evaluate(request)

    assert decision.allowed is False
    assert decision.reason == "continuous_capture_disabled"


def test_policy_blocks_external_vision_analysis_by_default() -> None:
    request = ScreenCaptureRequest(
        purpose="external",
        user_authorized=True,
        allow_external_analysis=True,
    )

    decision = ScreenCapturePolicy().evaluate(request)

    assert decision.allowed is False
    assert decision.reason == "external_vision_analysis_disabled"


def test_vision_events_do_not_include_screenshot_bytes_or_visible_text() -> None:
    events: list[BaseEvent] = []
    event_bus = EventBus()
    event_bus.subscribe(BaseEvent, events.append)
    service = VisionService(
        event_bus=event_bus,
        capture_provider=FakeScreenCaptureProvider(
            visible_text="email person@example.com"
        ),
        redactor=MetadataTextRedactor(),
        vision_provider=FakeVisionProvider(),
        policy=ScreenCapturePolicy(),
    )

    asyncio.run(
        service.request_screen_context(
            ScreenCaptureRequest(purpose="manual", user_authorized=True)
        )
    )

    event_field_names = {
        field.name for event in events for field in fields(type(event))
    }
    assert "content" not in event_field_names
    assert "visible_text" not in event_field_names
    assert "summary" not in event_field_names
