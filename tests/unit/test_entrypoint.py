from __future__ import annotations

from private_ai_companion.__main__ import main


def test_entrypoint_returns_success() -> None:
    assert main(()) == 0


def test_entrypoint_version_returns_success() -> None:
    assert main(("--version",)) == 0
