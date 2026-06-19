from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.lifecycle import ApplicationIdentity, LifecycleManager
from private_ai_companion.core.runtime_state import RuntimeState, RuntimeStateStore


@dataclass(frozen=True, slots=True)
class RuntimeSnapshot:
    state: RuntimeState


class CoreOrchestrator:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        state_store: RuntimeStateStore,
        identity: ApplicationIdentity,
    ) -> None:
        self.event_bus = event_bus
        self._state_store = state_store
        self._lifecycle = LifecycleManager(
            event_bus=event_bus,
            state_store=state_store,
            identity=identity,
        )

    @property
    def state(self) -> RuntimeState:
        return self._state_store.current

    async def start(self) -> RuntimeSnapshot:
        await self._lifecycle.start()
        return RuntimeSnapshot(state=self.state)

    async def stop(self, *, reason: str = "shutdown_requested") -> RuntimeSnapshot:
        await self._lifecycle.stop(reason=reason)
        return RuntimeSnapshot(state=self.state)

    async def run_once(self) -> RuntimeSnapshot:
        await self.start()
        return await self.stop(reason="run_once_complete")
