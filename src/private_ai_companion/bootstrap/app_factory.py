from __future__ import annotations

from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.adapters.llm import FakeLLMProvider
from private_ai_companion.adapters.speech import FakeAudioPlayer, FakeTTSProvider
from private_ai_companion.bootstrap.application import Application
from private_ai_companion.brain import LLMProvider, LLMProviderKind, LLMRouter
from private_ai_companion.config import (
    ConfigError,
    LLMProviderConfig,
    SpeechConfig,
    load_persona_profile,
    load_providers_config,
    load_speech_config,
)
from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.lifecycle import ApplicationIdentity
from private_ai_companion.core.orchestrator import CoreOrchestrator
from private_ai_companion.core.runtime_state import RuntimeStateStore
from private_ai_companion.interaction import TextInteractionService
from private_ai_companion.speech import (
    AudioPlayer,
    SpeechAudioFormat,
    SpeechQueueService,
    TTSProvider,
)


def create_application(
    *,
    name: str = PROJECT_NAME,
    version: str = __version__,
    persona_config_path: Path | None = None,
    providers_config_path: Path | None = None,
    speech_config_path: Path | None = None,
) -> Application:
    event_bus = EventBus()
    state_store = RuntimeStateStore()
    persona = load_persona_profile(persona_config_path)
    providers_config = load_providers_config(providers_config_path)
    speech_config = load_speech_config(speech_config_path)
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
    speech_queue = SpeechQueueService(
        event_bus=event_bus,
        tts_provider=_build_tts_provider(speech_config),
        audio_player=_build_audio_player(speech_config),
    )
    return Application(
        orchestrator=orchestrator,
        text_interaction=text_interaction,
        persona=persona,
        llm_router=llm_router,
        speech_queue=speech_queue,
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


def _build_tts_provider(speech_config: SpeechConfig) -> TTSProvider:
    if speech_config.tts.provider_id != "fake-tts":
        raise ConfigError(
            "Only fake TTS is executable in Phase 07; "
            f"provider {speech_config.tts.provider_id!r} is planned but not implemented"
        )

    return FakeTTSProvider(
        provider_id=speech_config.tts.provider_id,
        audio_format=SpeechAudioFormat(speech_config.tts.audio_format),
    )


def _build_audio_player(speech_config: SpeechConfig) -> AudioPlayer:
    _ = speech_config
    return FakeAudioPlayer()
