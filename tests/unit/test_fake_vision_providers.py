from __future__ import annotations

import asyncio

from private_ai_companion.adapters.vision import (
    FakeScreenCaptureProvider,
    FakeVisionProvider,
)
from private_ai_companion.vision import (
    ScreenCaptureRequest,
    ScreenCaptureSource,
    VisionAnalysisRequest,
    VisionAnalysisStatus,
)


def test_fake_screen_capture_provider_returns_temporary_image() -> None:
    provider = FakeScreenCaptureProvider(visible_text="hello screen")
    request = ScreenCaptureRequest(purpose="test", user_authorized=True)

    screenshot = asyncio.run(provider.capture(request))

    assert screenshot.request_id == request.request_id
    assert screenshot.content.startswith(b"\x89PNG")
    assert screenshot.image_format == "image/png"
    assert screenshot.persist is False
    assert screenshot.source is ScreenCaptureSource.FAKE
    assert screenshot.metadata["visible_text"] == "hello screen"


def test_fake_vision_provider_returns_local_analysis() -> None:
    capture_provider = FakeScreenCaptureProvider()
    vision_provider = FakeVisionProvider()
    request = ScreenCaptureRequest(purpose="test", user_authorized=True)
    screenshot = asyncio.run(capture_provider.capture(request))

    result = asyncio.run(
        vision_provider.analyze(
            VisionAnalysisRequest(
                screenshot=screenshot,
                visible_text="redacted visible text",
            )
        )
    )

    assert result.provider_id == "fake-vision"
    assert result.status is VisionAnalysisStatus.READY
    assert "nenhuma imagem foi enviada" in result.summary
    assert result.visible_text == "redacted visible text"
