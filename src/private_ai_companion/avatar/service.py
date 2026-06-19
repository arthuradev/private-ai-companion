from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.avatar.models import (
    AvatarExpression,
    AvatarExpressionRequest,
    AvatarIdleState,
    AvatarLipsyncFrame,
    AvatarProviderResult,
    AvatarProviderStatus,
)
from private_ai_companion.avatar.ports import AvatarProvider
from private_ai_companion.core import (
    AvatarLipsyncUpdated,
    AvatarStateApplied,
    AvatarStateRequested,
    EventBus,
    EventMetadata,
)


@dataclass(frozen=True, slots=True)
class AvatarServiceSettings:
    enabled: bool
    idle: AvatarIdleState
    lipsync_parameter_name: str
    lipsync_weight: float


class AvatarService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        provider: AvatarProvider,
        settings: AvatarServiceSettings,
    ) -> None:
        self._event_bus = event_bus
        self._provider = provider
        self._settings = settings
        self._current_expression = settings.idle.expression

    @property
    def provider_id(self) -> str:
        return self._provider.provider_id

    @property
    def current_expression(self) -> AvatarExpression:
        return self._current_expression

    async def connect(self) -> None:
        if self._settings.enabled:
            await self._provider.connect()

    async def disconnect(self) -> None:
        if self._settings.enabled:
            await self._provider.disconnect()

    async def apply_expression(
        self,
        expression: AvatarExpression,
        *,
        reason: str = "state_requested",
        intensity: float = 1.0,
        transition_seconds: float = 0.2,
    ) -> AvatarProviderResult:
        request = AvatarExpressionRequest(
            expression=expression,
            intensity=_clamp_ratio(intensity),
            transition_seconds=max(0.0, transition_seconds),
            reason=reason,
        )
        await self._event_bus.publish(
            AvatarStateRequested(
                expression=request.expression.value,
                reason=request.reason,
                intensity=request.intensity,
                metadata=EventMetadata(source="avatar"),
            )
        )

        if not self._settings.enabled:
            result = AvatarProviderResult(
                provider_id=self._provider.provider_id,
                status=AvatarProviderStatus.SKIPPED,
                expression=request.expression,
                detail="avatar_disabled",
                request_id=request.request_id,
            )
        else:
            result = await self._provider.apply_expression(request)

        if result.status is AvatarProviderStatus.APPLIED:
            self._current_expression = expression

        await self._event_bus.publish(
            AvatarStateApplied(
                expression=expression.value,
                provider_id=result.provider_id,
                status=result.status.value,
                metadata=EventMetadata(source="avatar"),
            )
        )
        return result

    async def apply_idle(self) -> AvatarProviderResult:
        return await self.apply_expression(
            self._settings.idle.expression,
            reason="idle",
            intensity=1.0,
        )

    async def apply_lipsync(self, mouth_open: float) -> AvatarProviderResult:
        frame = AvatarLipsyncFrame(
            mouth_open=_clamp_ratio(mouth_open),
            parameter_name=self._settings.lipsync_parameter_name,
            weight=_clamp_ratio(self._settings.lipsync_weight),
        )

        if not self._settings.enabled:
            result = AvatarProviderResult(
                provider_id=self._provider.provider_id,
                status=AvatarProviderStatus.SKIPPED,
                detail="avatar_disabled",
                request_id=frame.request_id,
            )
        else:
            result = await self._provider.apply_lipsync(frame)

        await self._event_bus.publish(
            AvatarLipsyncUpdated(
                parameter_name=frame.parameter_name,
                value=frame.mouth_open,
                provider_id=result.provider_id,
                metadata=EventMetadata(source="avatar"),
            )
        )
        return result


def _clamp_ratio(value: float) -> float:
    return min(1.0, max(0.0, value))
