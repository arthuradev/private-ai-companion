from __future__ import annotations

import asyncio
from dataclasses import dataclass

import pytest

from private_ai_companion.adapters.llm import FakeLLMProvider
from private_ai_companion.brain import (
    ContextBuilder,
    LLMGenerationRequest,
    LLMGenerationResponse,
    LLMProviderError,
    LLMProviderKind,
    LLMRouter,
    LLMRoutingError,
    PromptBuilder,
    PromptBundle,
    default_persona_profile,
)


@dataclass(frozen=True, slots=True)
class BrokenProvider:
    provider_id: str = "broken"
    model: str = "broken-model"

    @property
    def kind(self) -> LLMProviderKind:
        return LLMProviderKind.FAKE

    async def generate(
        self,
        request: LLMGenerationRequest,
    ) -> LLMGenerationResponse:
        _ = request
        raise LLMProviderError("not available")


def test_llm_router_uses_default_provider() -> None:
    router = LLMRouter(
        providers=(FakeLLMProvider(),),
        default_provider_id="fake-local",
    )

    response = asyncio.run(router.generate(sample_prompt()))

    assert response.provider_id == "fake-local"
    assert "Resposta fake local" in response.text


def test_llm_router_falls_back_after_provider_error() -> None:
    router = LLMRouter(
        providers=(BrokenProvider(), FakeLLMProvider(provider_id="fallback")),
        default_provider_id="broken",
        fallback_provider_ids=("fallback",),
    )

    response = asyncio.run(router.generate(sample_prompt()))

    assert response.provider_id == "fallback"


def test_llm_router_reports_failures_when_no_provider_can_generate() -> None:
    router = LLMRouter(
        providers=(BrokenProvider(),),
        default_provider_id="broken",
        fallback_provider_ids=("missing",),
    )

    with pytest.raises(LLMRoutingError) as exc_info:
        asyncio.run(router.generate(sample_prompt()))

    assert "broken" in str(exc_info.value)
    assert "missing" in str(exc_info.value)


def sample_prompt() -> PromptBundle:
    return PromptBuilder().build(
        persona=default_persona_profile(),
        context=ContextBuilder().build_for_user_text("hello"),
    )
