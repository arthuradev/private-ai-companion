from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.skills.models import (
    SkillEffectKind,
    SkillEffectRequest,
    SkillInvocation,
    SkillManifest,
    SkillRequest,
    SkillRunStatus,
)


@dataclass(frozen=True, slots=True)
class StatusSkill:
    @property
    def manifest(self) -> SkillManifest:
        return SkillManifest(
            skill_id="builtin.status",
            name="Status",
            description="Report a local readiness status.",
            version="0.1.0",
            permissions=("status.read",),
        )

    async def invoke(self, request: SkillRequest) -> SkillInvocation:
        _ = request
        return SkillInvocation(
            status=SkillRunStatus.COMPLETED,
            message="ready",
            output={"status": "ready"},
        )


@dataclass(frozen=True, slots=True)
class LocalNoteSkill:
    @property
    def manifest(self) -> SkillManifest:
        return SkillManifest(
            skill_id="builtin.local_note",
            name="Local note",
            description="Create a local note through the safe desktop action port.",
            version="0.1.0",
            permissions=("desktop.action",),
            allowed_action_types=("desktop.create_note",),
        )

    async def invoke(self, request: SkillRequest) -> SkillInvocation:
        title = request.input.get("title", "").strip()
        if not title:
            return SkillInvocation(
                status=SkillRunStatus.FAILED,
                message="note_title_required",
            )
        return SkillInvocation(
            status=SkillRunStatus.COMPLETED,
            message="local_note_requested",
            effects=(
                SkillEffectRequest(
                    kind=SkillEffectKind.DESKTOP_ACTION,
                    action_type="desktop.create_note",
                    parameters={
                        "title": title,
                        "body": request.input.get("body", ""),
                    },
                    user_confirmed=request.user_confirmed,
                    dry_run_only=request.dry_run_only,
                ),
            ),
        )


@dataclass(frozen=True, slots=True)
class OpenAllowedAppSkill:
    @property
    def manifest(self) -> SkillManifest:
        return SkillManifest(
            skill_id="builtin.open_allowed_app",
            name="Open allowed app",
            description="Request an allowlisted app through the safe desktop port.",
            version="0.1.0",
            permissions=("desktop.action",),
            allowed_action_types=("desktop.open_allowed_app",),
        )

    async def invoke(self, request: SkillRequest) -> SkillInvocation:
        app_id = request.input.get("app_id", "").strip()
        if not app_id:
            return SkillInvocation(
                status=SkillRunStatus.FAILED,
                message="app_id_required",
            )
        return SkillInvocation(
            status=SkillRunStatus.COMPLETED,
            message="open_allowed_app_requested",
            effects=(
                SkillEffectRequest(
                    kind=SkillEffectKind.DESKTOP_ACTION,
                    action_type="desktop.open_allowed_app",
                    parameters={"app_id": app_id},
                    user_confirmed=request.user_confirmed,
                    dry_run_only=request.dry_run_only,
                ),
            ),
        )
