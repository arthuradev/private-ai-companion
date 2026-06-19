from __future__ import annotations

import asyncio
from pathlib import Path

from private_ai_companion.avatar import AvatarExpression, AvatarProviderStatus
from private_ai_companion.bootstrap import Application, create_application
from private_ai_companion.core import RuntimePhase
from private_ai_companion.safety import ActionExecutionStatus
from private_ai_companion.skills import SkillRunStatus


def test_create_application_wires_core_runtime() -> None:
    application = create_application(name="test-app", version="0.0.0")

    assert isinstance(application, Application)
    assert application.orchestrator.state.phase is RuntimePhase.CREATED
    assert application.llm_router.provider_ids == ("fake-local",)
    assert application.speech_queue.pending_count == 0
    assert application.avatar.provider_id == "fake-avatar"
    assert application.vision.capture_provider_id == "fake-screen-capture"
    assert application.vision.vision_provider_id == "fake-vision"
    assert application.desktop_actions.executor_id == "safe-local-desktop"
    assert application.skills.skill_ids == (
        "builtin.status",
        "builtin.local_note",
        "builtin.open_allowed_app",
    )

    snapshot = asyncio.run(application.run_once())

    assert snapshot.state.phase is RuntimePhase.STOPPED


def test_application_handles_explicit_voice_file(tmp_path: Path) -> None:
    voice_file = tmp_path / "voice.txt"
    voice_file.write_text("hello through speech", encoding="utf-8")
    application = create_application(name="test-app", version="0.0.0")

    turn = asyncio.run(application.handle_user_voice_file(voice_file))

    assert turn.voice.transcript is not None
    assert turn.voice.transcript.text == "hello through speech"
    assert turn.text is not None
    assert turn.text.user.text == "hello through speech"


def test_application_applies_avatar_expression() -> None:
    application = create_application(name="test-app", version="0.0.0")

    result = asyncio.run(application.set_avatar_expression(AvatarExpression.HAPPY))

    assert result.status is AvatarProviderStatus.APPLIED
    assert application.avatar.current_expression is AvatarExpression.HAPPY


def test_application_requests_authorized_screen_context() -> None:
    application = create_application(name="test-app", version="0.0.0")

    context = asyncio.run(
        application.request_screen_context(
            purpose="manual_test",
            user_authorized=True,
        )
    )

    assert context.provider_id == "fake-vision"
    assert context.transient is True


def test_application_performs_confirmed_desktop_action() -> None:
    application = create_application(name="test-app", version="0.0.0")

    result = asyncio.run(
        application.perform_desktop_action(
            action_type="desktop.read_active_window_title",
            user_confirmed=True,
        )
    )

    assert result.status is ActionExecutionStatus.EXECUTED
    assert result.output["title"] == "Private AI Companion"


def test_application_runs_status_skill() -> None:
    application = create_application(name="test-app", version="0.0.0")

    result = asyncio.run(application.run_skill(skill_id="builtin.status"))

    assert result.status is SkillRunStatus.COMPLETED
    assert result.output["status"] == "ready"
