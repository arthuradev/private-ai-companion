from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import SpeechConfigError, load_speech_config


def test_load_speech_config_reads_default_file() -> None:
    config = load_speech_config()

    assert config.tts.provider_id == "fake-tts"
    assert config.tts.voice_id == "default"
    assert config.tts.language == "pt-BR"
    assert config.tts.audio_format == "text/plain"
    assert config.playback.enabled is False
    assert config.playback.interrupt_on_new_input is True
    assert config.stt.provider_id == "fake-stt"
    assert config.stt.language == "pt-BR"
    assert config.stt.enabled is True
    assert config.input.mode == "push-to-talk"
    assert config.input.microphone_enabled is False
    assert config.input.vad_enabled is True


def test_load_speech_config_reads_custom_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "speech.toml"
    config_path.write_text(
        """
[speech.tts]
provider_id = "fake-tts"
voice_id = "soft"
language = "en-US"
audio_format = "audio/wav"
enabled = true

[speech.playback]
enabled = true
interrupt_on_new_input = false

[speech.stt]
provider_id = "faster-whisper"
language = "en-US"
model_size = "small"
device = "cpu"
compute_type = "int8"
vad_filter = true
enabled = true

[speech.input]
mode = "vad"
microphone_enabled = false
vad_enabled = true
vad_threshold = 0.2
max_record_seconds = 12.5
""".strip(),
        encoding="utf-8",
    )

    config = load_speech_config(config_path)

    assert config.tts.voice_id == "soft"
    assert config.tts.audio_format == "audio/wav"
    assert config.playback.enabled is True
    assert config.playback.interrupt_on_new_input is False
    assert config.stt.provider_id == "faster-whisper"
    assert config.stt.model_size == "small"
    assert config.input.mode == "vad"
    assert config.input.vad_threshold == 0.2


def test_load_speech_config_rejects_unknown_audio_format(tmp_path: Path) -> None:
    config_path = tmp_path / "speech.toml"
    config_path.write_text(
        """
[speech.tts]
provider_id = "fake-tts"
voice_id = "soft"
language = "en-US"
audio_format = "application/unknown"
enabled = true

[speech.playback]
enabled = true
interrupt_on_new_input = true

[speech.stt]
provider_id = "fake-stt"
language = "pt-BR"
model_size = "base"
device = "cpu"
compute_type = "int8"
vad_filter = true
enabled = true

[speech.input]
mode = "push-to-talk"
microphone_enabled = false
vad_enabled = true
vad_threshold = 0.01
max_record_seconds = 30.0
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(SpeechConfigError):
        load_speech_config(config_path)


def test_load_speech_config_rejects_unknown_input_mode(tmp_path: Path) -> None:
    config_path = tmp_path / "speech.toml"
    config_path.write_text(
        """
[speech.tts]
provider_id = "fake-tts"
voice_id = "soft"
language = "en-US"
audio_format = "text/plain"
enabled = true

[speech.playback]
enabled = true
interrupt_on_new_input = true

[speech.stt]
provider_id = "fake-stt"
language = "pt-BR"
model_size = "base"
device = "cpu"
compute_type = "int8"
vad_filter = true
enabled = true

[speech.input]
mode = "always-on"
microphone_enabled = false
vad_enabled = true
vad_threshold = 0.01
max_record_seconds = 30.0
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(SpeechConfigError):
        load_speech_config(config_path)
