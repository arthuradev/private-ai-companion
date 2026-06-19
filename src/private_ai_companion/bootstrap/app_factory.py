from __future__ import annotations

from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.bootstrap.application import Application
from private_ai_companion.brain import ContextBuilder, PromptBuilder
from private_ai_companion.config import load_persona_profile
from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.lifecycle import ApplicationIdentity
from private_ai_companion.core.orchestrator import CoreOrchestrator
from private_ai_companion.core.runtime_state import RuntimeStateStore
from private_ai_companion.interaction import TextInteractionService


def create_application(
    *,
    name: str = PROJECT_NAME,
    version: str = __version__,
    persona_config_path: Path | None = None,
) -> Application:
    event_bus = EventBus()
    state_store = RuntimeStateStore()
    persona = load_persona_profile(persona_config_path)
    identity = ApplicationIdentity(name=name, version=version)
    orchestrator = CoreOrchestrator(
        event_bus=event_bus,
        state_store=state_store,
        identity=identity,
    )
    text_interaction = TextInteractionService(
        event_bus=event_bus,
        persona=persona,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
    )
    return Application(
        orchestrator=orchestrator,
        text_interaction=text_interaction,
        persona=persona,
    )
