from __future__ import annotations

import asyncio

from private_ai_companion.adapters.avatar import FakeAvatarProvider
from private_ai_companion.avatar import (
    AvatarExpression,
    AvatarExpressionRequest,
    AvatarLipsyncFrame,
    AvatarProviderStatus,
)


def test_fake_avatar_provider_records_expression_and_lipsync() -> None:
    provider = FakeAvatarProvider()

    asyncio.run(provider.connect())
    expression_result = asyncio.run(
        provider.apply_expression(
            AvatarExpressionRequest(expression=AvatarExpression.HAPPY)
        )
    )
    lipsync_result = asyncio.run(
        provider.apply_lipsync(AvatarLipsyncFrame(mouth_open=0.75))
    )

    assert provider.connected is True
    assert expression_result.status is AvatarProviderStatus.APPLIED
    assert lipsync_result.status is AvatarProviderStatus.APPLIED
    assert provider.expressions[0].expression is AvatarExpression.HAPPY
    assert provider.lipsync_frames[0].mouth_open == 0.75
