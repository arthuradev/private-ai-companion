from __future__ import annotations

from dataclasses import dataclass, field

from private_ai_companion.avatar import (
    AvatarExpressionRequest,
    AvatarLipsyncFrame,
    AvatarProviderResult,
    AvatarProviderStatus,
)


def empty_expression_requests() -> list[AvatarExpressionRequest]:
    return []


def empty_lipsync_frames() -> list[AvatarLipsyncFrame]:
    return []


@dataclass(slots=True)
class FakeAvatarProvider:
    provider_id: str = "fake-avatar"
    connected: bool = False
    expressions: list[AvatarExpressionRequest] = field(
        default_factory=empty_expression_requests
    )
    lipsync_frames: list[AvatarLipsyncFrame] = field(
        default_factory=empty_lipsync_frames
    )

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def apply_expression(
        self,
        request: AvatarExpressionRequest,
    ) -> AvatarProviderResult:
        self.expressions.append(request)
        return AvatarProviderResult(
            provider_id=self.provider_id,
            status=AvatarProviderStatus.APPLIED,
            expression=request.expression,
            detail="fake_avatar_expression_applied",
            request_id=request.request_id,
        )

    async def apply_lipsync(
        self,
        frame: AvatarLipsyncFrame,
    ) -> AvatarProviderResult:
        self.lipsync_frames.append(frame)
        return AvatarProviderResult(
            provider_id=self.provider_id,
            status=AvatarProviderStatus.APPLIED,
            detail="fake_avatar_lipsync_applied",
            request_id=frame.request_id,
        )
