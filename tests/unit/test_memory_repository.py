from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.memory import (
    MemoryCandidate,
    MemorySensitivity,
    MemorySource,
    MemoryStatus,
    SQLiteMemoryRepository,
)


def test_sqlite_memory_repository_creates_and_reviews_memory(tmp_path: Path) -> None:
    repository = SQLiteMemoryRepository(tmp_path / "memory.sqlite3")
    candidate = MemoryCandidate(
        content="User likes local-first tools.",
        source=MemorySource.USER_TEXT,
        sensitivity=MemorySensitivity.LOW,
        confidence=0.90,
    )

    record = repository.create_from_candidate(
        candidate,
        status=MemoryStatus.PENDING_REVIEW,
        reason="requires_user_review",
    )
    approved = repository.update_status(
        record.memory_id,
        status=MemoryStatus.APPROVED,
        reason="user_approved",
    )

    assert approved.status is MemoryStatus.APPROVED
    assert repository.get(record.memory_id).content == "User likes local-first tools."
    assert repository.search_approved("local-first") == (approved,)
    assert repository.list_by_status(MemoryStatus.PENDING_REVIEW) == ()

    audit_entries = repository.audit_entries(record.memory_id)
    assert [entry.action for entry in audit_entries] == [
        "candidate_created",
        "status_changed_to_approved",
    ]
    assert all("local-first" not in entry.reason for entry in audit_entries)


def test_sqlite_memory_repository_supports_edit_and_delete(tmp_path: Path) -> None:
    repository = SQLiteMemoryRepository(tmp_path / "memory.sqlite3")
    record = repository.create_from_candidate(
        MemoryCandidate(
            content="Original content",
            source=MemorySource.USER_REVIEW,
            sensitivity=MemorySensitivity.LOW,
            confidence=1.0,
        ),
        status=MemoryStatus.APPROVED,
        reason="user_approved",
    )

    edited = repository.update_content(
        record.memory_id,
        content="Edited content",
        reason="user_edited",
    )
    deleted = repository.delete(record.memory_id, reason="user_deleted")

    assert edited.content == "Edited content"
    assert deleted.status is MemoryStatus.DELETED
    assert repository.search_approved("Edited") == ()


def test_sqlite_memory_repository_rejects_empty_content_edits(tmp_path: Path) -> None:
    repository = SQLiteMemoryRepository(tmp_path / "memory.sqlite3")
    record = repository.create_from_candidate(
        MemoryCandidate(
            content="Keep this",
            source=MemorySource.USER_REVIEW,
            sensitivity=MemorySensitivity.LOW,
            confidence=1.0,
        ),
        status=MemoryStatus.APPROVED,
        reason="user_approved",
    )

    with pytest.raises(ValueError, match="memory content cannot be empty"):
        repository.update_content(record.memory_id, content=" ", reason="bad_edit")
