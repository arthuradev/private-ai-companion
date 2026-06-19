from __future__ import annotations

import asyncio

from private_ai_companion.adapters.llm import FakeLLMProvider
from private_ai_companion.brain import (
    ContextBuilder,
    LLMGenerationRequest,
    PromptBuilder,
    default_persona_profile,
)


def test_fake_llm_provider_generates_local_response_without_external_calls() -> None:
    prompt = PromptBuilder().build(
        persona=default_persona_profile(),
        context=ContextBuilder().build_for_user_text("hello"),
    )
    provider = FakeLLMProvider()

    response = asyncio.run(provider.generate(LLMGenerationRequest(prompt=prompt)))

    assert response.provider_id == "fake-local"
    assert response.model == "fake-local-v0"
    assert "Resposta fake local" in response.text
    assert "Nenhum provedor externo foi chamado" in response.text
    assert response.usage.prompt_tokens > 0
    assert response.usage.completion_tokens > 0
