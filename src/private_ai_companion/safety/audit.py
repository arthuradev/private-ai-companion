from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from private_ai_companion.safety.models import (
    ActionAuditRecord,
    ActionDecisionStatus,
    ActionExecutionStatus,
    ActionIntent,
    ActionPolicyDecision,
)


def _empty_audit_records() -> list[ActionAuditRecord]:
    return []


@dataclass(slots=True)
class InMemoryActionAuditLog:
    _records: list[ActionAuditRecord] = field(default_factory=_empty_audit_records)

    def record(
        self,
        *,
        intent: ActionIntent,
        decision: ActionPolicyDecision,
        outcome: ActionExecutionStatus,
        reason: str,
    ) -> ActionAuditRecord:
        record = ActionAuditRecord(
            audit_id=str(uuid4()),
            action_id=intent.action_id,
            action_type=intent.action_type,
            risk=decision.risk,
            decision=decision.status,
            outcome=outcome,
            reason=reason,
            confirmation_required=(
                decision.status is ActionDecisionStatus.REQUIRES_CONFIRMATION
                or decision.requires_confirmation
            ),
            executed=outcome is ActionExecutionStatus.EXECUTED,
        )
        self._records.append(record)
        return record

    def list_records(self) -> tuple[ActionAuditRecord, ...]:
        return tuple(self._records)
