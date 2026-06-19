from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from uuid import uuid4


class SpeechAudioFormat(StrEnum):
    TEXT = "text/plain"
    WAV = "audio/wav"
    MP3 = "audio/mpeg"


class SpeechInputAudioFormat(StrEnum):
    TEXT = "text/plain"
    WAV = "audio/wav"
    MP3 = "audio/mpeg"
    FLAC = "audio/flac"
    OGG = "audio/ogg"
    WEBM = "audio/webm"
    RAW = "application/octet-stream"


class SpeechInputMode(StrEnum):
    PUSH_TO_TALK = "push-to-talk"
    VAD = "vad"


class SpeechInputSource(StrEnum):
    BUFFER = "buffer"
    FILE = "file"
    MICROPHONE = "microphone"


class SpeechInputStatus(StrEnum):
    TRANSCRIBING = "transcribing"
    TRANSCRIBED = "transcribed"
    IGNORED = "ignored"
    FAILED = "failed"


SPEECH_INPUT_AUDIO_FORMAT_BY_SUFFIX = {
    ".txt": SpeechInputAudioFormat.TEXT,
    ".wav": SpeechInputAudioFormat.WAV,
    ".mp3": SpeechInputAudioFormat.MP3,
    ".flac": SpeechInputAudioFormat.FLAC,
    ".ogg": SpeechInputAudioFormat.OGG,
    ".webm": SpeechInputAudioFormat.WEBM,
}


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
class SpeechInputAudio:
    audio_format: SpeechInputAudioFormat
    content: bytes | None = None
    path: Path | None = None
    sample_rate_hz: int | None = None
    duration_seconds: float | None = None
    source: SpeechInputSource = SpeechInputSource.BUFFER

    @classmethod
    def from_path(
        cls,
        path: Path,
        *,
        audio_format: SpeechInputAudioFormat | None = None,
        duration_seconds: float | None = None,
    ) -> SpeechInputAudio:
        return cls(
            audio_format=audio_format or infer_speech_input_audio_format(path),
            path=path,
            duration_seconds=duration_seconds,
            source=SpeechInputSource.FILE,
        )


@dataclass(frozen=True, slots=True)
class STTRequest:
    audio: SpeechInputAudio
    language: str | None = None
    prompt: str | None = None
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class STTSegment:
    segment_id: str
    start_seconds: float
    end_seconds: float
    text: str
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class STTResult:
    transcript_id: str
    request_id: str
    text: str
    language: str | None
    confidence: float | None
    duration_seconds: float | None
    segments: tuple[STTSegment, ...] = ()


@dataclass(frozen=True, slots=True)
class VoiceActivityResult:
    has_voice: bool
    speech_ratio: float
    reason: str


@dataclass(frozen=True, slots=True)
class VoiceInputResult:
    request_id: str
    mode: SpeechInputMode
    status: SpeechInputStatus
    transcript: STTResult | None = None
    voice_activity: VoiceActivityResult | None = None
    ignored_reason: str | None = None


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


def infer_speech_input_audio_format(path: Path) -> SpeechInputAudioFormat:
    return SPEECH_INPUT_AUDIO_FORMAT_BY_SUFFIX.get(
        path.suffix.casefold(),
        SpeechInputAudioFormat.RAW,
    )
