from __future__ import annotations

import pytest

from private_ai_companion.__main__ import main


def test_entrypoint_returns_success(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(()) == 0
    captured = capsys.readouterr()
    assert "Runtime lifecycle completed with state: stopped." in captured.out


def test_entrypoint_version_returns_success(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("--version",)) == 0
    captured = capsys.readouterr()
    assert "private-ai-companion 0.0.0" in captured.out
