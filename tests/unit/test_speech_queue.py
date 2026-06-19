from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from private_ai_companion.adapters.speech import FakeAudioPlayer, FakeTTSProvider
from private_ai_companion.core import BaseEvent, EventBus
from private_ai_companion.speech import (
    SpeechAudio,
    SpeechQueueService,
    SpeechQueueStatus,
    TTSRequest,
)


def test_speech_queue_drains_tts_and_playback_events() -> None:
    event_bus = EventBus()
    player = FakeAudioPlayer()
    queue = SpeechQueueService(
        event_bus=event_bus,
        tts_provider=FakeTTSProvider(),
        audio_player=player,
    )
    events: list[str] = []

    def record_event(event: BaseEvent) -> None:
        events.append(event.name)

    event_bus.subscribe(BaseEvent, record_event)

    asyncio.run(queue.enqueue(TTSRequest(text="hello", voice_id="voice-a")))
    drained = asyncio.run(queue.drain_all())

    assert [item.status for item in drained] == [SpeechQueueStatus.FINISHED]
    assert len(player.played_audio) == 1
    assert events == ["TTSRequested", "SpeechStarted", "SpeechFinished"]


def test_speech_queue_interrupt_clears_pending_items() -> None:
    queue = SpeechQueueService(
        event_bus=EventBus(),
        tts_provider=FakeTTSProvider(),
        audio_player=FakeAudioPlayer(),
    )

    asyncio.run(queue.enqueue(TTSRequest(text="one")))
    asyncio.run(queue.enqueue(TTSRequest(text="two")))
    result = asyncio.run(queue.interrupt(reason="new_user_input"))

    assert result.cleared_items == 2
    assert result.interrupted_item_id is None
    assert queue.pending_count == 0


def test_speech_queue_interrupts_active_playback() -> None:
    async def run_scenario() -> SpeechQueueStatus:
        player = BlockingAudioPlayer()
        queue = SpeechQueueService(
            event_bus=EventBus(),
            tts_provider=FakeTTSProvider(),
            audio_player=player,
        )
        await queue.enqueue(TTSRequest(text="hello"))
        drain_task = asyncio.create_task(queue.drain_once())
        await player.started.wait()

        result = await queue.interrupt(reason="new_user_input")
        drained_item = await drain_task

        assert result.interrupted_item_id is not None
        assert player.interrupted is True
        assert drained_item is not None
        return drained_item.status

    assert asyncio.run(run_scenario()) is SpeechQueueStatus.INTERRUPTED


@dataclass(slots=True)
class BlockingAudioPlayer:
    started: asyncio.Event = field(default_factory=asyncio.Event)
    interrupted: bool = False
    played_audio: SpeechAudio | None = None

    async def play(self, audio: SpeechAudio) -> None:
        self.played_audio = audio
        self.started.set()
        while not self.interrupted:
            await asyncio.sleep(0.001)

    async def interrupt(self) -> None:
        self.interrupted = True
