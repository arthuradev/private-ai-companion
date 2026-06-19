from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from private_ai_companion.speech import (
    SpeechInputAudio,
    SpeechInputAudioFormat,
    STTRequest,
    STTResult,
    STTSegment,
)


@dataclass(frozen=True, slots=True)
class FakeSTTProvider:
    provider_id: str = "fake-stt"
    fallback_transcript: str = "mensagem de voz fake"

    async def transcribe(self, request: STTRequest) -> STTResult:
        text = self._extract_text(request.audio) or self.fallback_transcript
        duration_seconds = request.audio.duration_seconds or max(
            0.1,
            len(text.split()) * 0.2,
        )
        return STTResult(
            transcript_id=str(uuid4()),
            request_id=request.request_id,
            text=text,
            language=request.language,
            confidence=1.0,
            duration_seconds=duration_seconds,
            segments=(
                STTSegment(
                    segment_id=str(uuid4()),
                    start_seconds=0.0,
                    end_seconds=duration_seconds,
                    text=text,
                    confidence=1.0,
                ),
            ),
        )

    @staticmethod
    def _extract_text(audio: SpeechInputAudio) -> str:
        if audio.audio_format is not SpeechInputAudioFormat.TEXT:
            return ""
        if audio.content is not None:
            return audio.content.decode("utf-8", errors="ignore").strip()
        if audio.path is not None:
            return audio.path.read_text(encoding="utf-8").strip()
        return ""
