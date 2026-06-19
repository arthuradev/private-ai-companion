from __future__ import annotations

from pathlib import Path

from private_ai_companion.memory import (
    MemoryCandidate,
    MemoryPolicy,
    MemoryReviewService,
    MemorySensitivity,
    MemorySource,
    MemoryStatus,
    SQLiteMemoryRepository,
)


def test_memory_review_service_stores_pending_candidate(tmp_path: Path) -> None:
    service = MemoryReviewService(
        repository=SQLiteMemoryRepository(tmp_path / "memory.sqlite3"),
        policy=MemoryPolicy(),
    )

    record = service.submit_candidate(
        MemoryCandidate(
            content="User prefers concise replies.",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.LOW,
            confidence=0.95,
        )
    )
    approved = service.approve(record.memory_id)

    assert record.status is MemoryStatus.PENDING_REVIEW
    assert approved.status is MemoryStatus.APPROVED


def test_memory_review_service_rejects_sensitive_candidate(tmp_path: Path) -> None:
    service = MemoryReviewService(
        repository=SQLiteMemoryRepository(tmp_path / "memory.sqlite3"),
        policy=MemoryPolicy(),
    )

    record = service.submit_candidate(
        MemoryCandidate(
            content="Sensitive private detail",
            source=MemorySource.USER_TEXT,
            sensitivity=MemorySensitivity.SENSITIVE,
            confidence=0.95,
        )
    )

    assert record.status is MemoryStatus.REJECTED
