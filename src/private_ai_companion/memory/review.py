from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.memory.models import (
    MemoryCandidate,
    MemoryRecord,
    MemorySensitivity,
    MemoryStatus,
)
from private_ai_companion.memory.policy import MemoryPolicy, MemoryPolicyAction
from private_ai_companion.memory.repository import SQLiteMemoryRepository

REDACTED_REJECTED_MEMORY = "[redacted rejected sensitive memory]"


@dataclass(frozen=True, slots=True)
class MemoryReviewService:
    repository: SQLiteMemoryRepository
    policy: MemoryPolicy

    def submit_candidate(self, candidate: MemoryCandidate) -> MemoryRecord:
        decision = self.policy.decide_candidate(candidate)
        candidate_to_store = self._redact_rejected_sensitive_candidate(
            candidate,
            rejected=decision.action is MemoryPolicyAction.REJECT,
        )
        return self.repository.create_from_candidate(
            candidate_to_store,
            status=decision.status,
            reason=decision.reason,
        )

    def approve(self, memory_id: str, *, reason: str = "user_approved") -> MemoryRecord:
        return self.repository.update_status(
            memory_id,
            status=MemoryStatus.APPROVED,
            reason=reason,
        )

    def reject(self, memory_id: str, *, reason: str = "user_rejected") -> MemoryRecord:
        return self.repository.update_status(
            memory_id,
            status=MemoryStatus.REJECTED,
            reason=reason,
        )

    def edit(
        self,
        memory_id: str,
        *,
        content: str,
        reason: str = "user_edited",
    ) -> MemoryRecord:
        return self.repository.update_content(
            memory_id,
            content=content,
            reason=reason,
        )

    def delete(self, memory_id: str, *, reason: str = "user_deleted") -> MemoryRecord:
        return self.repository.delete(memory_id, reason=reason)

    @staticmethod
    def _redact_rejected_sensitive_candidate(
        candidate: MemoryCandidate,
        *,
        rejected: bool,
    ) -> MemoryCandidate:
        if not rejected or candidate.sensitivity not in {
            MemorySensitivity.HIGH,
            MemorySensitivity.SENSITIVE,
        }:
            return candidate

        return MemoryCandidate(
            candidate_id=candidate.candidate_id,
            content=REDACTED_REJECTED_MEMORY,
            source=candidate.source,
            sensitivity=candidate.sensitivity,
            confidence=candidate.confidence,
            created_at=candidate.created_at,
        )
