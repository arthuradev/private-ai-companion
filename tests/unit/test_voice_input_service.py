from __future__ import annotations

import asyncio

import pytest

from private_ai_companion.adapters.speech import (
    EnergyVoiceActivityDetector,
    FakeSTTProvider,
)
from private_ai_companion.core import BaseEvent, EventBus
from private_ai_companion.speech import (
    SpeechInputAudio,
    SpeechInputAudioFormat,
    SpeechInputMode,
    SpeechInputStatus,
    VoiceInputError,
    VoiceInputService,
    VoiceInputSettings,
)


def test_voice_input_service_transcribes_clip_and_publishes_events() -> None:
    event_bus = EventBus()
    service = VoiceInputService(
        event_bus=event_bus,
        stt_provider=FakeSTTProvider(),
        voice_activity_detector=EnergyVoiceActivityDetector(),
        settings=VoiceInputSettings(
            language="en-US",
            default_mode=SpeechInputMode.PUSH_TO_TALK,
            vad_enabled=True,
            enabled=True,
        ),
    )
    events: list[str] = []

    def record_event(event: BaseEvent) -> None:
        events.append(event.name)

    event_bus.subscribe(BaseEvent, record_event)

    result = asyncio.run(
        service.process_clip(
            SpeechInputAudio(
                audio_format=SpeechInputAudioFormat.TEXT,
                content=b"hello from voice",
                duration_seconds=0.8,
            )
        )
    )

    assert result.status is SpeechInputStatus.TRANSCRIBED
    assert result.transcript is not None
    assert result.transcript.text == "hello from voice"
    assert events == [
        "VoiceInputStarted",
        "UserSpeechReceived",
        "VoiceInputFinished",
    ]


def test_voice_input_service_ignores_clip_without_voice() -> None:
    service = VoiceInputService(
        event_bus=EventBus(),
        stt_provider=FakeSTTProvider(),
        voice_activity_detector=EnergyVoiceActivityDetector(threshold=1.0),
        settings=VoiceInputSettings(
            language="en-US",
            default_mode=SpeechInputMode.VAD,
            vad_enabled=True,
            enabled=True,
        ),
    )

    result = asyncio.run(
        service.process_clip(
            SpeechInputAudio(
                audio_format=SpeechInputAudioFormat.WAV,
                content=b"\x00\x00\x00",
            )
        )
    )

    assert result.status is SpeechInputStatus.IGNORED
    assert result.transcript is None
    assert result.ignored_reason == "no_voice_detected"


def test_voice_input_service_requires_explicit_audio() -> None:
    service = VoiceInputService(
        event_bus=EventBus(),
        stt_provider=FakeSTTProvider(),
        voice_activity_detector=EnergyVoiceActivityDetector(),
        settings=VoiceInputSettings(
            language="en-US",
            default_mode=SpeechInputMode.PUSH_TO_TALK,
            vad_enabled=False,
            enabled=True,
        ),
    )

    with pytest.raises(VoiceInputError):
        asyncio.run(
            service.process_clip(
                SpeechInputAudio(audio_format=SpeechInputAudioFormat.WAV)
            )
        )
