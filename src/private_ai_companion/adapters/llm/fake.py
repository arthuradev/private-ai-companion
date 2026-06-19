from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.brain import (
    LLMGenerationRequest,
    LLMGenerationResponse,
    LLMProviderKind,
    LLMUsage,
    PromptRole,
)


@dataclass(frozen=True, slots=True)
class FakeLLMProvider:
    provider_id: str = "fake-local"
    model: str = "fake-local-v0"

    @property
    def kind(self) -> LLMProviderKind:
        return LLMProviderKind.FAKE

    async def generate(
        self,
        request: LLMGenerationRequest,
    ) -> LLMGenerationResponse:
        prompt_text = request.prompt.as_text()
        user_text = self._latest_user_text(request)
        response_text = (
            "Resposta fake local: recebi sua mensagem"
            f"{f' ({user_text})' if user_text else ''}. "
            "Nenhum provedor externo foi chamado."
        )
        return LLMGenerationResponse(
            text=response_text,
            provider_id=self.provider_id,
            model=request.model or self.model,
            usage=LLMUsage(
                prompt_tokens=self._estimate_tokens(prompt_text),
                completion_tokens=self._estimate_tokens(response_text),
            ),
        )

    @staticmethod
    def _latest_user_text(request: LLMGenerationRequest) -> str:
        for message in reversed(request.prompt.messages):
            if message.role is PromptRole.USER:
                return message.content.split("User message:\n", maxsplit=1)[-1].split(
                    "\n",
                    maxsplit=1,
                )[0]
        return ""

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return len(text.split())
