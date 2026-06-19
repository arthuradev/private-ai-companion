from __future__ import annotations

from dataclasses import dataclass, field

from private_ai_companion.speech import SpeechAudio


def empty_audio_list() -> list[SpeechAudio]:
    return []


@dataclass(slots=True)
class FakeAudioPlayer:
    played_audio: list[SpeechAudio] = field(default_factory=empty_audio_list)
    interrupted: bool = False

    async def play(self, audio: SpeechAudio) -> None:
        self.played_audio.append(audio)

    async def interrupt(self) -> None:
        self.interrupted = True
