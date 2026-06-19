from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core.orchestrator import CoreOrchestrator, RuntimeSnapshot
from private_ai_companion.interaction import TextInteractionService, TextTurn


@dataclass(frozen=True, slots=True)
class Application:
    orchestrator: CoreOrchestrator
    text_interaction: TextInteractionService

    async def start(self) -> RuntimeSnapshot:
        return await self.orchestrator.start()

    async def stop(self, *, reason: str = "shutdown_requested") -> RuntimeSnapshot:
        return await self.orchestrator.stop(reason=reason)

    async def run_once(self) -> RuntimeSnapshot:
        return await self.orchestrator.run_once()

    async def handle_user_text(self, text: str) -> TextTurn:
        return await self.text_interaction.handle_user_text(text)
