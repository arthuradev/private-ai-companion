from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_SPEECH_CONFIG_PATH = Path("configs/speech.default.toml")
SUPPORTED_AUDIO_FORMATS = {"text/plain", "audio/wav", "audio/mpeg"}
SUPPORTED_SPEECH_INPUT_MODES = {"push-to-talk", "vad"}
SUPPORTED_STT_PROVIDER_IDS = {"fake-stt", "faster-whisper"}


class SpeechConfigError(ConfigError):
    """Raised when speech configuration is invalid."""


@dataclass(frozen=True, slots=True)
class TTSConfig:
    provider_id: str
    voice_id: str
    language: str
    audio_format: str
    enabled: bool


@dataclass(frozen=True, slots=True)
class PlaybackConfig:
    enabled: bool
    interrupt_on_new_input: bool


@dataclass(frozen=True, slots=True)
class STTConfig:
    provider_id: str
    language: str | None
    model_size: str
    device: str
    compute_type: str
    vad_filter: bool
    enabled: bool


@dataclass(frozen=True, slots=True)
class SpeechInputConfig:
    mode: str
    microphone_enabled: bool
    vad_enabled: bool
    vad_threshold: float
    max_record_seconds: float


@dataclass(frozen=True, slots=True)
class SpeechConfig:
    tts: TTSConfig
    playback: PlaybackConfig
    stt: STTConfig
    input: SpeechInputConfig


def load_speech_config(path: Path | None = None) -> SpeechConfig:
    config_path = path or DEFAULT_SPEECH_CONFIG_PATH
    if not config_path.exists():
        return default_speech_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    speech_raw = _required_mapping(raw, "speech")
    tts_raw = _required_mapping(speech_raw, "tts")
    playback_raw = _required_mapping(speech_raw, "playback")
    stt_raw = _required_mapping(speech_raw, "stt")
    input_raw = _required_mapping(speech_raw, "input")
    return SpeechConfig(
        tts=TTSConfig(
            provider_id=_required_text(tts_raw, "provider_id"),
            voice_id=_required_text(tts_raw, "voice_id"),
            language=_required_text(tts_raw, "language"),
            audio_format=_audio_format_text(_required_text(tts_raw, "audio_format")),
            enabled=_required_bool(tts_raw, "enabled"),
        ),
        playback=PlaybackConfig(
            enabled=_required_bool(playback_raw, "enabled"),
            interrupt_on_new_input=_required_bool(
                playback_raw,
                "interrupt_on_new_input",
            ),
        ),
        stt=STTConfig(
            provider_id=_stt_provider_id(_required_text(stt_raw, "provider_id")),
            language=_optional_text(stt_raw, "language"),
            model_size=_required_text(stt_raw, "model_size"),
            device=_required_text(stt_raw, "device"),
            compute_type=_required_text(stt_raw, "compute_type"),
            vad_filter=_required_bool(stt_raw, "vad_filter"),
            enabled=_required_bool(stt_raw, "enabled"),
        ),
        input=SpeechInputConfig(
            mode=_speech_input_mode(_required_text(input_raw, "mode")),
            microphone_enabled=_required_bool(input_raw, "microphone_enabled"),
            vad_enabled=_required_bool(input_raw, "vad_enabled"),
            vad_threshold=_ratio(input_raw, "vad_threshold"),
            max_record_seconds=_positive_float(input_raw, "max_record_seconds"),
        ),
    )


def default_speech_config() -> SpeechConfig:
    return SpeechConfig(
        tts=TTSConfig(
            provider_id="fake-tts",
            voice_id="default",
            language="pt-BR",
            audio_format="text/plain",
            enabled=True,
        ),
        playback=PlaybackConfig(
            enabled=False,
            interrupt_on_new_input=True,
        ),
        stt=STTConfig(
            provider_id="fake-stt",
            language="pt-BR",
            model_size="base",
            device="cpu",
            compute_type="int8",
            vad_filter=True,
            enabled=True,
        ),
        input=SpeechInputConfig(
            mode="push-to-talk",
            microphone_enabled=False,
            vad_enabled=True,
            vad_threshold=0.01,
            max_record_seconds=30.0,
        ),
    )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise SpeechConfigError(f"speech config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SpeechConfigError(f"speech config field {key!r} must be text")
    return value.strip()


def _optional_text(mapping: Mapping[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise SpeechConfigError(f"speech config field {key!r} must be text or null")
    stripped = value.strip()
    return stripped or None


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise SpeechConfigError(f"speech config field {key!r} must be boolean")
    return value


def _audio_format_text(value: str) -> str:
    if value not in SUPPORTED_AUDIO_FORMATS:
        raise SpeechConfigError(f"unknown speech audio format {value!r}")
    return value


def _stt_provider_id(value: str) -> str:
    if value not in SUPPORTED_STT_PROVIDER_IDS:
        raise SpeechConfigError(f"unknown STT provider {value!r}")
    return value


def _speech_input_mode(value: str) -> str:
    if value not in SUPPORTED_SPEECH_INPUT_MODES:
        raise SpeechConfigError(f"unknown speech input mode {value!r}")
    return value


def _ratio(mapping: Mapping[str, object], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, int | float):
        raise SpeechConfigError(f"speech config field {key!r} must be a number")
    ratio = float(value)
    if ratio < 0.0 or ratio > 1.0:
        raise SpeechConfigError(f"speech config field {key!r} must be between 0 and 1")
    return ratio


def _positive_float(mapping: Mapping[str, object], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, int | float):
        raise SpeechConfigError(f"speech config field {key!r} must be a number")
    number = float(value)
    if number <= 0.0:
        raise SpeechConfigError(f"speech config field {key!r} must be positive")
    return number
