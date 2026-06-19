from __future__ import annotations

from typing import Protocol

from private_ai_companion.speech.models import SpeechAudio, TTSRequest


class TTSProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable TTS provider id."""
        ...

    async def synthesize(self, request: TTSRequest) -> SpeechAudio:
        """Create audio bytes from text."""
        ...


class AudioPlayer(Protocol):
    async def play(self, audio: SpeechAudio) -> None:
        """Play synthesized audio."""
        ...

    async def interrupt(self) -> None:
        """Interrupt active playback."""
        ...
