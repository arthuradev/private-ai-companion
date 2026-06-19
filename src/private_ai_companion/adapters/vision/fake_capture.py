from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from private_ai_companion.vision import (
    ScreenCaptureRequest,
    ScreenCaptureSource,
    ScreenshotImage,
)

FAKE_SCREENSHOT_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00"
    b"\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
)


@dataclass(frozen=True, slots=True)
class FakeScreenCaptureProvider:
    provider_id: str = "fake-screen-capture"
    visible_text: str = "Private AI Companion fake screen context"

    async def capture(self, request: ScreenCaptureRequest) -> ScreenshotImage:
        return ScreenshotImage(
            screenshot_id=str(uuid4()),
            request_id=request.request_id,
            content=FAKE_SCREENSHOT_PNG,
            image_format="image/png",
            width=1,
            height=1,
            source=ScreenCaptureSource.FAKE,
            persist=False,
            metadata={
                "capture_provider_id": self.provider_id,
                "visible_text": self.visible_text,
            },
        )
