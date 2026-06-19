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


@dataclass(frozen=True, slots=True)
class UserTextReceived(BaseEvent):
    text: str = ""


@dataclass(frozen=True, slots=True)
class UserSpeechReceived(BaseEvent):
    text: str = ""
    language: str | None = None
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class AssistantTextReady(BaseEvent):
    text: str = ""


@dataclass(frozen=True, slots=True)
class VoiceInputStarted(BaseEvent):
    mode: str = "push-to-talk"


@dataclass(frozen=True, slots=True)
class VoiceInputFinished(BaseEvent):
    status: str = "transcribed"
    transcript_id: str | None = None
    duration_seconds: float | None = None


@dataclass(frozen=True, slots=True)
class VoiceInputIgnored(BaseEvent):
    reason: str = "ignored"


@dataclass(frozen=True, slots=True)
class TTSRequested(BaseEvent):
    text: str = ""
    voice_id: str | None = None


@dataclass(frozen=True, slots=True)
class SpeechStarted(BaseEvent):
    item_id: str = ""


@dataclass(frozen=True, slots=True)
class SpeechFinished(BaseEvent):
    item_id: str = ""


@dataclass(frozen=True, slots=True)
class SpeechInterrupted(BaseEvent):
    reason: str = "interrupted"
    interrupted_item_id: str | None = None
    cleared_items: int = 0


@dataclass(frozen=True, slots=True)
class AvatarStateRequested(BaseEvent):
    expression: str = "idle"
    reason: str = "state_requested"
    intensity: float = 1.0


@dataclass(frozen=True, slots=True)
class AvatarStateApplied(BaseEvent):
    expression: str = "idle"
    provider_id: str = ""
    status: str = "applied"


@dataclass(frozen=True, slots=True)
class AvatarLipsyncUpdated(BaseEvent):
    parameter_name: str = ""
    value: float = 0.0
    provider_id: str = ""


@dataclass(frozen=True, slots=True)
class ScreenContextRequested(BaseEvent):
    request_id: str = ""
    mode: str = "manual"
    purpose: str = ""


@dataclass(frozen=True, slots=True)
class ScreenContextCaptured(BaseEvent):
    request_id: str = ""
    screenshot_id: str = ""
    capture_provider_id: str = ""
    image_format: str = ""
    width: int = 0
    height: int = 0
    persisted: bool = False


@dataclass(frozen=True, slots=True)
class ScreenContextDenied(BaseEvent):
    request_id: str = ""
    reason: str = ""


@dataclass(frozen=True, slots=True)
class ScreenContextRedacted(BaseEvent):
    request_id: str = ""
    screenshot_id: str = ""
    redacted: bool = False
    finding_count: int = 0


@dataclass(frozen=True, slots=True)
class VisionAnalysisReady(BaseEvent):
    request_id: str = ""
    context_id: str = ""
    vision_provider_id: str = ""
    status: str = "ready"
    label_count: int = 0
    redacted: bool = False


@dataclass(frozen=True, slots=True)
class ActionIntentCreated(BaseEvent):
    action_id: str = ""
    action_type: str = ""
    source: str = ""


@dataclass(frozen=True, slots=True)
class PermissionRequired(BaseEvent):
    action_id: str = ""
    action_type: str = ""
    risk: str = ""
    reason: str = ""


@dataclass(frozen=True, slots=True)
class ActionExecuted(BaseEvent):
    action_id: str = ""
    action_type: str = ""
    risk: str = ""
    status: str = ""
    executor_id: str = ""
    dry_run: bool = False


@dataclass(frozen=True, slots=True)
class AuditEventCreated(BaseEvent):
    audit_id: str = ""
    action_id: str = ""
    action_type: str = ""
    risk: str = ""
    decision: str = ""
    outcome: str = ""


@dataclass(frozen=True, slots=True)
class SkillInvoked(BaseEvent):
    skill_id: str = ""
    request_id: str = ""
    source: str = ""


@dataclass(frozen=True, slots=True)
class SkillDenied(BaseEvent):
    skill_id: str = ""
    request_id: str = ""
    reason: str = ""


@dataclass(frozen=True, slots=True)
class SkillCompleted(BaseEvent):
    skill_id: str = ""
    request_id: str = ""
    status: str = ""
    effect_count: int = 0
