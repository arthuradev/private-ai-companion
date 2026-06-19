from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.desktop import DesktopActionRequest, DesktopActionService
from private_ai_companion.skills import (
    SkillEffectKind,
    SkillEffectRequest,
    SkillEffectResult,
    SkillRequest,
)


@dataclass(frozen=True, slots=True)
class DesktopSkillEffectExecutor:
    desktop_actions: DesktopActionService

    async def execute_effect(
        self,
        request: SkillRequest,
        effect: SkillEffectRequest,
    ) -> SkillEffectResult:
        if effect.kind is not SkillEffectKind.DESKTOP_ACTION:
            return SkillEffectResult(
                kind=effect.kind,
                status="denied",
                message="unsupported_skill_effect",
            )

        result = await self.desktop_actions.perform(
            DesktopActionRequest(
                action_type=effect.action_type,
                parameters=dict(effect.parameters),
                source=f"skill:{request.skill_id}",
                user_confirmed=effect.user_confirmed,
                dry_run_only=effect.dry_run_only,
            )
        )
        return SkillEffectResult(
            kind=effect.kind,
            status=result.status.value,
            message=result.message,
            output=result.output,
        )
