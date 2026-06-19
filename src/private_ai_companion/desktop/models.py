from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from private_ai_companion.safety import (
    ActionAuditRecord,
    ActionExecutionStatus,
    RiskLevel,
)


class DesktopActionType(StrEnum):
    READ_ACTIVE_WINDOW_TITLE = "desktop.read_active_window_title"
    CREATE_NOTE = "desktop.create_note"
    OPEN_ALLOWED_APP = "desktop.open_allowed_app"


def _empty_parameters() -> dict[str, str]:
    return {}


def _empty_output() -> dict[str, str]:
    return {}


@dataclass(frozen=True, slots=True)
class DesktopActionRequest:
    action_type: str
    parameters: dict[str, str] = field(default_factory=_empty_parameters)
    source: str = "manual_cli_request"
    user_confirmed: bool = False
    dry_run_only: bool = False


@dataclass(frozen=True, slots=True)
class DesktopActionDryRun:
    action_id: str
    action_type: str
    risk: RiskLevel
    summary: str
    side_effects: tuple[str, ...] = ()
    safe_to_execute: bool = True


@dataclass(frozen=True, slots=True)
class DesktopActionExecutionResult:
    action_id: str
    action_type: str
    status: ActionExecutionStatus
    message: str
    output: dict[str, str] = field(default_factory=_empty_output)


@dataclass(frozen=True, slots=True)
class DesktopActionResult:
    action_id: str
    action_type: str
    status: ActionExecutionStatus
    risk: RiskLevel
    message: str
    dry_run: DesktopActionDryRun | None = None
    output: dict[str, str] = field(default_factory=_empty_output)
    audit_record: ActionAuditRecord | None = None
