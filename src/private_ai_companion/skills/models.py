from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class SkillRunStatus(StrEnum):
    COMPLETED = "completed"
    DENIED = "denied"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    FAILED = "failed"


class SkillEffectKind(StrEnum):
    DESKTOP_ACTION = "desktop_action"


def _empty_text_map() -> dict[str, str]:
    return {}


@dataclass(frozen=True, slots=True)
class SkillManifest:
    skill_id: str
    name: str
    description: str
    version: str
    permissions: tuple[str, ...] = ()
    allowed_action_types: tuple[str, ...] = ()
    enabled_by_default: bool = True


@dataclass(frozen=True, slots=True)
class SkillRequest:
    skill_id: str
    input: dict[str, str] = field(default_factory=_empty_text_map)
    user_confirmed: bool = False
    dry_run_only: bool = False
    source: str = "manual_cli_request"
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class SkillEffectRequest:
    kind: SkillEffectKind
    action_type: str
    parameters: dict[str, str] = field(default_factory=_empty_text_map)
    user_confirmed: bool = False
    dry_run_only: bool = False


@dataclass(frozen=True, slots=True)
class SkillEffectResult:
    kind: SkillEffectKind
    status: str
    message: str
    output: dict[str, str] = field(default_factory=_empty_text_map)


@dataclass(frozen=True, slots=True)
class SkillInvocation:
    status: SkillRunStatus
    message: str
    output: dict[str, str] = field(default_factory=_empty_text_map)
    effects: tuple[SkillEffectRequest, ...] = ()


@dataclass(frozen=True, slots=True)
class SkillRunResult:
    skill_id: str
    request_id: str
    status: SkillRunStatus
    message: str
    output: dict[str, str] = field(default_factory=_empty_text_map)
    effects: tuple[SkillEffectResult, ...] = ()
