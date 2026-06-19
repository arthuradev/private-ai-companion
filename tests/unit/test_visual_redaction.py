from __future__ import annotations

from private_ai_companion.vision import (
    MetadataTextRedactor,
    ScreenCaptureSource,
    ScreenshotImage,
)


def test_metadata_text_redactor_redacts_sensitive_visible_text() -> None:
    screenshot = ScreenshotImage(
        screenshot_id="screenshot-1",
        request_id="request-1",
        content=b"image-bytes",
        image_format="image/png",
        width=1,
        height=1,
        source=ScreenCaptureSource.FAKE,
        metadata={
            "visible_text": "email person@example.com token=abc123",
        },
    )

    result = MetadataTextRedactor().redact(screenshot)

    assert result.redacted is True
    assert result.finding_count == 2
    assert "person@example.com" not in result.visible_text
    assert "abc123" not in result.visible_text
    assert "[redacted-email]" in result.visible_text
    assert "token=[redacted-secret]" in result.visible_text


def test_metadata_text_redactor_can_be_disabled() -> None:
    screenshot = ScreenshotImage(
        screenshot_id="screenshot-1",
        request_id="request-1",
        content=b"image-bytes",
        image_format="image/png",
        width=1,
        height=1,
        source=ScreenCaptureSource.FAKE,
        metadata={"visible_text": "person@example.com"},
    )

    result = MetadataTextRedactor(enabled=False).redact(screenshot)

    assert result.redacted is False
    assert result.visible_text == "person@example.com"
