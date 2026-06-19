from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from private_ai_companion.brain import (
    ContextBuilder,
    LLMRouter,
    PersonaProfile,
    PromptBuilder,
    PromptBundle,
)
from private_ai_companion.core import (
    AssistantTextReady,
    EventBus,
    EventMetadata,
    EventSensitivity,
    UserTextReceived,
)


@dataclass(frozen=True, slots=True)
class UserTextMessage:
    text: str


@dataclass(frozen=True, slots=True)
class AssistantTextMessage:
    text: str


@dataclass(frozen=True, slots=True)
class TextTurn:
    user: UserTextMessage
    assistant: AssistantTextMessage
    prompt: PromptBundle


class TextResponder(Protocol):
    async def respond(
        self,
        message: UserTextMessage,
        prompt: PromptBundle,
    ) -> AssistantTextMessage:
        """Return a local assistant message for a user text message."""
        ...


class LLMTextResponder:
    def __init__(self, *, router: LLMRouter) -> None:
        self._router = router

    async def respond(
        self,
        message: UserTextMessage,
        prompt: PromptBundle,
    ) -> AssistantTextMessage:
        if not message.text:
            return AssistantTextMessage(
                text="Nao recebi texto nessa mensagem. Pode tentar de novo?"
            )

        response = await self._router.generate(prompt)
        return AssistantTextMessage(text=response.text)


class TextInteractionService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        persona: PersonaProfile,
        llm_router: LLMRouter,
        responder: TextResponder | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._persona = persona
        self._context_builder = ContextBuilder()
        self._prompt_builder = PromptBuilder()
        self._responder = responder or LLMTextResponder(router=llm_router)

    async def handle_user_text(self, text: str) -> TextTurn:
        user = UserTextMessage(text=text.strip())
        await self._event_bus.publish(
            UserTextReceived(
                text=user.text,
                metadata=EventMetadata(
                    source="interaction",
                    sensitivity=EventSensitivity.PRIVATE,
                ),
            )
        )

        context = self._context_builder.build_for_user_text(user.text)
        prompt = self._prompt_builder.build(persona=self._persona, context=context)
        assistant = await self._responder.respond(user, prompt)
        await self._event_bus.publish(
            AssistantTextReady(
                text=assistant.text,
                metadata=EventMetadata(
                    source="interaction",
                    sensitivity=EventSensitivity.INTERNAL,
                ),
            )
        )

        return TextTurn(user=user, assistant=assistant, prompt=prompt)
