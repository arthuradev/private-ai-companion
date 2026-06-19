from __future__ import annotations

import asyncio

from private_ai_companion.skills import (
    LocalNoteSkill,
    OpenAllowedAppSkill,
    SkillEffectKind,
    SkillRequest,
    SkillRunStatus,
    StatusSkill,
)


def test_status_skill_reports_ready() -> None:
    result = asyncio.run(StatusSkill().invoke(SkillRequest(skill_id="builtin.status")))

    assert result.status is SkillRunStatus.COMPLETED
    assert result.output["status"] == "ready"
    assert result.effects == ()


def test_local_note_skill_returns_desktop_effect() -> None:
    result = asyncio.run(
        LocalNoteSkill().invoke(
            SkillRequest(
                skill_id="builtin.local_note",
                input={"title": "Hello", "body": "Body"},
                user_confirmed=True,
            )
        )
    )

    assert result.status is SkillRunStatus.COMPLETED
    assert result.effects[0].kind is SkillEffectKind.DESKTOP_ACTION
    assert result.effects[0].action_type == "desktop.create_note"
    assert result.effects[0].user_confirmed is True


def test_open_allowed_app_skill_requires_app_id() -> None:
    result = asyncio.run(
        OpenAllowedAppSkill().invoke(SkillRequest(skill_id="builtin.open_allowed_app"))
    )

    assert result.status is SkillRunStatus.FAILED
    assert result.message == "app_id_required"
