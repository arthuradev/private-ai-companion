from __future__ import annotations

from private_ai_companion.brain import (
    ContextBuilder,
    ConversationMessage,
    ConversationRole,
)


def test_context_builder_trims_user_text_and_session_notes() -> None:
    builder = ContextBuilder()

    context = builder.build_for_user_text(
        " hello ",
        recent_messages=(
            ConversationMessage(role=ConversationRole.USER, content="previous"),
        ),
        session_notes=(" keep ", "", "private "),
    )

    assert context.user_message == "hello"
    assert context.recent_messages == (
        ConversationMessage(role=ConversationRole.USER, content="previous"),
    )
    assert context.session_notes == ("keep", "private")
