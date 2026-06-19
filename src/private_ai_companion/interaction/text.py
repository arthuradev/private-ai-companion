from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

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


class TextResponder(Protocol):
    async def respond(self, message: UserTextMessage) -> AssistantTextMessage:
        """Return a local assistant message for a user text message."""
        ...


class Phase03TextResponder:
    async def respond(self, message: UserTextMessage) -> AssistantTextMessage:
        if not message.text:
            return AssistantTextMessage(
                text="Nao recebi texto nessa mensagem. Pode tentar de novo?"
            )

        return AssistantTextMessage(
            text=(
                "Recebi sua mensagem. A conversa com LLM configuravel sera "
                "implementada nas proximas fases."
            )
        )


class TextInteractionService:
    def __init__(
        self,
        *,
        event_bus: EventBus,
        responder: TextResponder | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._responder = responder or Phase03TextResponder()

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

        assistant = await self._responder.respond(user)
        await self._event_bus.publish(
            AssistantTextReady(
                text=assistant.text,
                metadata=EventMetadata(
                    source="interaction",
                    sensitivity=EventSensitivity.INTERNAL,
                ),
            )
        )

        return TextTurn(user=user, assistant=assistant)
