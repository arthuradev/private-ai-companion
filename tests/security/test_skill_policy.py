from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from private_ai_companion.adapters.desktop import SafeLocalDesktopExecutor
from private_ai_companion.bootstrap.skill_effects import DesktopSkillEffectExecutor
from private_ai_companion.core import EventBus
from private_ai_companion.desktop import (
    DesktopActionService,
    DesktopPermissionPolicy,
)
from private_ai_companion.safety import (
    ActionPolicy,
    InMemoryActionAuditLog,
    RiskClassifier,
)
from private_ai_companion.skills import (
    BaseSkill,
    SkillEffectKind,
    SkillEffectRequest,
    SkillInvocation,
    SkillManager,
    SkillManifest,
    SkillPolicy,
    SkillRegistry,
    SkillRequest,
    SkillRunStatus,
)


@dataclass(frozen=True, slots=True)
class CriticalActionSkill:
    @property
    def manifest(self) -> SkillManifest:
        return SkillManifest(
            skill_id="test.critical_action",
            name="Critical action",
            description="Attempts to request shell through a skill effect.",
            version="0.1.0",
            permissions=("desktop.action",),
            allowed_action_types=("system.run_shell",),
        )

    async def invoke(self, request: SkillRequest) -> SkillInvocation:
        return SkillInvocation(
            status=SkillRunStatus.COMPLETED,
            message="critical_requested",
            effects=(
                SkillEffectRequest(
                    kind=SkillEffectKind.DESKTOP_ACTION,
                    action_type="system.run_shell",
                    parameters={"command": "echo unsafe"},
                    user_confirmed=request.user_confirmed,
                ),
            ),
        )


def test_skill_effects_are_still_blocked_by_desktop_safety(tmp_path: Path) -> None:
    registry = SkillRegistry()
    skill: BaseSkill = CriticalActionSkill()
    registry.register(skill)
    desktop_actions = DesktopActionService(
        event_bus=EventBus(),
        executor=SafeLocalDesktopExecutor(notes_directory=tmp_path, allowed_apps={}),
        risk_classifier=RiskClassifier(),
        action_policy=ActionPolicy(allowed_action_types=("system.run_shell",)),
        permission_policy=DesktopPermissionPolicy(
            allowed_action_types=("system.run_shell",),
        ),
        audit_log=InMemoryActionAuditLog(),
    )
    manager = SkillManager(
        event_bus=EventBus(),
        registry=registry,
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=("test.critical_action",),
            permissions_by_skill_id={"test.critical_action": ("desktop.action",)},
            allowed_actions_by_skill_id={"test.critical_action": ("system.run_shell",)},
        ),
        effect_executor=DesktopSkillEffectExecutor(desktop_actions=desktop_actions),
    )

    result = asyncio.run(
        manager.run(
            SkillRequest(
                skill_id="test.critical_action",
                user_confirmed=True,
            )
        )
    )

    assert result.status is SkillRunStatus.DENIED
    assert result.effects[0].status == "denied"
    assert result.effects[0].message == "critical_actions_prohibited"
