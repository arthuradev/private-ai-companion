from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from private_ai_companion.brain.prompt_builder import PromptBundle


class LLMProviderKind(StrEnum):
    FAKE = "fake"
    LOCAL = "local"
    CLOUD = "cloud"


@dataclass(frozen=True, slots=True)
class LLMUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0


@dataclass(frozen=True, slots=True)
class LLMGenerationRequest:
    prompt: PromptBundle
    model: str | None = None


@dataclass(frozen=True, slots=True)
class LLMGenerationResponse:
    text: str
    provider_id: str
    model: str
    usage: LLMUsage


class LLMProvider(Protocol):
    @property
    def provider_id(self) -> str:
        """Stable provider id used by routing config."""
        ...

    @property
    def kind(self) -> LLMProviderKind:
        """Provider locality/category."""
        ...

    @property
    def model(self) -> str:
        """Configured model name."""
        ...

    async def generate(
        self,
        request: LLMGenerationRequest,
    ) -> LLMGenerationResponse:
        """Generate text for a prompt bundle."""
        ...
