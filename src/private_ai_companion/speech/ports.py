from __future__ import annotations

from typing import Protocol

from private_ai_companion.speech.models import (
    SpeechAudio,
    SpeechInputAudio,
    STTRequest,
    STTResult,
    TTSRequest,
    VoiceActivityResult,
)


class TTSProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable TTS provider id."""
        ...

    async def synthesize(self, request: TTSRequest) -> SpeechAudio:
        """Create audio bytes from text."""
        ...


class STTProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable STT provider id."""
        ...

    async def transcribe(self, request: STTRequest) -> STTResult:
        """Transcribe explicit user speech audio into text."""
        ...


class VoiceActivityDetector(Protocol):
    async def detect(self, audio: SpeechInputAudio) -> VoiceActivityResult:
        """Detect whether an explicit audio clip contains speech."""
        ...


class PushToTalkRecorder(Protocol):
    async def record_once(self) -> SpeechInputAudio:
        """Record one explicit push-to-talk clip."""
        ...


class AudioPlayer(Protocol):
    async def play(self, audio: SpeechAudio) -> None:
        """Play synthesized audio."""
        ...

    async def interrupt(self) -> None:
        """Interrupt active playback."""
        ...
