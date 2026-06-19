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
""".strip(),
        encoding="utf-8",
    )

    config = load_speech_config(config_path)

    assert config.tts.voice_id == "soft"
    assert config.tts.audio_format == "audio/wav"
    assert config.playback.enabled is True
    assert config.playback.interrupt_on_new_input is False


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
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(SpeechConfigError):
        load_speech_config(config_path)
