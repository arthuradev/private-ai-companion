from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.core import (
    ActionExecuted,
    ActionIntentCreated,
    AuditEventCreated,
    EventBus,
    EventMetadata,
    EventSensitivity,
    PermissionRequired,
)
from private_ai_companion.desktop.models import (
    DesktopActionRequest,
    DesktopActionResult,
)
from private_ai_companion.desktop.permissions import DesktopPermissionPolicy
from private_ai_companion.desktop.ports import DesktopActionExecutor
from private_ai_companion.safety import (
    ActionAuditRecord,
    ActionExecutionStatus,
    ActionIntent,
    ActionPolicy,
    ActionPolicyDecision,
    InMemoryActionAuditLog,
    RiskClassification,
    RiskClassifier,
)


@dataclass(slots=True)
class DesktopActionService:
    event_bus: EventBus
    executor: DesktopActionExecutor
    risk_classifier: RiskClassifier
    action_policy: ActionPolicy
    permission_policy: DesktopPermissionPolicy
    audit_log: InMemoryActionAuditLog

    @property
    def executor_id(self) -> str:
        return self.executor.executor_id

    @property
    def audit_records(self) -> tuple[ActionAuditRecord, ...]:
        return self.audit_log.list_records()

    async def perform(self, request: DesktopActionRequest) -> DesktopActionResult:
        intent = ActionIntent(
            action_type=request.action_type,
            parameters=dict(request.parameters),
            source=request.source,
            user_confirmed=request.user_confirmed,
            dry_run_only=request.dry_run_only,
        )
        await self.event_bus.publish(
            ActionIntentCreated(
                action_id=intent.action_id,
                action_type=intent.action_type,
                source=intent.source,
                metadata=_action_event_metadata(),
            )
        )

        classification = self.risk_classifier.classify(intent)
        decision = self.action_policy.evaluate(intent, classification)
        if decision.denied:
            return await self._deny(intent, classification, decision)

        permission = self.permission_policy.evaluate(intent)
        if not permission.allowed:
            denied_decision = ActionPolicyDecision(
                action_id=intent.action_id,
                action_type=intent.action_type,
                risk=classification.risk,
                status=decision.status,
                reason=permission.reason,
                requires_confirmation=decision.requires_confirmation,
            )
            return await self._deny(intent, classification, denied_decision)

        dry_run = await self.executor.dry_run(intent, classification.risk)
        if request.dry_run_only:
            record = self.audit_log.record(
                intent=intent,
                decision=decision,
                outcome=ActionExecutionStatus.DRY_RUN,
                reason="dry_run_only",
            )
            await self._publish_action_executed(
                intent=intent,
                classification=classification,
                status=ActionExecutionStatus.DRY_RUN,
                dry_run=True,
            )
            await self._publish_audit(record)
            return DesktopActionResult(
                action_id=intent.action_id,
                action_type=intent.action_type,
                status=ActionExecutionStatus.DRY_RUN,
                risk=classification.risk,
                message=dry_run.summary,
                dry_run=dry_run,
                audit_record=record,
            )

        if decision.requires_confirmation and not intent.user_confirmed:
            record = self.audit_log.record(
                intent=intent,
                decision=decision,
                outcome=ActionExecutionStatus.REQUIRES_CONFIRMATION,
                reason=decision.reason,
            )
            await self.event_bus.publish(
                PermissionRequired(
                    action_id=intent.action_id,
                    action_type=intent.action_type,
                    risk=classification.risk.value,
                    reason=decision.reason,
                    metadata=_action_event_metadata(),
                )
            )
            await self._publish_audit(record)
            return DesktopActionResult(
                action_id=intent.action_id,
                action_type=intent.action_type,
                status=ActionExecutionStatus.REQUIRES_CONFIRMATION,
                risk=classification.risk,
                message=decision.reason,
                dry_run=dry_run,
                audit_record=record,
            )

        execution = await self.executor.execute(intent, classification.risk)
        record = self.audit_log.record(
            intent=intent,
            decision=decision,
            outcome=execution.status,
            reason=execution.message,
        )
        await self._publish_action_executed(
            intent=intent,
            classification=classification,
            status=execution.status,
            dry_run=False,
        )
        await self._publish_audit(record)
        return DesktopActionResult(
            action_id=intent.action_id,
            action_type=intent.action_type,
            status=execution.status,
            risk=classification.risk,
            message=execution.message,
            dry_run=dry_run,
            output=execution.output,
            audit_record=record,
        )

    async def _deny(
        self,
        intent: ActionIntent,
        classification: RiskClassification,
        decision: ActionPolicyDecision,
    ) -> DesktopActionResult:
        record = self.audit_log.record(
            intent=intent,
            decision=decision,
            outcome=ActionExecutionStatus.DENIED,
            reason=decision.reason,
        )
        await self._publish_audit(record)
        return DesktopActionResult(
            action_id=intent.action_id,
            action_type=intent.action_type,
            status=ActionExecutionStatus.DENIED,
            risk=classification.risk,
            message=decision.reason,
            audit_record=record,
        )

    async def _publish_action_executed(
        self,
        *,
        intent: ActionIntent,
        classification: RiskClassification,
        status: ActionExecutionStatus,
        dry_run: bool,
    ) -> None:
        await self.event_bus.publish(
            ActionExecuted(
                action_id=intent.action_id,
                action_type=intent.action_type,
                risk=classification.risk.value,
                status=status.value,
                executor_id=self.executor.executor_id,
                dry_run=dry_run,
                metadata=_action_event_metadata(),
            )
        )

    async def _publish_audit(self, record: ActionAuditRecord) -> None:
        await self.event_bus.publish(
            AuditEventCreated(
                audit_id=record.audit_id,
                action_id=record.action_id,
                action_type=record.action_type,
                risk=record.risk.value,
                decision=record.decision.value,
                outcome=record.outcome.value,
                metadata=_action_event_metadata(),
            )
        )


def _action_event_metadata() -> EventMetadata:
    return EventMetadata(source="desktop", sensitivity=EventSensitivity.SENSITIVE)
