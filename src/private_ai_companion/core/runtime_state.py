from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import ClassVar

from private_ai_companion.core.errors import LifecycleError


class RuntimePhase(StrEnum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class RuntimeState:
    phase: RuntimePhase = RuntimePhase.CREATED
    started_at: datetime | None = None
    stopped_at: datetime | None = None
    failure_reason: str | None = None


class RuntimeStateStore:
    _ALLOWED_TRANSITIONS: ClassVar[dict[RuntimePhase, set[RuntimePhase]]] = {
        RuntimePhase.CREATED: {RuntimePhase.STARTING, RuntimePhase.STOPPED},
        RuntimePhase.STARTING: {RuntimePhase.RUNNING, RuntimePhase.FAILED},
        RuntimePhase.RUNNING: {RuntimePhase.STOPPING, RuntimePhase.FAILED},
        RuntimePhase.STOPPING: {RuntimePhase.STOPPED, RuntimePhase.FAILED},
        RuntimePhase.STOPPED: set(),
        RuntimePhase.FAILED: set(),
    }

    def __init__(self) -> None:
        self._state = RuntimeState()

    @property
    def current(self) -> RuntimeState:
        return self._state

    def transition_to(
        self,
        phase: RuntimePhase,
        *,
        failure_reason: str | None = None,
    ) -> RuntimeState:
        current_phase = self._state.phase
        if phase not in self._ALLOWED_TRANSITIONS[current_phase]:
            msg = f"cannot transition runtime from {current_phase} to {phase}"
            raise LifecycleError(msg)

        now = datetime.now(UTC)
        started_at = self._state.started_at
        stopped_at = self._state.stopped_at

        if phase is RuntimePhase.RUNNING and started_at is None:
            started_at = now
        if phase in {RuntimePhase.STOPPED, RuntimePhase.FAILED}:
            stopped_at = now

        self._state = replace(
            self._state,
            phase=phase,
            started_at=started_at,
            stopped_at=stopped_at,
            failure_reason=failure_reason,
        )
        return self._state
