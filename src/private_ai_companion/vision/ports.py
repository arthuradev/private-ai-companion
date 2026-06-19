from __future__ import annotations

from typing import Protocol

from private_ai_companion.vision.models import (
    RedactionResult,
    ScreenCaptureRequest,
    ScreenshotImage,
    VisionAnalysisRequest,
    VisionAnalysisResult,
)


class ScreenCaptureProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable screen capture provider id."""
        ...

    async def capture(self, request: ScreenCaptureRequest) -> ScreenshotImage:
        """Capture one explicit screenshot."""
        ...


class ImageRedactor(Protocol):
    def redact(self, screenshot: ScreenshotImage) -> RedactionResult:
        """Return redacted text/metadata derived from a screenshot."""
        ...


class VisionProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable vision provider id."""
        ...

    async def analyze(self, request: VisionAnalysisRequest) -> VisionAnalysisResult:
        """Analyze a temporary screenshot context."""
        ...
