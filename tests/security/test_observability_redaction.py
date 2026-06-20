from __future__ import annotations

import asyncio

from private_ai_companion.bootstrap import create_application


def test_observability_does_not_retain_private_turn_text() -> None:
    application = create_application()

    asyncio.run(application.handle_user_text("my secret token is abc123"))

    diagnostics = application.diagnostics_snapshot()
    replay_text = repr(diagnostics.replay_records)
    log_text = "\n".join(record.to_json_line() for record in diagnostics.log_records)

    assert "my secret token is abc123" not in replay_text
    assert "my secret token is abc123" not in log_text
    assert "Resposta fake local" not in replay_text
    assert "Resposta fake local" not in log_text
