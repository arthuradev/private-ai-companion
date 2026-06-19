from __future__ import annotations

from private_ai_companion.vision import (
    ScreenCaptureMode,
    ScreenCapturePolicy,
    ScreenCaptureRequest,
)


def test_screen_capture_policy_allows_manual_authorized_capture() -> None:
    policy = ScreenCapturePolicy()
    request = ScreenCaptureRequest(
        purpose="inspect_current_screen",
        user_authorized=True,
    )

    decision = policy.evaluate(request)

    assert decision.allowed is True
    assert decision.allow_persistence is False
    assert decision.allow_external_analysis is False


def test_screen_capture_policy_requires_user_authorization() -> None:
    policy = ScreenCapturePolicy()
    request = ScreenCaptureRequest(purpose="inspect_current_screen")

    decision = policy.evaluate(request)

    assert decision.allowed is False
    assert decision.reason == "user_authorization_required"


def test_screen_capture_policy_rejects_continuous_capture_by_default() -> None:
    policy = ScreenCapturePolicy()
    request = ScreenCaptureRequest(
        purpose="watch_screen",
        mode=ScreenCaptureMode.CONTINUOUS,
        user_authorized=True,
    )

    decision = policy.evaluate(request)

    assert decision.allowed is False
    assert decision.reason == "continuous_capture_disabled"


def test_screen_capture_policy_rejects_persistence_by_default() -> None:
    policy = ScreenCapturePolicy()
    request = ScreenCaptureRequest(
        purpose="save_screen",
        user_authorized=True,
        allow_persistence=True,
    )

    decision = policy.evaluate(request)

    assert decision.allowed is False
    assert decision.reason == "screenshot_persistence_disabled"


def test_screen_capture_policy_rejects_external_analysis_by_default() -> None:
    policy = ScreenCapturePolicy()
    request = ScreenCaptureRequest(
        purpose="external_screen_analysis",
        user_authorized=True,
        allow_external_analysis=True,
    )

    decision = policy.evaluate(request)

    assert decision.allowed is False
    assert decision.reason == "external_vision_analysis_disabled"
