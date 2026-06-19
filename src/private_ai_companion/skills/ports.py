from __future__ import annotations

from typing import Protocol

from private_ai_companion.skills.models import (
    SkillEffectRequest,
    SkillEffectResult,
    SkillInvocation,
    SkillManifest,
    SkillRequest,
)


class BaseSkill(Protocol):
    @property
    def manifest(self) -> SkillManifest:
        """Static manifest describing permissions and allowed actions."""
        ...

    async def invoke(self, request: SkillRequest) -> SkillInvocation:
        """Produce a skill result or typed effects without executing unsafe work."""
        ...


class SkillEffectExecutor(Protocol):
    async def execute_effect(
        self,
        request: SkillRequest,
        effect: SkillEffectRequest,
    ) -> SkillEffectResult:
        """Execute one manager-approved skill effect."""
        ...
