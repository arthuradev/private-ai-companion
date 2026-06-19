from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.events import AppStarted, AppStopped, AppStopping
from private_ai_companion.core.runtime_state import RuntimePhase, RuntimeStateStore


@dataclass(frozen=True, slots=True)
class ApplicationIdentity:
    name: str
    version: str


class LifecycleManager:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        state_store: RuntimeStateStore,
        identity: ApplicationIdentity,
    ) -> None:
        self._event_bus = event_bus
        self._state_store = state_store
        self._identity = identity

    async def start(self) -> None:
        self._state_store.transition_to(RuntimePhase.STARTING)
        await self._event_bus.publish(
            AppStarted(app_name=self._identity.name, version=self._identity.version)
        )
        self._state_store.transition_to(RuntimePhase.RUNNING)

    async def stop(self, *, reason: str = "shutdown_requested") -> None:
        if self._state_store.current.phase is RuntimePhase.CREATED:
            self._state_store.transition_to(RuntimePhase.STOPPED)
            return

        self._state_store.transition_to(RuntimePhase.STOPPING)
        await self._event_bus.publish(AppStopping(reason=reason))
        self._state_store.transition_to(RuntimePhase.STOPPED)
        await self._event_bus.publish(AppStopped(reason=reason))
