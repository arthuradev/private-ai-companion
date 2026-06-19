from __future__ import annotations

import asyncio
from pathlib import Path

from private_ai_companion.avatar import AvatarExpression, AvatarProviderStatus
from private_ai_companion.bootstrap import Application, create_application
from private_ai_companion.core import RuntimePhase


def test_create_application_wires_core_runtime() -> None:
    application = create_application(name="test-app", version="0.0.0")

    assert isinstance(application, Application)
    assert application.orchestrator.state.phase is RuntimePhase.CREATED
    assert application.llm_router.provider_ids == ("fake-local",)
    assert application.speech_queue.pending_count == 0
    assert application.avatar.provider_id == "fake-avatar"

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
