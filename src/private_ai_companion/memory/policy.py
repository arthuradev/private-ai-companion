from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from private_ai_companion.memory.models import (
    MemoryCandidate,
    MemorySensitivity,
    MemoryStatus,
)


class MemoryPolicyAction(StrEnum):
    PENDING_REVIEW = "pending_review"
    APPROVE = "approve"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class MemoryPolicyDecision:
    action: MemoryPolicyAction
    status: MemoryStatus
    reason: str


@dataclass(frozen=True, slots=True)
class MemoryPolicy:
    reject_sensitive_by_default: bool = True
    auto_approve_low_sensitivity: bool = False
    minimum_confidence: float = 0.40

    def decide_candidate(self, candidate: MemoryCandidate) -> MemoryPolicyDecision:
        if not candidate.content.strip():
            return MemoryPolicyDecision(
                action=MemoryPolicyAction.REJECT,
                status=MemoryStatus.REJECTED,
                reason="empty_content",
            )

        if candidate.confidence < self.minimum_confidence:
            return MemoryPolicyDecision(
                action=MemoryPolicyAction.REJECT,
                status=MemoryStatus.REJECTED,
                reason="confidence_below_minimum",
            )

        if self.reject_sensitive_by_default and candidate.sensitivity in {
            MemorySensitivity.HIGH,
            MemorySensitivity.SENSITIVE,
        }:
            return MemoryPolicyDecision(
                action=MemoryPolicyAction.REJECT,
                status=MemoryStatus.REJECTED,
                reason="sensitive_memory_requires_explicit_safe_flow",
            )

        if (
            self.auto_approve_low_sensitivity
            and candidate.sensitivity is MemorySensitivity.LOW
        ):
            return MemoryPolicyDecision(
                action=MemoryPolicyAction.APPROVE,
                status=MemoryStatus.APPROVED,
                reason="auto_approved_low_sensitivity",
            )

        return MemoryPolicyDecision(
            action=MemoryPolicyAction.PENDING_REVIEW,
            status=MemoryStatus.PENDING_REVIEW,
            reason="requires_user_review",
        )
