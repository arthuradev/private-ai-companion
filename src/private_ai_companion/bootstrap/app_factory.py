from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.adapters.avatar import (
    FakeAvatarProvider,
    VTubeStudioAvatarProvider,
)
from private_ai_companion.adapters.desktop import SafeLocalDesktopExecutor
from private_ai_companion.adapters.llm import FakeLLMProvider
from private_ai_companion.adapters.speech import (
    EnergyVoiceActivityDetector,
    FakeAudioPlayer,
    FakeSTTProvider,
    FakeTTSProvider,
    FasterWhisperSTTProvider,
)
from private_ai_companion.adapters.vision import (
    FakeScreenCaptureProvider,
    FakeVisionProvider,
)
from private_ai_companion.avatar import (
    AvatarExpression,
    AvatarIdleState,
    AvatarProvider,
    AvatarService,
    AvatarServiceSettings,
)
from private_ai_companion.bootstrap.application import Application
from private_ai_companion.bootstrap.skill_effects import DesktopSkillEffectExecutor
from private_ai_companion.brain import LLMProvider, LLMProviderKind, LLMRouter
from private_ai_companion.config import (
    AvatarConfig,
    ConfigError,
    DesktopConfig,
    LLMProviderConfig,
    PrivacyConfig,
    SkillsConfig,
    SpeechConfig,
    load_avatar_config,
    load_desktop_config,
    load_persona_profile,
    load_privacy_config,
    load_providers_config,
    load_skills_config,
    load_speech_config,
)
from private_ai_companion.core.event_bus import EventBus
from private_ai_companion.core.lifecycle import ApplicationIdentity
from private_ai_companion.core.orchestrator import CoreOrchestrator
from private_ai_companion.core.runtime_state import RuntimeStateStore
from private_ai_companion.desktop import (
    DesktopActionExecutor,
    DesktopActionService,
    DesktopPermissionPolicy,
)
from private_ai_companion.interaction import (
    TextInteractionService,
    VoiceInteractionService,
)
from private_ai_companion.safety import (
    ActionPolicy,
    InMemoryActionAuditLog,
    RiskClassifier,
    RiskLevel,
)
from private_ai_companion.skills import (
    LocalNoteSkill,
    OpenAllowedAppSkill,
    SkillManager,
    SkillPolicy,
    SkillRegistry,
    StatusSkill,
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
from private_ai_companion.vision import (
    MetadataTextRedactor,
    ScreenCapturePolicy,
    ScreenCaptureProvider,
    VisionProvider,
    VisionService,
)


@dataclass(frozen=True, slots=True)
class ApplicationConfigPaths:
    persona: Path | None = None
    providers: Path | None = None
    speech: Path | None = None
    avatar: Path | None = None
    privacy: Path | None = None
    desktop: Path | None = None
    skills: Path | None = None


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
    privacy_config = load_privacy_config(paths.privacy)
    desktop_config = load_desktop_config(paths.desktop)
    skills_config = load_skills_config(paths.skills)
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
    vision = VisionService(
        event_bus=event_bus,
        capture_provider=_build_screen_capture_provider(privacy_config),
        redactor=MetadataTextRedactor(
            enabled=(
                privacy_config.redaction.enabled
                and privacy_config.redaction.redact_text_metadata
            )
        ),
        vision_provider=_build_vision_provider(privacy_config),
        policy=_build_screen_capture_policy(privacy_config),
    )
    desktop_actions = DesktopActionService(
        event_bus=event_bus,
        executor=_build_desktop_action_executor(desktop_config),
        risk_classifier=RiskClassifier(),
        action_policy=_build_action_policy(desktop_config),
        permission_policy=_build_desktop_permission_policy(desktop_config),
        audit_log=InMemoryActionAuditLog(),
    )
    skills = SkillManager(
        event_bus=event_bus,
        registry=_build_skill_registry(),
        policy=_build_skill_policy(skills_config),
        effect_executor=DesktopSkillEffectExecutor(desktop_actions=desktop_actions),
    )
    return Application(
        orchestrator=orchestrator,
        text_interaction=text_interaction,
        persona=persona,
        llm_router=llm_router,
        speech_queue=speech_queue,
        voice_interaction=voice_interaction,
        avatar=avatar,
        vision=vision,
        desktop_actions=desktop_actions,
        skills=skills,
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


def _build_screen_capture_provider(
    privacy_config: PrivacyConfig,
) -> ScreenCaptureProvider:
    if privacy_config.screen_capture.provider_id == "fake-screen-capture":
        return FakeScreenCaptureProvider()

    raise ConfigError(
        "Only fake-screen-capture is executable in Phase 10; "
        f"provider {privacy_config.screen_capture.provider_id!r} is not implemented"
    )


def _build_vision_provider(privacy_config: PrivacyConfig) -> VisionProvider:
    if privacy_config.vision.provider_id == "fake-vision":
        return FakeVisionProvider()

    raise ConfigError(
        "Only fake-vision is executable in Phase 10; "
        f"provider {privacy_config.vision.provider_id!r} is not implemented"
    )


def _build_screen_capture_policy(
    privacy_config: PrivacyConfig,
) -> ScreenCapturePolicy:
    return ScreenCapturePolicy(
        enabled=privacy_config.screen_capture.enabled,
        require_user_authorization=(
            privacy_config.screen_capture.require_user_authorization
        ),
        allow_continuous_capture=privacy_config.screen_capture.allow_continuous_capture,
        persist_screenshots_by_default=(
            privacy_config.screen_capture.persist_screenshots_by_default
        ),
        allow_external_analysis=privacy_config.screen_capture.allow_external_analysis,
    )


def _build_desktop_action_executor(
    desktop_config: DesktopConfig,
) -> DesktopActionExecutor:
    if desktop_config.actions.executor_id == "safe-local-desktop":
        return SafeLocalDesktopExecutor(
            notes_directory=Path(desktop_config.notes.directory),
            allowed_apps=dict(desktop_config.allowed_apps),
            fake_active_window_title=desktop_config.window.fake_active_window_title,
            max_note_bytes=desktop_config.notes.max_note_bytes,
        )

    raise ConfigError(
        "Only safe-local-desktop is executable in Phase 11; "
        f"executor {desktop_config.actions.executor_id!r} is not implemented"
    )


def _build_action_policy(desktop_config: DesktopConfig) -> ActionPolicy:
    allowed_action_types = (
        desktop_config.actions.allowed_action_types
        if desktop_config.actions.enabled
        else ()
    )
    return ActionPolicy(
        allowed_action_types=allowed_action_types,
        require_confirmation_for=tuple(
            RiskLevel(level)
            for level in desktop_config.actions.require_confirmation_for
        ),
        allow_high_risk=desktop_config.actions.allow_high_risk,
        allow_critical_risk=desktop_config.actions.allow_critical_risk,
    )


def _build_desktop_permission_policy(
    desktop_config: DesktopConfig,
) -> DesktopPermissionPolicy:
    allowed_action_types = (
        desktop_config.actions.allowed_action_types
        if desktop_config.actions.enabled
        else ()
    )
    return DesktopPermissionPolicy(
        allowed_action_types=allowed_action_types,
        allowed_app_ids=tuple(desktop_config.allowed_apps),
        notes_enabled=desktop_config.notes.enabled,
        active_window_title_enabled=desktop_config.window.active_window_title_enabled,
    )


def _build_skill_registry() -> SkillRegistry:
    registry = SkillRegistry()
    registry.register(StatusSkill())
    registry.register(LocalNoteSkill())
    registry.register(OpenAllowedAppSkill())
    return registry


def _build_skill_policy(skills_config: SkillsConfig) -> SkillPolicy:
    enabled_skill_ids = tuple(
        skill.skill_id for skill in skills_config.skills if skill.enabled
    )
    permissions_by_skill_id = {
        skill.skill_id: skill.permissions for skill in skills_config.skills
    }
    allowed_actions_by_skill_id = {
        skill.skill_id: skill.allowed_action_types for skill in skills_config.skills
    }
    return SkillPolicy(
        enabled=skills_config.enabled,
        enabled_skill_ids=enabled_skill_ids,
        permissions_by_skill_id=permissions_by_skill_id,
        allowed_actions_by_skill_id=allowed_actions_by_skill_id,
    )
