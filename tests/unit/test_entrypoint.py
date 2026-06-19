from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.__main__ import main


def test_entrypoint_single_turn_returns_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("--once", "hello")) == 0
    captured = capsys.readouterr()
    assert "private-ai-companion" in captured.out
    assert "Resposta fake local" in captured.out


def test_entrypoint_version_returns_success(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("--version",)) == 0
    captured = capsys.readouterr()
    assert "private-ai-companion 0.0.0" in captured.out


def test_entrypoint_voice_file_returns_success(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    voice_file = tmp_path / "voice.txt"
    voice_file.write_text("hello voice", encoding="utf-8")

    assert main(("--voice-file", str(voice_file))) == 0

    captured = capsys.readouterr()
    assert "Voz transcrita: hello voice" in captured.out
    assert "Resposta fake local" in captured.out


def test_entrypoint_rejects_text_and_voice_file_together(tmp_path: Path) -> None:
    voice_file = tmp_path / "voice.txt"
    voice_file.write_text("hello voice", encoding="utf-8")

    with pytest.raises(SystemExit) as error:
        main(("--once", "hello", "--voice-file", str(voice_file)))

    assert error.value.code == 2


def test_entrypoint_avatar_expression_returns_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("--avatar-expression", "happy")) == 0

    captured = capsys.readouterr()
    assert "Avatar: happy via fake-avatar (applied)" in captured.out


def test_entrypoint_screen_context_returns_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("--screen-context", "--screen-purpose", "manual_test")) == 0

    captured = capsys.readouterr()
    assert "Tela: contexto temporario via fake-vision" in captured.out
    assert "Contexto visual fake local" in captured.out


def test_entrypoint_desktop_action_dry_run_returns_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "--desktop-action",
                "open-allowed-app",
                "--app-id",
                "calculator",
                "--desktop-dry-run",
            )
        )
        == 0
    )

    captured = capsys.readouterr()
    assert "Acao desktop: dry_run (medium)" in captured.out
    assert "Open allowed app 'Calculator'" in captured.out


def test_entrypoint_skill_status_returns_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("--skill", "builtin.status")) == 0

    captured = capsys.readouterr()
    assert "Skill: builtin.status (completed)" in captured.out
    assert "status: ready" in captured.out


def test_entrypoint_skill_effect_dry_run_returns_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "--skill",
                "builtin.open_allowed_app",
                "--skill-input",
                "app_id=calculator",
                "--skill-dry-run",
            )
        )
        == 0
    )

    captured = capsys.readouterr()
    assert "Skill: builtin.open_allowed_app (completed)" in captured.out
    assert "Effect: desktop_action dry_run" in captured.out


def test_entrypoint_rejects_multiple_single_actions(tmp_path: Path) -> None:
    voice_file = tmp_path / "voice.txt"
    voice_file.write_text("hello voice", encoding="utf-8")

    with pytest.raises(SystemExit) as error:
        main(
            (
                "--voice-file",
                str(voice_file),
                "--avatar-expression",
                "happy",
            )
        )

    assert error.value.code == 2


def test_entrypoint_rejects_text_and_screen_context_together() -> None:
    with pytest.raises(SystemExit) as error:
        main(("--once", "hello", "--screen-context"))

    assert error.value.code == 2


def test_entrypoint_rejects_text_and_desktop_action_together() -> None:
    with pytest.raises(SystemExit) as error:
        main(("--once", "hello", "--desktop-action", "read-active-window-title"))

    assert error.value.code == 2


def test_entrypoint_rejects_text_and_skill_together() -> None:
    with pytest.raises(SystemExit) as error:
        main(("--once", "hello", "--skill", "builtin.status"))

    assert error.value.code == 2


def test_entrypoint_rejects_create_note_without_title() -> None:
    with pytest.raises(SystemExit) as error:
        main(("--desktop-action", "create-note"))

    assert error.value.code == 2


def test_entrypoint_rejects_malformed_skill_input() -> None:
    with pytest.raises(SystemExit) as error:
        main(("--skill", "builtin.status", "--skill-input", "broken"))

    assert error.value.code == 2
