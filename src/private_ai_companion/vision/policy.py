from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.vision.models import (
    ScreenCaptureDecisionStatus,
    ScreenCaptureMode,
    ScreenCapturePolicyDecision,
    ScreenCaptureRequest,
)


@dataclass(frozen=True, slots=True)
class ScreenCapturePolicy:
    enabled: bool = True
    require_user_authorization: bool = True
    allow_continuous_capture: bool = False
    persist_screenshots_by_default: bool = False
    allow_external_analysis: bool = False

    def evaluate(self, request: ScreenCaptureRequest) -> ScreenCapturePolicyDecision:
        if not self.enabled:
            return self._deny(request, "screen_capture_disabled")

        if request.mode is ScreenCaptureMode.CONTINUOUS and not (
            self.allow_continuous_capture
        ):
            return self._deny(request, "continuous_capture_disabled")

        if self.require_user_authorization and not request.user_authorized:
            return self._deny(request, "user_authorization_required")

        if request.allow_persistence and not self.persist_screenshots_by_default:
            return self._deny(request, "screenshot_persistence_disabled")

        if request.allow_external_analysis and not self.allow_external_analysis:
            return self._deny(request, "external_vision_analysis_disabled")

        return ScreenCapturePolicyDecision(
            request_id=request.request_id,
            status=ScreenCaptureDecisionStatus.ALLOWED,
            reason="allowed",
            allow_persistence=(
                request.allow_persistence and self.persist_screenshots_by_default
            ),
            allow_external_analysis=(
                request.allow_external_analysis and self.allow_external_analysis
            ),
        )

    @staticmethod
    def _deny(
        request: ScreenCaptureRequest,
        reason: str,
    ) -> ScreenCapturePolicyDecision:
        return ScreenCapturePolicyDecision(
            request_id=request.request_id,
            status=ScreenCaptureDecisionStatus.DENIED,
            reason=reason,
        )
