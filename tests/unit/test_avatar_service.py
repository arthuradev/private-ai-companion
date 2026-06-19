from __future__ import annotations

import asyncio

from private_ai_companion.adapters.avatar import FakeAvatarProvider
from private_ai_companion.avatar import (
    AvatarExpression,
    AvatarIdleState,
    AvatarProviderStatus,
    AvatarService,
    AvatarServiceSettings,
)
from private_ai_companion.core import BaseEvent, EventBus


def test_avatar_service_applies_expression_and_publishes_events() -> None:
    event_bus = EventBus()
    provider = FakeAvatarProvider()
    service = AvatarService(
        event_bus=event_bus,
        provider=provider,
        settings=AvatarServiceSettings(
            enabled=True,
            idle=AvatarIdleState(enabled=True),
            lipsync_parameter_name="MouthOpen",
            lipsync_weight=1.0,
        ),
    )
    events: list[str] = []

    def record_event(event: BaseEvent) -> None:
        events.append(event.name)

    event_bus.subscribe(BaseEvent, record_event)

    result = asyncio.run(
        service.apply_expression(
            AvatarExpression.CURIOUS,
            reason="test",
            intensity=1.5,
        )
    )

    assert result.status is AvatarProviderStatus.APPLIED
    assert service.current_expression is AvatarExpression.CURIOUS
    assert provider.expressions[0].intensity == 1.0
    assert events == ["AvatarStateRequested", "AvatarStateApplied"]


def test_avatar_service_applies_lipsync_frame() -> None:
    provider = FakeAvatarProvider()
    service = AvatarService(
        event_bus=EventBus(),
        provider=provider,
        settings=AvatarServiceSettings(
            enabled=True,
            idle=AvatarIdleState(enabled=True),
            lipsync_parameter_name="MouthOpen",
            lipsync_weight=0.5,
        ),
    )

    result = asyncio.run(service.apply_lipsync(2.0))

    assert result.status is AvatarProviderStatus.APPLIED
    assert provider.lipsync_frames[0].mouth_open == 1.0
    assert provider.lipsync_frames[0].weight == 0.5


def test_avatar_service_skips_provider_when_disabled() -> None:
    provider = FakeAvatarProvider()
    service = AvatarService(
        event_bus=EventBus(),
        provider=provider,
        settings=AvatarServiceSettings(
            enabled=False,
            idle=AvatarIdleState(enabled=True),
            lipsync_parameter_name="MouthOpen",
            lipsync_weight=1.0,
        ),
    )

    result = asyncio.run(service.apply_expression(AvatarExpression.HAPPY))

    assert result.status is AvatarProviderStatus.SKIPPED
    assert provider.expressions == []
