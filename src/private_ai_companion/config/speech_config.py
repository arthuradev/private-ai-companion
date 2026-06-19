from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.config.errors import ConfigError

DEFAULT_SPEECH_CONFIG_PATH = Path("configs/speech.default.toml")
SUPPORTED_AUDIO_FORMATS = {"text/plain", "audio/wav", "audio/mpeg"}


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
class SpeechConfig:
    tts: TTSConfig
    playback: PlaybackConfig


def load_speech_config(path: Path | None = None) -> SpeechConfig:
    config_path = path or DEFAULT_SPEECH_CONFIG_PATH
    if not config_path.exists():
        return default_speech_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    speech_raw = _required_mapping(raw, "speech")
    tts_raw = _required_mapping(speech_raw, "tts")
    playback_raw = _required_mapping(speech_raw, "playback")
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


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise SpeechConfigError(f"speech config field {key!r} must be boolean")
    return value


def _audio_format_text(value: str) -> str:
    if value not in SUPPORTED_AUDIO_FORMATS:
        raise SpeechConfigError(f"unknown speech audio format {value!r}")
    return value
