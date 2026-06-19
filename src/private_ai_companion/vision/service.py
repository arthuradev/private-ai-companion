from __future__ import annotations

from uuid import uuid4

from private_ai_companion.core import (
    EventBus,
    EventMetadata,
    EventSensitivity,
    ScreenContextCaptured,
    ScreenContextDenied,
    ScreenContextRedacted,
    ScreenContextRequested,
    VisionAnalysisReady,
)
from private_ai_companion.vision.errors import ScreenCaptureDeniedError
from private_ai_companion.vision.models import (
    ScreenCaptureRequest,
    VisionAnalysisRequest,
    VisualContext,
)
from private_ai_companion.vision.policy import ScreenCapturePolicy
from private_ai_companion.vision.ports import (
    ImageRedactor,
    ScreenCaptureProvider,
    VisionProvider,
)


class VisionService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        capture_provider: ScreenCaptureProvider,
        redactor: ImageRedactor,
        vision_provider: VisionProvider,
        policy: ScreenCapturePolicy,
    ) -> None:
        self._event_bus = event_bus
        self._capture_provider = capture_provider
        self._redactor = redactor
        self._vision_provider = vision_provider
        self._policy = policy

    @property
    def capture_provider_id(self) -> str:
        return self._capture_provider.provider_id

    @property
    def vision_provider_id(self) -> str:
        return self._vision_provider.provider_id

    async def request_screen_context(
        self,
        request: ScreenCaptureRequest,
    ) -> VisualContext:
        await self._event_bus.publish(
            ScreenContextRequested(
                request_id=request.request_id,
                mode=request.mode.value,
                purpose=request.purpose,
                metadata=_vision_event_metadata(),
            )
        )
        decision = self._policy.evaluate(request)
        if not decision.allowed:
            await self._event_bus.publish(
                ScreenContextDenied(
                    request_id=request.request_id,
                    reason=decision.reason,
                    metadata=_vision_event_metadata(),
                )
            )
            raise ScreenCaptureDeniedError(decision.reason)

        screenshot = await self._capture_provider.capture(request)
        if decision.allow_persistence != screenshot.persist:
            screenshot = type(screenshot)(
                screenshot_id=screenshot.screenshot_id,
                request_id=screenshot.request_id,
                content=screenshot.content,
                image_format=screenshot.image_format,
                width=screenshot.width,
                height=screenshot.height,
                source=screenshot.source,
                captured_at=screenshot.captured_at,
                persist=decision.allow_persistence,
                metadata=dict(screenshot.metadata),
            )

        await self._event_bus.publish(
            ScreenContextCaptured(
                request_id=request.request_id,
                screenshot_id=screenshot.screenshot_id,
                capture_provider_id=self._capture_provider.provider_id,
                image_format=screenshot.image_format,
                width=screenshot.width,
                height=screenshot.height,
                persisted=screenshot.persist,
                metadata=_vision_event_metadata(),
            )
        )

        redaction = self._redactor.redact(screenshot)
        await self._event_bus.publish(
            ScreenContextRedacted(
                request_id=request.request_id,
                screenshot_id=redaction.screenshot.screenshot_id,
                redacted=redaction.redacted,
                finding_count=redaction.finding_count,
                metadata=_vision_event_metadata(),
            )
        )

        analysis = await self._vision_provider.analyze(
            VisionAnalysisRequest(
                screenshot=redaction.screenshot,
                visible_text=redaction.visible_text,
                allow_external_analysis=decision.allow_external_analysis,
            )
        )
        context = VisualContext(
            context_id=str(uuid4()),
            request_id=request.request_id,
            screenshot_id=redaction.screenshot.screenshot_id,
            provider_id=analysis.provider_id,
            summary=analysis.summary,
            labels=analysis.labels,
            visible_text=analysis.visible_text,
            redacted=redaction.redacted,
        )
        await self._event_bus.publish(
            VisionAnalysisReady(
                request_id=request.request_id,
                context_id=context.context_id,
                vision_provider_id=analysis.provider_id,
                status=analysis.status.value,
                label_count=len(analysis.labels),
                redacted=redaction.redacted,
                metadata=_vision_event_metadata(),
            )
        )
        return context


def _vision_event_metadata() -> EventMetadata:
    return EventMetadata(source="vision", sensitivity=EventSensitivity.SENSITIVE)
