from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from private_ai_companion.brain import (
    ContextBuilder,
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


class Phase03TextResponder:
    def __init__(self, *, persona: PersonaProfile) -> None:
        self._persona = persona

    async def respond(
        self,
        message: UserTextMessage,
        prompt: PromptBundle,
    ) -> AssistantTextMessage:
        _ = prompt
        if not message.text:
            return AssistantTextMessage(
                text="Nao recebi texto nessa mensagem. Pode tentar de novo?"
            )

        return AssistantTextMessage(
            text=(
                f"Recebi sua mensagem. A persona atual e {self._persona.display_name}. "
                "A conversa com LLM configuravel sera implementada nas proximas fases."
            )
        )


class TextInteractionService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        persona: PersonaProfile,
        context_builder: ContextBuilder | None = None,
        prompt_builder: PromptBuilder | None = None,
        responder: TextResponder | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._persona = persona
        self._context_builder = context_builder or ContextBuilder()
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._responder = responder or Phase03TextResponder(persona=persona)

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
