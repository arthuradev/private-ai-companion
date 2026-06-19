from __future__ import annotations

from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.adapters.llm import FakeLLMProvider
from private_ai_companion.bootstrap.application import Application
from private_ai_companion.brain import LLMProvider, LLMProviderKind, LLMRouter
from private_ai_companion.config import (
    ConfigError,
    LLMProviderConfig,
    load_persona_profile,
    load_providers_config,
)
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
    providers_config_path: Path | None = None,
) -> Application:
    event_bus = EventBus()
    state_store = RuntimeStateStore()
    persona = load_persona_profile(persona_config_path)
    providers_config = load_providers_config(providers_config_path)
    providers = _build_llm_providers(providers_config.llm.enabled_providers)
    llm_router = LLMRouter(
        providers=providers,
        default_provider_id=providers_config.llm.default_provider,
        fallback_provider_ids=providers_config.llm.fallback_order,
    )
    identity = ApplicationIdentity(name=name, version=version)
    orchestrator = CoreOrchestrator(
        event_bus=event_bus,
        state_store=state_store,
        identity=identity,
    )
    text_interaction = TextInteractionService(
        event_bus=event_bus,
        persona=persona,
        llm_router=llm_router,
    )
    return Application(
        orchestrator=orchestrator,
        text_interaction=text_interaction,
        persona=persona,
        llm_router=llm_router,
    )


def _build_llm_providers(
    provider_configs: tuple[LLMProviderConfig, ...],
) -> tuple[LLMProvider, ...]:
    providers: list[LLMProvider] = []
    for provider_config in provider_configs:
        if provider_config.kind is LLMProviderKind.FAKE:
            providers.append(
                FakeLLMProvider(
                    provider_id=provider_config.provider_id,
                    model=provider_config.model,
                )
            )
            continue

        raise ConfigError(
            "Only fake LLM providers are executable in Phase 05; "
            f"provider {provider_config.provider_id!r} is planned but not implemented"
        )

    return tuple(providers)
