from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class SpeechAudioFormat(StrEnum):
    TEXT = "text/plain"
    WAV = "audio/wav"
    MP3 = "audio/mpeg"


class SpeechQueueStatus(StrEnum):
    QUEUED = "queued"
    SYNTHESIZING = "synthesizing"
    PLAYING = "playing"
    FINISHED = "finished"
    INTERRUPTED = "interrupted"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class TTSRequest:
    text: str
    voice_id: str | None = None
    language: str = "pt-BR"
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class SpeechAudio:
    audio_id: str
    request_id: str
    content: bytes
    audio_format: SpeechAudioFormat
    duration_seconds: float


@dataclass(frozen=True, slots=True)
class SpeechQueueItem:
    item_id: str
    request: TTSRequest
    status: SpeechQueueStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class SpeechInterruptResult:
    interrupted_item_id: str | None
    cleared_items: int
    reason: str
