from __future__ import annotations

import asyncio

from private_ai_companion.adapters.speech import FakeSTTProvider
from private_ai_companion.speech import (
    SpeechInputAudio,
    SpeechInputAudioFormat,
    STTRequest,
)


def test_fake_stt_provider_transcribes_text_audio() -> None:
    provider = FakeSTTProvider()

    result = asyncio.run(
        provider.transcribe(
            STTRequest(
                audio=SpeechInputAudio(
                    audio_format=SpeechInputAudioFormat.TEXT,
                    content=b"hello by voice",
                    duration_seconds=1.2,
                ),
                language="en-US",
            )
        )
    )

    assert result.request_id
    assert result.text == "hello by voice"
    assert result.language == "en-US"
    assert result.confidence == 1.0
    assert result.duration_seconds == 1.2
    assert result.segments[0].text == "hello by voice"


def test_fake_stt_provider_uses_fallback_for_binary_audio() -> None:
    provider = FakeSTTProvider(fallback_transcript="fallback voice")

    result = asyncio.run(
        provider.transcribe(
            STTRequest(
                audio=SpeechInputAudio(
                    audio_format=SpeechInputAudioFormat.WAV,
                    content=b"\x01\x02",
                )
            )
        )
    )

    assert result.text == "fallback voice"
