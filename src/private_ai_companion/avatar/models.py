from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class AvatarExpression(StrEnum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    INTERRUPTED = "interrupted"
    HAPPY = "happy"
    CURIOUS = "curious"
    CONCERNED = "concerned"
    CONFUSED = "confused"
    NEUTRAL = "neutral"


class AvatarProviderStatus(StrEnum):
    APPLIED = "applied"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class AvatarExpressionRequest:
    expression: AvatarExpression
    intensity: float = 1.0
    transition_seconds: float = 0.2
    reason: str = "state_requested"
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class AvatarProviderResult:
    provider_id: str
    status: AvatarProviderStatus
    expression: AvatarExpression | None = None
    detail: str = ""
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class AvatarLipsyncFrame:
    mouth_open: float
    parameter_name: str = "MouthOpen"
    weight: float = 1.0
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class AvatarIdleState:
    enabled: bool
    expression: AvatarExpression = AvatarExpression.IDLE
    interval_seconds: float = 30.0
