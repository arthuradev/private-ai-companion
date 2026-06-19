from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from private_ai_companion.core import (
    BaseEvent,
    EventBus,
    SkillCompleted,
    SkillDenied,
    SkillInvoked,
)
from private_ai_companion.skills import (
    LocalNoteSkill,
    SkillEffectRequest,
    SkillEffectResult,
    SkillManager,
    SkillPolicy,
    SkillRegistry,
    SkillRequest,
    SkillRunStatus,
    StatusSkill,
)


def _empty_effect_calls() -> list[SkillEffectRequest]:
    return []


@dataclass(slots=True)
class FakeSkillEffectExecutor:
    status: str = "executed"
    calls: list[SkillEffectRequest] = field(default_factory=_empty_effect_calls)

    async def execute_effect(
        self,
        request: SkillRequest,
        effect: SkillEffectRequest,
    ) -> SkillEffectResult:
        _ = request
        self.calls.append(effect)
        return SkillEffectResult(
            kind=effect.kind,
            status=self.status,
            message="effect_executed",
        )


def build_registry() -> SkillRegistry:
    registry = SkillRegistry()
    registry.register(StatusSkill())
    registry.register(LocalNoteSkill())
    return registry


def test_skill_manager_runs_enabled_status_skill() -> None:
    executor = FakeSkillEffectExecutor()
    manager = SkillManager(
        event_bus=EventBus(),
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=("builtin.status",),
            permissions_by_skill_id={"builtin.status": ("status.read",)},
            allowed_actions_by_skill_id={"builtin.status": ()},
        ),
        effect_executor=executor,
    )

    result = asyncio.run(manager.run(SkillRequest(skill_id="builtin.status")))

    assert result.status is SkillRunStatus.COMPLETED
    assert result.output["status"] == "ready"
    assert executor.calls == []


def test_skill_manager_denies_disabled_skill() -> None:
    manager = SkillManager(
        event_bus=EventBus(),
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=(),
            permissions_by_skill_id={},
            allowed_actions_by_skill_id={},
        ),
        effect_executor=FakeSkillEffectExecutor(),
    )

    result = asyncio.run(manager.run(SkillRequest(skill_id="builtin.status")))

    assert result.status is SkillRunStatus.DENIED
    assert result.message == "skill_disabled"


def test_skill_manager_denies_missing_permission() -> None:
    manager = SkillManager(
        event_bus=EventBus(),
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=("builtin.status",),
            permissions_by_skill_id={"builtin.status": ()},
            allowed_actions_by_skill_id={"builtin.status": ()},
        ),
        effect_executor=FakeSkillEffectExecutor(),
    )

    result = asyncio.run(manager.run(SkillRequest(skill_id="builtin.status")))

    assert result.status is SkillRunStatus.DENIED
    assert result.message == "skill_permission_not_granted"


def test_skill_manager_denies_unregistered_enabled_skill() -> None:
    manager = SkillManager(
        event_bus=EventBus(),
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=("external.missing",),
            permissions_by_skill_id={"external.missing": ()},
            allowed_actions_by_skill_id={"external.missing": ()},
        ),
        effect_executor=FakeSkillEffectExecutor(),
    )

    result = asyncio.run(manager.run(SkillRequest(skill_id="external.missing")))

    assert result.status is SkillRunStatus.DENIED
    assert result.message == "skill_not_registered"


def test_skill_manager_denies_unallowed_skill_action() -> None:
    executor = FakeSkillEffectExecutor()
    manager = SkillManager(
        event_bus=EventBus(),
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=("builtin.local_note",),
            permissions_by_skill_id={"builtin.local_note": ("desktop.action",)},
            allowed_actions_by_skill_id={"builtin.local_note": ()},
        ),
        effect_executor=executor,
    )

    result = asyncio.run(
        manager.run(
            SkillRequest(
                skill_id="builtin.local_note",
                input={"title": "Hello"},
            )
        )
    )

    assert result.status is SkillRunStatus.DENIED
    assert result.message == "skill_action_not_allowed:desktop.create_note"
    assert executor.calls == []


def test_skill_manager_publishes_sanitized_events() -> None:
    events: list[BaseEvent] = []
    event_bus = EventBus()
    event_bus.subscribe(BaseEvent, events.append)
    manager = SkillManager(
        event_bus=event_bus,
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=("builtin.status",),
            permissions_by_skill_id={"builtin.status": ("status.read",)},
            allowed_actions_by_skill_id={"builtin.status": ()},
        ),
        effect_executor=FakeSkillEffectExecutor(),
    )

    result = asyncio.run(manager.run(SkillRequest(skill_id="builtin.status")))

    assert result.status is SkillRunStatus.COMPLETED
    assert [type(event) for event in events] == [SkillInvoked, SkillCompleted]
    assert all(not hasattr(event, "input") for event in events)


def test_skill_manager_publishes_denied_event() -> None:
    events: list[BaseEvent] = []
    event_bus = EventBus()
    event_bus.subscribe(BaseEvent, events.append)
    manager = SkillManager(
        event_bus=event_bus,
        registry=build_registry(),
        policy=SkillPolicy(
            enabled=True,
            enabled_skill_ids=(),
            permissions_by_skill_id={},
            allowed_actions_by_skill_id={},
        ),
        effect_executor=FakeSkillEffectExecutor(),
    )

    result = asyncio.run(manager.run(SkillRequest(skill_id="builtin.status")))

    assert result.status is SkillRunStatus.DENIED
    assert [type(event) for event in events] == [
        SkillInvoked,
        SkillDenied,
        SkillCompleted,
    ]
