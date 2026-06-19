from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from private_ai_companion.brain import LLMRouter, PersonaProfile
from private_ai_companion.core.orchestrator import CoreOrchestrator, RuntimeSnapshot
from private_ai_companion.interaction import (
    TextInteractionService,
    TextTurn,
    VoiceInteractionService,
    VoiceTurn,
)
from private_ai_companion.speech import SpeechInputAudio, SpeechQueueService


@dataclass(frozen=True, slots=True)
class Application:
    orchestrator: CoreOrchestrator
    text_interaction: TextInteractionService
    persona: PersonaProfile
    llm_router: LLMRouter
    speech_queue: SpeechQueueService
    voice_interaction: VoiceInteractionService

    async def start(self) -> RuntimeSnapshot:
        return await self.orchestrator.start()

    async def stop(self, *, reason: str = "shutdown_requested") -> RuntimeSnapshot:
        return await self.orchestrator.stop(reason=reason)

    async def run_once(self) -> RuntimeSnapshot:
        return await self.orchestrator.run_once()

    async def handle_user_text(self, text: str) -> TextTurn:
        return await self.text_interaction.handle_user_text(text)

    async def handle_user_voice_clip(self, audio: SpeechInputAudio) -> VoiceTurn:
        return await self.voice_interaction.handle_clip(audio)

    async def handle_user_voice_file(self, path: Path) -> VoiceTurn:
        return await self.handle_user_voice_clip(SpeechInputAudio.from_path(path))
