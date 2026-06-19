from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class ScreenCaptureMode(StrEnum):
    MANUAL = "manual"
    CONTINUOUS = "continuous"


class ScreenCaptureSource(StrEnum):
    SCREEN = "screen"
    WINDOW = "window"
    FAKE = "fake-screen"


class ScreenCaptureDecisionStatus(StrEnum):
    ALLOWED = "allowed"
    DENIED = "denied"


class VisionAnalysisStatus(StrEnum):
    READY = "ready"
    SKIPPED = "skipped"
    FAILED = "failed"


def _empty_metadata() -> dict[str, str]:
    return {}


@dataclass(frozen=True, slots=True)
class ScreenCaptureRequest:
    purpose: str
    mode: ScreenCaptureMode = ScreenCaptureMode.MANUAL
    user_authorized: bool = False
    allow_persistence: bool = False
    allow_external_analysis: bool = False
    source: ScreenCaptureSource = ScreenCaptureSource.SCREEN
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class ScreenCapturePolicyDecision:
    request_id: str
    status: ScreenCaptureDecisionStatus
    reason: str
    allow_persistence: bool = False
    allow_external_analysis: bool = False

    @property
    def allowed(self) -> bool:
        return self.status is ScreenCaptureDecisionStatus.ALLOWED


@dataclass(frozen=True, slots=True)
class ScreenshotImage:
    screenshot_id: str
    request_id: str
    content: bytes
    image_format: str
    width: int
    height: int
    source: ScreenCaptureSource
    captured_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    persist: bool = False
    metadata: dict[str, str] = field(default_factory=_empty_metadata)


@dataclass(frozen=True, slots=True)
class RedactionFinding:
    rule_id: str
    count: int


@dataclass(frozen=True, slots=True)
class RedactionResult:
    screenshot: ScreenshotImage
    visible_text: str
    findings: tuple[RedactionFinding, ...] = ()

    @property
    def redacted(self) -> bool:
        return any(finding.count > 0 for finding in self.findings)

    @property
    def finding_count(self) -> int:
        return sum(finding.count for finding in self.findings)


@dataclass(frozen=True, slots=True)
class VisionAnalysisRequest:
    screenshot: ScreenshotImage
    visible_text: str
    allow_external_analysis: bool = False
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class VisionAnalysisResult:
    provider_id: str
    request_id: str
    status: VisionAnalysisStatus
    summary: str
    labels: tuple[str, ...] = ()
    visible_text: str = ""
    safety_notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class VisualContext:
    context_id: str
    request_id: str
    screenshot_id: str
    provider_id: str
    summary: str
    labels: tuple[str, ...]
    visible_text: str
    redacted: bool
    transient: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
