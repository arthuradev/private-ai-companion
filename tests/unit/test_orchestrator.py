from __future__ import annotations

import asyncio

from private_ai_companion.core import (
    ApplicationIdentity,
    CoreOrchestrator,
    EventBus,
    RuntimePhase,
    RuntimeStateStore,
)


def test_orchestrator_run_once_starts_and_stops_runtime() -> None:
    orchestrator = CoreOrchestrator(
        event_bus=EventBus(),
        state_store=RuntimeStateStore(),
        identity=ApplicationIdentity(name="test-app", version="0.0.0"),
    )

    snapshot = asyncio.run(orchestrator.run_once())

    assert snapshot.state.phase is RuntimePhase.STOPPED
    assert snapshot.state.started_at is not None
    assert snapshot.state.stopped_at is not None
