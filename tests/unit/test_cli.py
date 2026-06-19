from __future__ import annotations

import asyncio
from pathlib import Path

from rich.console import Console

from private_ai_companion.avatar import AvatarExpression
from private_ai_companion.bootstrap import create_application
from private_ai_companion.ui import RichCliApp


def test_cli_single_turn_renders_banner_and_local_response() -> None:
    console = Console(record=True, width=100, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(cli.run_single_turn("ola"))
    output = console.export_text()

    assert exit_code == 0
    assert "private-ai-companion" in output
    assert "CLI inicial com Rich/Pyfiglet" in output
    assert "persona configuravel" in output
    assert "Voce: ola" in output
    assert "Resposta fake local" in output


def test_cli_interactive_exits_on_command() -> None:
    console = Console(record=True, width=100, force_terminal=False)
    cli = RichCliApp(
        application=create_application(),
        console=console,
        input_reader=lambda _prompt: "/exit",
    )

    exit_code = asyncio.run(cli.run_interactive())
    output = console.export_text()

    assert exit_code == 0
    assert "private-ai-companion" in output
    assert "Encerrando." in output


def test_cli_voice_file_transcribes_and_renders_response(tmp_path: Path) -> None:
    voice_file = tmp_path / "voice.txt"
    voice_file.write_text("ola por voz", encoding="utf-8")
    console = Console(record=True, width=100, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(cli.run_voice_file(voice_file))
    output = console.export_text()

    assert exit_code == 0
    assert "Voz transcrita: ola por voz" in output
    assert "Resposta fake local" in output


def test_cli_avatar_expression_renders_result() -> None:
    console = Console(record=True, width=100, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(cli.run_avatar_expression(AvatarExpression.HAPPY))
    output = console.export_text()

    assert exit_code == 0
    assert "Avatar: happy via fake-avatar (applied)" in output
