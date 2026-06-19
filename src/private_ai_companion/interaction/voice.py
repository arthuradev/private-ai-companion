from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.interaction.text import TextInteractionService, TextTurn
from private_ai_companion.speech import (
    SpeechInputAudio,
    SpeechInputStatus,
    VoiceInputResult,
    VoiceInputService,
)


@dataclass(frozen=True, slots=True)
class VoiceTurn:
    voice: VoiceInputResult
    text: TextTurn | None


class VoiceInteractionService:
    def __init__(
        self,
        *,
        voice_input: VoiceInputService,
        text_interaction: TextInteractionService,
    ) -> None:
        self._voice_input = voice_input
        self._text_interaction = text_interaction

    async def handle_clip(self, audio: SpeechInputAudio) -> VoiceTurn:
        voice_result = await self._voice_input.process_clip(audio)
        if (
            voice_result.status is not SpeechInputStatus.TRANSCRIBED
            or voice_result.transcript is None
        ):
            return VoiceTurn(voice=voice_result, text=None)

        text_turn = await self._text_interaction.handle_user_text(
            voice_result.transcript.text
        )
        return VoiceTurn(voice=voice_result, text=text_turn)
