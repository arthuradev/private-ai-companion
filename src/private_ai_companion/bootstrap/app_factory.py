from __future__ import annotations

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.bootstrap.application import Application
from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.lifecycle import ApplicationIdentity
from private_ai_companion.core.orchestrator import CoreOrchestrator
from private_ai_companion.core.runtime_state import RuntimeStateStore
from private_ai_companion.interaction import TextInteractionService


def create_application(
    *,
    name: str = PROJECT_NAME,
    version: str = __version__,
) -> Application:
    event_bus = EventBus()
    state_store = RuntimeStateStore()
    identity = ApplicationIdentity(name=name, version=version)
    orchestrator = CoreOrchestrator(
        event_bus=event_bus,
        state_store=state_store,
        identity=identity,
    )
    text_interaction = TextInteractionService(event_bus=event_bus)
    return Application(orchestrator=orchestrator, text_interaction=text_interaction)
