from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class EventSensitivity(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"
    SENSITIVE = "sensitive"


@dataclass(frozen=True, slots=True)
class EventMetadata:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    source: str = "core"
    correlation_id: str | None = None
    sensitivity: EventSensitivity = EventSensitivity.INTERNAL


@dataclass(frozen=True, slots=True)
class BaseEvent:
    metadata: EventMetadata = field(default_factory=EventMetadata)

    @property
    def name(self) -> str:
        return type(self).__name__


@dataclass(frozen=True, slots=True)
class AppStarted(BaseEvent):
    app_name: str = "private-ai-companion"
    version: str = "0.0.0"


@dataclass(frozen=True, slots=True)
class AppStopping(BaseEvent):
    reason: str = "shutdown_requested"


@dataclass(frozen=True, slots=True)
class AppStopped(BaseEvent):
    reason: str = "shutdown_complete"
