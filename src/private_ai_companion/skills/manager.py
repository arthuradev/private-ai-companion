from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core import (
    EventBus,
    EventMetadata,
    EventSensitivity,
    SkillCompleted,
    SkillDenied,
    SkillInvoked,
)
from private_ai_companion.skills.errors import SkillRegistryError
from private_ai_companion.skills.models import (
    SkillEffectKind,
    SkillEffectRequest,
    SkillEffectResult,
    SkillRequest,
    SkillRunResult,
    SkillRunStatus,
)
from private_ai_companion.skills.ports import SkillEffectExecutor
from private_ai_companion.skills.registry import SkillRegistry


@dataclass(frozen=True, slots=True)
class SkillPolicy:
    enabled: bool
    enabled_skill_ids: tuple[str, ...]
    permissions_by_skill_id: dict[str, tuple[str, ...]]
    allowed_actions_by_skill_id: dict[str, tuple[str, ...]]

    def allows_skill(self, skill_id: str) -> bool:
        return self.enabled and skill_id in self.enabled_skill_ids

    def allowed_permissions(self, skill_id: str) -> tuple[str, ...]:
        return self.permissions_by_skill_id.get(skill_id, ())

    def allowed_actions(self, skill_id: str) -> tuple[str, ...]:
        return self.allowed_actions_by_skill_id.get(skill_id, ())


@dataclass(slots=True)
class SkillManager:
    event_bus: EventBus
    registry: SkillRegistry
    policy: SkillPolicy
    effect_executor: SkillEffectExecutor

    @property
    def skill_ids(self) -> tuple[str, ...]:
        return tuple(manifest.skill_id for manifest in self.registry.list_manifests())

    async def run(self, request: SkillRequest) -> SkillRunResult:
        await self.event_bus.publish(
            SkillInvoked(
                skill_id=request.skill_id,
                request_id=request.request_id,
                source=request.source,
                metadata=_skill_event_metadata(),
            )
        )

        if not self.policy.allows_skill(request.skill_id):
            return await self._deny(request, "skill_disabled")

        try:
            skill = self.registry.get(request.skill_id)
        except SkillRegistryError:
            return await self._deny(request, "skill_not_registered")
        manifest = skill.manifest
        missing_permissions = sorted(
            set(manifest.permissions)
            - set(self.policy.allowed_permissions(request.skill_id))
        )
        if missing_permissions:
            return await self._deny(request, "skill_permission_not_granted")

        invocation = await skill.invoke(request)
        if invocation.status is not SkillRunStatus.COMPLETED:
            result = SkillRunResult(
                skill_id=request.skill_id,
                request_id=request.request_id,
                status=invocation.status,
                message=invocation.message,
                output=invocation.output,
            )
            await self._publish_completed(result)
            return result

        denied_action = self._first_denied_effect(request, invocation.effects)
        if denied_action is not None:
            return await self._deny(
                request, f"skill_action_not_allowed:{denied_action}"
            )

        effect_results: list[SkillEffectResult] = []
        for effect in invocation.effects:
            effect_results.append(
                await self.effect_executor.execute_effect(request, effect)
            )

        status = _combine_status(invocation.status, tuple(effect_results))
        result = SkillRunResult(
            skill_id=request.skill_id,
            request_id=request.request_id,
            status=status,
            message=invocation.message,
            output=invocation.output,
            effects=tuple(effect_results),
        )
        await self._publish_completed(result)
        return result

    def _first_denied_effect(
        self,
        request: SkillRequest,
        effects: tuple[SkillEffectRequest, ...],
    ) -> str | None:
        allowed_actions = set(self.policy.allowed_actions(request.skill_id))
        for effect in effects:
            if effect.kind is not SkillEffectKind.DESKTOP_ACTION:
                return effect.kind.value
            if effect.action_type not in allowed_actions:
                return effect.action_type
        return None

    async def _deny(self, request: SkillRequest, reason: str) -> SkillRunResult:
        await self.event_bus.publish(
            SkillDenied(
                skill_id=request.skill_id,
                request_id=request.request_id,
                reason=reason,
                metadata=_skill_event_metadata(),
            )
        )
        result = SkillRunResult(
            skill_id=request.skill_id,
            request_id=request.request_id,
            status=SkillRunStatus.DENIED,
            message=reason,
        )
        await self._publish_completed(result)
        return result

    async def _publish_completed(self, result: SkillRunResult) -> None:
        await self.event_bus.publish(
            SkillCompleted(
                skill_id=result.skill_id,
                request_id=result.request_id,
                status=result.status.value,
                effect_count=len(result.effects),
                metadata=_skill_event_metadata(),
            )
        )


def _combine_status(
    invocation_status: SkillRunStatus,
    effects: tuple[SkillEffectResult, ...],
) -> SkillRunStatus:
    if invocation_status is not SkillRunStatus.COMPLETED:
        return invocation_status
    if any(effect.status == SkillRunStatus.DENIED.value for effect in effects):
        return SkillRunStatus.DENIED
    if any(
        effect.status == SkillRunStatus.REQUIRES_CONFIRMATION.value
        for effect in effects
    ):
        return SkillRunStatus.REQUIRES_CONFIRMATION
    if any(effect.status == SkillRunStatus.FAILED.value for effect in effects):
        return SkillRunStatus.FAILED
    return SkillRunStatus.COMPLETED


def _skill_event_metadata() -> EventMetadata:
    return EventMetadata(source="skills", sensitivity=EventSensitivity.INTERNAL)
