from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core.orchestrator import CoreOrchestrator, RuntimeSnapshot


@dataclass(frozen=True, slots=True)
class Application:
    orchestrator: CoreOrchestrator

    async def run_once(self) -> RuntimeSnapshot:
        return await self.orchestrator.run_once()
