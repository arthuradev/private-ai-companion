from __future__ import annotations


class VisionError(RuntimeError):
    """Base error for screen context and vision failures."""


class ScreenCaptureDeniedError(VisionError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class ScreenCaptureUnavailableError(VisionError):
    """Raised when the configured capture provider cannot capture a screen."""
