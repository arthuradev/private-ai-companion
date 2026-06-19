from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from private_ai_companion.speech import SpeechAudio, SpeechAudioFormat, TTSRequest


@dataclass(frozen=True, slots=True)
class FakeTTSProvider:
    provider_id: str = "fake-tts"
    audio_format: SpeechAudioFormat = SpeechAudioFormat.TEXT

    async def synthesize(self, request: TTSRequest) -> SpeechAudio:
        content = f"[fake-tts:{request.voice_id or 'default'}] {request.text}".encode()
        return SpeechAudio(
            audio_id=str(uuid4()),
            request_id=request.request_id,
            content=content,
            audio_format=self.audio_format,
            duration_seconds=max(0.1, len(request.text.split()) * 0.15),
        )
