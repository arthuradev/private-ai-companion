from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.adapters.avatar import (
    FakeAvatarProvider,
    VTubeStudioAvatarProvider,
)
from private_ai_companion.adapters.llm import FakeLLMProvider
from private_ai_companion.adapters.speech import (
    EnergyVoiceActivityDetector,
    FakeAudioPlayer,
    FakeSTTProvider,
    FakeTTSProvider,
    FasterWhisperSTTProvider,
)
from private_ai_companion.avatar import (
    AvatarExpression,
    AvatarIdleState,
    AvatarProvider,
    AvatarService,
    AvatarServiceSettings,
)
from private_ai_companion.bootstrap.application import Application
from private_ai_companion.brain import LLMProvider, LLMProviderKind, LLMRouter
from private_ai_companion.config import (
    AvatarConfig,
    ConfigError,
    LLMProviderConfig,
    SpeechConfig,
    load_avatar_config,
    load_persona_profile,
    load_providers_config,
    load_speech_config,
)
from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.lifecycle import ApplicationIdentity
from private_ai_companion.core.orchestrator import CoreOrchestrator
from private_ai_companion.core.runtime_state import RuntimeStateStore
from private_ai_companion.interaction import (
    TextInteractionService,
    VoiceInteractionService,
)
from private_ai_companion.speech import (
    AudioPlayer,
    SpeechAudioFormat,
    SpeechInputMode,
    SpeechQueueService,
    STTProvider,
    TTSProvider,
    VoiceActivityDetector,
    VoiceInputService,
    VoiceInputSettings,
)


@dataclass(frozen=True, slots=True)
class ApplicationConfigPaths:
    persona: Path | None = None
    providers: Path | None = None
    speech: Path | None = None
    avatar: Path | None = None


def create_application(
    *,
    name: str = PROJECT_NAME,
    version: str = __version__,
    config_paths: ApplicationConfigPaths | None = None,
) -> Application:
    paths = config_paths or ApplicationConfigPaths()
    event_bus = EventBus()
    state_store = RuntimeStateStore()
    persona = load_persona_profile(paths.persona)
    providers_config = load_providers_config(paths.providers)
    speech_config = load_speech_config(paths.speech)
    avatar_config = load_avatar_config(paths.avatar)
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
    voice_input = VoiceInputService(
        event_bus=event_bus,
        stt_provider=_build_stt_provider(speech_config),
        voice_activity_detector=_build_voice_activity_detector(speech_config),
        settings=VoiceInputSettings(
            language=speech_config.stt.language,
            default_mode=SpeechInputMode(speech_config.input.mode),
            vad_enabled=speech_config.input.vad_enabled,
            enabled=speech_config.stt.enabled,
        ),
    )
    voice_interaction = VoiceInteractionService(
        voice_input=voice_input,
        text_interaction=text_interaction,
    )
    avatar = AvatarService(
        event_bus=event_bus,
        provider=_build_avatar_provider(avatar_config),
        settings=_build_avatar_service_settings(avatar_config),
    )
    return Application(
        orchestrator=orchestrator,
        text_interaction=text_interaction,
        persona=persona,
        llm_router=llm_router,
        speech_queue=speech_queue,
        voice_interaction=voice_interaction,
        avatar=avatar,
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


def _build_stt_provider(speech_config: SpeechConfig) -> STTProvider:
    if speech_config.stt.provider_id == "fake-stt":
        return FakeSTTProvider()

    if speech_config.stt.provider_id == "faster-whisper":
        return FasterWhisperSTTProvider(
            provider_id=speech_config.stt.provider_id,
            model_size=speech_config.stt.model_size,
            device=speech_config.stt.device,
            compute_type=speech_config.stt.compute_type,
            vad_filter=speech_config.stt.vad_filter,
        )

    raise ConfigError(
        "Only fake-stt and faster-whisper STT are executable in Phase 08; "
        f"provider {speech_config.stt.provider_id!r} is not implemented"
    )


def _build_voice_activity_detector(
    speech_config: SpeechConfig,
) -> VoiceActivityDetector:
    return EnergyVoiceActivityDetector(threshold=speech_config.input.vad_threshold)


def _build_avatar_provider(avatar_config: AvatarConfig) -> AvatarProvider:
    if avatar_config.provider_id == "fake-avatar":
        return FakeAvatarProvider()

    if avatar_config.provider_id == "vtube-studio":
        token = os.environ.get(
            avatar_config.vtube_studio.authentication_token_env,
        )
        return VTubeStudioAvatarProvider(
            provider_id=avatar_config.provider_id,
            host=avatar_config.vtube_studio.host,
            port=avatar_config.vtube_studio.port,
            plugin_name=avatar_config.vtube_studio.plugin_name,
            plugin_developer=avatar_config.vtube_studio.plugin_developer,
            authentication_token=token,
            request_token_on_connect=(
                avatar_config.vtube_studio.request_token_on_connect
            ),
            expression_hotkeys={
                AvatarExpression(hotkey.expression): hotkey.hotkey_id
                for hotkey in avatar_config.expression_hotkeys
            },
        )

    raise ConfigError(
        "Only fake-avatar and vtube-studio avatar providers are executable in "
        f"Phase 09; provider {avatar_config.provider_id!r} is not implemented"
    )


def _build_avatar_service_settings(
    avatar_config: AvatarConfig,
) -> AvatarServiceSettings:
    return AvatarServiceSettings(
        enabled=avatar_config.enabled,
        idle=AvatarIdleState(
            enabled=avatar_config.idle.enabled,
            expression=AvatarExpression(avatar_config.idle.expression),
            interval_seconds=avatar_config.idle.interval_seconds,
        ),
        lipsync_parameter_name=avatar_config.lipsync.parameter_name,
        lipsync_weight=avatar_config.lipsync.weight,
    )
