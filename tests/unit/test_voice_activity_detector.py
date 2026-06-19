from __future__ import annotations

import asyncio

from private_ai_companion.adapters.speech import EnergyVoiceActivityDetector
from private_ai_companion.speech import SpeechInputAudio, SpeechInputAudioFormat


def test_energy_voice_activity_detector_detects_active_audio() -> None:
    detector = EnergyVoiceActivityDetector(threshold=0.2)

    result = asyncio.run(
        detector.detect(
            SpeechInputAudio(
                audio_format=SpeechInputAudioFormat.WAV,
                content=b"\x00\x01\x02\x03",
            )
        )
    )

    assert result.has_voice is True
    assert result.reason == "voice_detected"


def test_energy_voice_activity_detector_rejects_empty_audio() -> None:
    detector = EnergyVoiceActivityDetector()

    result = asyncio.run(
        detector.detect(
            SpeechInputAudio(
                audio_format=SpeechInputAudioFormat.WAV,
                content=b"",
            )
        )
    )

    assert result.has_voice is False
    assert result.reason == "empty_audio"
