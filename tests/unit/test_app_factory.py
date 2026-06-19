from __future__ import annotations

import asyncio

from private_ai_companion.bootstrap import Application, create_application
from private_ai_companion.core import RuntimePhase


def test_create_application_wires_core_runtime() -> None:
    application = create_application(name="test-app", version="0.0.0")

    assert isinstance(application, Application)
    assert application.orchestrator.state.phase is RuntimePhase.CREATED
    assert application.llm_router.provider_ids == ("fake-local",)

    snapshot = asyncio.run(application.run_once())

    assert snapshot.state.phase is RuntimePhase.STOPPED
