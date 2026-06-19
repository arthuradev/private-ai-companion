from __future__ import annotations

from collections.abc import Iterable

from private_ai_companion.brain.errors import LLMProviderError, LLMRoutingError
from private_ai_companion.brain.llm import (
    LLMGenerationRequest,
    LLMGenerationResponse,
    LLMProvider,
)
from private_ai_companion.brain.prompt_builder import PromptBundle


class LLMRouter:
    def __init__(
        self,
        *,
        providers: Iterable[LLMProvider],
        default_provider_id: str,
        fallback_provider_ids: tuple[str, ...] = (),
    ) -> None:
        self._providers = {provider.provider_id: provider for provider in providers}
        self._default_provider_id = default_provider_id
        self._fallback_provider_ids = fallback_provider_ids

    @property
    def provider_ids(self) -> tuple[str, ...]:
        return tuple(self._providers)

    async def generate(
        self,
        prompt: PromptBundle,
        *,
        preferred_provider_id: str | None = None,
    ) -> LLMGenerationResponse:
        failures: list[str] = []

        for provider_id in self._route(preferred_provider_id):
            provider = self._providers.get(provider_id)
            if provider is None:
                failures.append(f"{provider_id}: provider is not registered")
                continue

            try:
                return await provider.generate(
                    LLMGenerationRequest(prompt=prompt, model=provider.model)
                )
            except LLMProviderError as error:
                failures.append(f"{provider_id}: {error}")

        failure_text = "; ".join(failures) if failures else "no providers configured"
        raise LLMRoutingError(f"LLM routing failed: {failure_text}")

    def _route(self, preferred_provider_id: str | None) -> tuple[str, ...]:
        route: list[str] = []
        if preferred_provider_id:
            route.append(preferred_provider_id)
        route.append(self._default_provider_id)
        route.extend(self._fallback_provider_ids)
        return tuple(dict.fromkeys(route))
