from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.speech import SpeechInputAudio, VoiceActivityResult


@dataclass(frozen=True, slots=True)
class EnergyVoiceActivityDetector:
    threshold: float = 0.01

    async def detect(self, audio: SpeechInputAudio) -> VoiceActivityResult:
        data = self._read_audio_bytes(audio)
        if not data:
            return VoiceActivityResult(
                has_voice=False,
                speech_ratio=0.0,
                reason="empty_audio",
            )

        active_bytes = sum(1 for value in data if value not in (0, 128))
        speech_ratio = active_bytes / len(data)
        has_voice = speech_ratio >= self.threshold
        return VoiceActivityResult(
            has_voice=has_voice,
            speech_ratio=speech_ratio,
            reason="voice_detected" if has_voice else "no_voice_detected",
        )

    @staticmethod
    def _read_audio_bytes(audio: SpeechInputAudio) -> bytes:
        if audio.content is not None:
            return audio.content
        if audio.path is not None:
            return audio.path.read_bytes()
        return b""
