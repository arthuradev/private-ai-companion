from __future__ import annotations

from collections import deque
from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from private_ai_companion.core import (
    EventBus,
    EventMetadata,
    EventSensitivity,
    SpeechFinished,
    SpeechInterrupted,
    SpeechStarted,
    TTSRequested,
)
from private_ai_companion.speech.models import (
    SpeechInterruptResult,
    SpeechQueueItem,
    SpeechQueueStatus,
    TTSRequest,
)
from private_ai_companion.speech.ports import AudioPlayer, TTSProvider


class SpeechQueueService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        tts_provider: TTSProvider,
        audio_player: AudioPlayer,
    ) -> None:
        self._event_bus = event_bus
        self._tts_provider = tts_provider
        self._audio_player = audio_player
        self._queue: deque[SpeechQueueItem] = deque()
        self._current_item: SpeechQueueItem | None = None
        self._interrupted_item_ids: set[str] = set()

    @property
    def pending_count(self) -> int:
        return len(self._queue)

    @property
    def current_item(self) -> SpeechQueueItem | None:
        return self._current_item

    async def enqueue(self, request: TTSRequest) -> SpeechQueueItem:
        item = SpeechQueueItem(
            item_id=str(uuid4()),
            request=request,
            status=SpeechQueueStatus.QUEUED,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        self._queue.append(item)
        await self._event_bus.publish(
            TTSRequested(
                text=request.text,
                voice_id=request.voice_id,
                metadata=EventMetadata(
                    source="speech",
                    sensitivity=EventSensitivity.PRIVATE,
                ),
            )
        )
        return item

    async def drain_once(self) -> SpeechQueueItem | None:
        if not self._queue:
            return None

        item = self._set_current(self._queue.popleft(), SpeechQueueStatus.SYNTHESIZING)
        audio = await self._tts_provider.synthesize(item.request)

        item = self._set_current(item, SpeechQueueStatus.PLAYING)
        await self._event_bus.publish(
            SpeechStarted(
                item_id=item.item_id,
                metadata=EventMetadata(source="speech"),
            )
        )
        await self._audio_player.play(audio)

        if item.item_id in self._interrupted_item_ids:
            self._interrupted_item_ids.remove(item.item_id)
            interrupted = replace(
                item,
                status=SpeechQueueStatus.INTERRUPTED,
                updated_at=datetime.now(UTC),
            )
            self._current_item = None
            return interrupted

        finished = self._set_current(item, SpeechQueueStatus.FINISHED)
        await self._event_bus.publish(
            SpeechFinished(
                item_id=finished.item_id,
                metadata=EventMetadata(source="speech"),
            )
        )
        self._current_item = None
        return finished

    async def drain_all(self) -> tuple[SpeechQueueItem, ...]:
        drained: list[SpeechQueueItem] = []
        while self._queue:
            item = await self.drain_once()
            if item is not None:
                drained.append(item)
        return tuple(drained)

    async def interrupt(
        self,
        *,
        reason: str = "user_interrupted",
    ) -> SpeechInterruptResult:
        cleared_items = len(self._queue)
        self._queue.clear()
        interrupted_item_id: str | None = None

        if self._current_item is not None:
            interrupted = self._set_current(
                self._current_item,
                SpeechQueueStatus.INTERRUPTED,
            )
            interrupted_item_id = interrupted.item_id
            self._interrupted_item_ids.add(interrupted.item_id)
            await self._audio_player.interrupt()
            self._current_item = None

        result = SpeechInterruptResult(
            interrupted_item_id=interrupted_item_id,
            cleared_items=cleared_items,
            reason=reason,
        )
        await self._event_bus.publish(
            SpeechInterrupted(
                reason=reason,
                interrupted_item_id=interrupted_item_id,
                cleared_items=cleared_items,
                metadata=EventMetadata(source="speech"),
            )
        )
        return result

    def _set_current(
        self,
        item: SpeechQueueItem,
        status: SpeechQueueStatus,
    ) -> SpeechQueueItem:
        updated = replace(
            item,
            status=status,
            updated_at=datetime.now(UTC),
        )
        self._current_item = updated
        return updated
