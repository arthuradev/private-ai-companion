from __future__ import annotations

from pathlib import Path

from private_ai_companion.memory import (
    REDACTED_REJECTED_MEMORY,
    MemoryCandidate,
    MemoryPolicy,
    MemoryPolicyAction,
    MemoryReviewService,
    MemorySensitivity,
    MemorySource,
    MemoryStatus,
    SQLiteMemoryRepository,
)


def test_memory_policy_rejects_sensitive_candidates_by_default() -> None:
    decision = MemoryPolicy().decide_candidate(
        MemoryCandidate(
            content="Private bank token",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.SENSITIVE,
            confidence=0.99,
        )
    )

    assert decision.action is MemoryPolicyAction.REJECT
    assert decision.status is MemoryStatus.REJECTED
    assert decision.reason == "sensitive_memory_requires_explicit_safe_flow"


def test_memory_policy_keeps_low_sensitivity_candidates_pending_by_default() -> None:
    decision = MemoryPolicy().decide_candidate(
        MemoryCandidate(
            content="User prefers short answers.",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.LOW,
            confidence=0.90,
        )
    )

    assert decision.action is MemoryPolicyAction.PENDING_REVIEW
    assert decision.status is MemoryStatus.PENDING_REVIEW


def test_memory_policy_rejects_low_confidence_candidates() -> None:
    decision = MemoryPolicy(minimum_confidence=0.75).decide_candidate(
        MemoryCandidate(
            content="Maybe a preference",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.LOW,
            confidence=0.50,
        )
    )

    assert decision.action is MemoryPolicyAction.REJECT
    assert decision.reason == "confidence_below_minimum"


def test_rejected_sensitive_candidate_is_not_stored_raw(tmp_path: Path) -> None:
    service = MemoryReviewService(
        repository=SQLiteMemoryRepository(tmp_path / "memory.sqlite3"),
        policy=MemoryPolicy(),
    )

    record = service.submit_candidate(
        MemoryCandidate(
            content="my bank token is super-secret",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.SENSITIVE,
            confidence=0.99,
        )
    )

    assert record.status is MemoryStatus.REJECTED
    assert record.content == REDACTED_REJECTED_MEMORY
    assert "super-secret" not in record.content
