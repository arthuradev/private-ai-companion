from __future__ import annotations

import asyncio

import pytest

from private_ai_companion.adapters.vision import (
    FakeScreenCaptureProvider,
    FakeVisionProvider,
)
from private_ai_companion.core import (
    BaseEvent,
    EventBus,
    ScreenContextCaptured,
    ScreenContextDenied,
    ScreenContextRedacted,
    ScreenContextRequested,
    VisionAnalysisReady,
)
from private_ai_companion.vision import (
    MetadataTextRedactor,
    ScreenCaptureDeniedError,
    ScreenCapturePolicy,
    ScreenCaptureRequest,
    VisionService,
)


def test_vision_service_creates_temporary_screen_context() -> None:
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

    context = asyncio.run(
        service.request_screen_context(
            ScreenCaptureRequest(purpose="manual", user_authorized=True)
        )
    )

    assert context.provider_id == "fake-vision"
    assert context.transient is True
    assert context.redacted is True
    assert "person@example.com" not in context.visible_text
    assert [type(event) for event in events] == [
        ScreenContextRequested,
        ScreenContextCaptured,
        ScreenContextRedacted,
        VisionAnalysisReady,
    ]


def test_vision_service_denies_unauthorized_capture() -> None:
    events: list[BaseEvent] = []
    event_bus = EventBus()
    event_bus.subscribe(BaseEvent, events.append)
    service = VisionService(
        event_bus=event_bus,
        capture_provider=FakeScreenCaptureProvider(),
        redactor=MetadataTextRedactor(),
        vision_provider=FakeVisionProvider(),
        policy=ScreenCapturePolicy(),
    )

    with pytest.raises(ScreenCaptureDeniedError, match="user_authorization_required"):
        asyncio.run(
            service.request_screen_context(ScreenCaptureRequest(purpose="manual"))
        )

    assert [type(event) for event in events] == [
        ScreenContextRequested,
        ScreenContextDenied,
    ]
