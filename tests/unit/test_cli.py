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


def test_cli_screen_context_renders_temporary_context() -> None:
    console = Console(record=True, width=120, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(cli.run_screen_context("manual_test"))
    output = console.export_text()

    assert exit_code == 0
    assert "Tela: contexto temporario via fake-vision" in output
    assert "Contexto visual fake local" in output
    assert "Redaction: sem achados" in output


def test_cli_desktop_action_renders_dry_run() -> None:
    console = Console(record=True, width=120, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(
        cli.run_desktop_action(
            action_type="desktop.open_allowed_app",
            parameters={"app_id": "calculator"},
            user_confirmed=False,
            dry_run_only=True,
        )
    )
    output = console.export_text()

    assert exit_code == 0
    assert "Acao desktop: dry_run (medium)" in output
    assert "Open allowed app 'Calculator'" in output


def test_cli_skill_renders_status() -> None:
    console = Console(record=True, width=120, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(
        cli.run_skill(
            skill_id="builtin.status",
            skill_input={},
            user_confirmed=False,
            dry_run_only=False,
        )
    )
    output = console.export_text()

    assert exit_code == 0
    assert "Skill: builtin.status (completed)" in output
    assert "status: ready" in output


def test_cli_skill_renders_effect_dry_run() -> None:
    console = Console(record=True, width=120, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(
        cli.run_skill(
            skill_id="builtin.open_allowed_app",
            skill_input={"app_id": "calculator"},
            user_confirmed=False,
            dry_run_only=True,
        )
    )
    output = console.export_text()

    assert exit_code == 0
    assert "Skill: builtin.open_allowed_app (completed)" in output
    assert "Effect: desktop_action dry_run" in output


def test_cli_dashboard_renders_local_dashboard() -> None:
    console = Console(record=True, width=120, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(cli.run_dashboard())
    output = console.export_text()

    assert exit_code == 0
    assert "Dashboard local" in output
    assert "Permissoes e acoes locais" in output


def test_cli_tray_status_renders_menu() -> None:
    console = Console(record=True, width=120, force_terminal=False)
    cli = RichCliApp(application=create_application(), console=console)

    exit_code = asyncio.run(cli.run_tray_status())
    output = console.export_text()

    assert exit_code == 0
    assert "Tray status" in output
    assert "Abrir dashboard" in output
