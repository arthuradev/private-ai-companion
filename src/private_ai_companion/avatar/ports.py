from __future__ import annotations

from typing import Protocol

from private_ai_companion.avatar.models import (
    AvatarExpressionRequest,
    AvatarLipsyncFrame,
    AvatarProviderResult,
)


class AvatarProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable avatar provider id."""
        ...

    async def connect(self) -> None:
        """Prepare the provider connection if needed."""
        ...

    async def disconnect(self) -> None:
        """Close the provider connection if needed."""
        ...

    async def apply_expression(
        self,
        request: AvatarExpressionRequest,
    ) -> AvatarProviderResult:
        """Apply a visual expression or presentation state."""
        ...

    async def apply_lipsync(
        self,
        frame: AvatarLipsyncFrame,
    ) -> AvatarProviderResult:
        """Apply one lipsync frame."""
        ...
