from __future__ import annotations

import asyncio

from private_ai_companion.adapters.speech import FakeTTSProvider
from private_ai_companion.speech import SpeechAudioFormat, TTSRequest


def test_fake_tts_provider_synthesizes_text_audio() -> None:
    provider = FakeTTSProvider()

    audio = asyncio.run(
        provider.synthesize(
            TTSRequest(text="hello there", voice_id="voice-a", language="en-US")
        )
    )

    assert audio.request_id
    assert audio.audio_format is SpeechAudioFormat.TEXT
    assert audio.content.decode("utf-8") == "[fake-tts:voice-a] hello there"
    assert audio.duration_seconds > 0
