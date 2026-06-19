from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class MemorySensitivity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SENSITIVE = "sensitive"


class MemoryStatus(StrEnum):
    CANDIDATE = "candidate"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"


class MemorySource(StrEnum):
    USER_TEXT = "user_text"
    USER_REVIEW = "user_review"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class MemoryCandidate:
    content: str
    source: MemorySource
    sensitivity: MemorySensitivity
    confidence: float
    candidate_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    content: str
    source: MemorySource
    sensitivity: MemorySensitivity
    confidence: float
    status: MemoryStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class MemoryAuditEntry:
    audit_id: str
    memory_id: str
    action: str
    status: MemoryStatus
    reason: str
    created_at: datetime
