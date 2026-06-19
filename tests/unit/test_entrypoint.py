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
