from __future__ import annotations

import asyncio
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from importlib import import_module
from typing import Protocol, cast
from uuid import uuid4

from private_ai_companion.speech import STTError, STTRequest, STTResult, STTSegment


class _WhisperModel(Protocol):
    def transcribe(
        self,
        audio: str,
        *,
        language: str | None,
        vad_filter: bool,
    ) -> tuple[Iterable[object], object]:
        """Subset of faster-whisper's WhisperModel API used by this adapter."""
        ...


@dataclass(slots=True)
class FasterWhisperSTTProvider:
    provider_id: str = "faster-whisper"
    model_size: str = "base"
    device: str = "cpu"
    compute_type: str = "int8"
    vad_filter: bool = True
    _model: _WhisperModel | None = field(default=None, init=False, repr=False)

    async def transcribe(self, request: STTRequest) -> STTResult:
        return await asyncio.to_thread(self._transcribe_sync, request)

    def _transcribe_sync(self, request: STTRequest) -> STTResult:
        if request.audio.path is None:
            raise STTError("faster-whisper STT requires an explicit audio file path")

        model = self._load_model()
        raw_segments, info = model.transcribe(
            str(request.audio.path),
            language=request.language,
            vad_filter=self.vad_filter,
        )
        segments = tuple(
            STTSegment(
                segment_id=str(uuid4()),
                start_seconds=_float_attr(raw_segment, "start", 0.0),
                end_seconds=_float_attr(raw_segment, "end", 0.0),
                text=_text_attr(raw_segment, "text").strip(),
                confidence=_optional_float_attr(raw_segment, "avg_logprob"),
            )
            for raw_segment in raw_segments
        )
        text = " ".join(segment.text for segment in segments if segment.text).strip()
        return STTResult(
            transcript_id=str(uuid4()),
            request_id=request.request_id,
            text=text,
            language=_optional_text_attr(info, "language") or request.language,
            confidence=_optional_float_attr(info, "language_probability"),
            duration_seconds=(
                segments[-1].end_seconds if segments else request.audio.duration_seconds
            ),
            segments=segments,
        )

    def _load_model(self) -> _WhisperModel:
        if self._model is not None:
            return self._model

        try:
            module = import_module("faster_whisper")
        except ModuleNotFoundError as exc:
            raise STTError(
                "faster-whisper is not installed. Install the optional STT extra "
                "before selecting provider_id='faster-whisper'."
            ) from exc

        model_factory = cast(Callable[..., _WhisperModel], module.WhisperModel)
        self._model = model_factory(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )
        return self._model


def _text_attr(source: object, attribute: str) -> str:
    value = cast(object, getattr(source, attribute, ""))
    return value if isinstance(value, str) else ""


def _optional_text_attr(source: object, attribute: str) -> str | None:
    value = _text_attr(source, attribute).strip()
    return value or None


def _float_attr(source: object, attribute: str, default: float) -> float:
    value = cast(object, getattr(source, attribute, default))
    if isinstance(value, int | float):
        return float(value)
    return default


def _optional_float_attr(source: object, attribute: str) -> float | None:
    value = cast(object, getattr(source, attribute, None))
    if isinstance(value, int | float):
        return float(value)
    return None
