from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ConversationRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class ConversationMessage:
    role: ConversationRole
    content: str


@dataclass(frozen=True, slots=True)
class PromptContext:
    user_message: str
    recent_messages: tuple[ConversationMessage, ...] = ()
    session_notes: tuple[str, ...] = ()


class ContextBuilder:
    def build_for_user_text(
        self,
        text: str,
        *,
        recent_messages: tuple[ConversationMessage, ...] = (),
        session_notes: tuple[str, ...] = (),
    ) -> PromptContext:
        return PromptContext(
            user_message=text.strip(),
            recent_messages=recent_messages,
            session_notes=tuple(note.strip() for note in session_notes if note.strip()),
        )
