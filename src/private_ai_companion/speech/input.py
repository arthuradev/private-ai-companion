from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from private_ai_companion.core import (
    EventBus,
    EventMetadata,
    EventSensitivity,
    UserSpeechReceived,
    VoiceInputFinished,
    VoiceInputIgnored,
    VoiceInputStarted,
)
from private_ai_companion.speech.errors import VoiceInputError
from private_ai_companion.speech.models import (
    SpeechInputAudio,
    SpeechInputMode,
    SpeechInputStatus,
    STTRequest,
    VoiceActivityResult,
    VoiceInputResult,
)
from private_ai_companion.speech.ports import STTProvider, VoiceActivityDetector


@dataclass(frozen=True, slots=True)
class VoiceInputSettings:
    language: str | None
    default_mode: SpeechInputMode
    vad_enabled: bool
    enabled: bool


class VoiceInputService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        stt_provider: STTProvider,
        voice_activity_detector: VoiceActivityDetector,
        settings: VoiceInputSettings,
    ) -> None:
        self._event_bus = event_bus
        self._stt_provider = stt_provider
        self._voice_activity_detector = voice_activity_detector
        self._settings = settings

    async def process_clip(
        self,
        audio: SpeechInputAudio,
        *,
        mode: SpeechInputMode | None = None,
    ) -> VoiceInputResult:
        self._validate_audio(audio)
        request_id = str(uuid4())
        input_mode = mode or self._settings.default_mode
        await self._event_bus.publish(
            VoiceInputStarted(
                mode=input_mode.value,
                metadata=EventMetadata(source="speech"),
            )
        )

        if not self._settings.enabled:
            return await self._ignore(
                request_id=request_id,
                mode=input_mode,
                reason="stt_disabled",
                voice_activity=None,
                duration_seconds=audio.duration_seconds,
            )

        voice_activity: VoiceActivityResult | None = None
        if self._settings.vad_enabled or input_mode is SpeechInputMode.VAD:
            voice_activity = await self._voice_activity_detector.detect(audio)
            if not voice_activity.has_voice:
                return await self._ignore(
                    request_id=request_id,
                    mode=input_mode,
                    reason=voice_activity.reason,
                    voice_activity=voice_activity,
                    duration_seconds=audio.duration_seconds,
                )

        transcript = await self._stt_provider.transcribe(
            STTRequest(
                audio=audio,
                language=self._settings.language,
                request_id=request_id,
            )
        )
        if not transcript.text.strip():
            return await self._ignore(
                request_id=request_id,
                mode=input_mode,
                reason="empty_transcript",
                voice_activity=voice_activity,
                duration_seconds=transcript.duration_seconds,
            )

        await self._event_bus.publish(
            UserSpeechReceived(
                text=transcript.text,
                language=transcript.language,
                confidence=transcript.confidence,
                metadata=EventMetadata(
                    source="speech",
                    sensitivity=EventSensitivity.PRIVATE,
                ),
            )
        )
        result = VoiceInputResult(
            request_id=request_id,
            mode=input_mode,
            status=SpeechInputStatus.TRANSCRIBED,
            transcript=transcript,
            voice_activity=voice_activity,
        )
        await self._finish(
            result=result,
            duration_seconds=transcript.duration_seconds,
        )
        return result

    async def _ignore(
        self,
        *,
        request_id: str,
        mode: SpeechInputMode,
        reason: str,
        voice_activity: VoiceActivityResult | None,
        duration_seconds: float | None,
    ) -> VoiceInputResult:
        result = VoiceInputResult(
            request_id=request_id,
            mode=mode,
            status=SpeechInputStatus.IGNORED,
            voice_activity=voice_activity,
            ignored_reason=reason,
        )
        await self._event_bus.publish(
            VoiceInputIgnored(
                reason=reason,
                metadata=EventMetadata(source="speech"),
            )
        )
        await self._finish(result=result, duration_seconds=duration_seconds)
        return result

    async def _finish(
        self,
        *,
        result: VoiceInputResult,
        duration_seconds: float | None,
    ) -> None:
        await self._event_bus.publish(
            VoiceInputFinished(
                status=result.status.value,
                transcript_id=(
                    result.transcript.transcript_id
                    if result.transcript is not None
                    else None
                ),
                duration_seconds=duration_seconds,
                metadata=EventMetadata(source="speech"),
            )
        )

    @staticmethod
    def _validate_audio(audio: SpeechInputAudio) -> None:
        if audio.content is None and audio.path is None:
            raise VoiceInputError("voice input requires explicit audio content or path")
        if audio.path is not None and not audio.path.exists():
            raise VoiceInputError(f"voice input file not found: {audio.path}")
