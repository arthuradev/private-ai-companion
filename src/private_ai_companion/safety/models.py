from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionDecisionStatus(StrEnum):
    ALLOWED = "allowed"
    DENIED = "denied"
    REQUIRES_CONFIRMATION = "requires_confirmation"


class ActionExecutionStatus(StrEnum):
    DENIED = "denied"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    DRY_RUN = "dry_run"
    EXECUTED = "executed"
    FAILED = "failed"


def _empty_parameters() -> dict[str, str]:
    return {}


@dataclass(frozen=True, slots=True)
class ActionIntent:
    action_type: str
    parameters: dict[str, str] = field(default_factory=_empty_parameters)
    source: str = "manual_request"
    user_confirmed: bool = False
    dry_run_only: bool = False
    action_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class RiskClassification:
    action_id: str
    action_type: str
    risk: RiskLevel
    reason: str


@dataclass(frozen=True, slots=True)
class ActionPolicyDecision:
    action_id: str
    action_type: str
    risk: RiskLevel
    status: ActionDecisionStatus
    reason: str
    requires_confirmation: bool = False

    @property
    def allowed(self) -> bool:
        return self.status is ActionDecisionStatus.ALLOWED

    @property
    def denied(self) -> bool:
        return self.status is ActionDecisionStatus.DENIED


@dataclass(frozen=True, slots=True)
class ActionAuditRecord:
    audit_id: str
    action_id: str
    action_type: str
    risk: RiskLevel
    decision: ActionDecisionStatus
    outcome: ActionExecutionStatus
    reason: str
    confirmation_required: bool
    executed: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
