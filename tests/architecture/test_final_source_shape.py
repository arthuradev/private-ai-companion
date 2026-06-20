from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PACKAGE_ROOT = REPO_ROOT / "src" / "private_ai_companion"


def test_project_does_not_use_a_giant_main_py() -> None:
    assert not (REPO_ROOT / "main.py").exists()
    assert not (PACKAGE_ROOT / "main.py").exists()


def test_entrypoint_stays_a_thin_cli_boundary() -> None:
    entrypoint_lines = (
        (PACKAGE_ROOT / "__main__.py").read_text(encoding="utf-8").splitlines()
    )

    assert len(entrypoint_lines) <= 320


def test_runtime_modules_have_explicit_packages() -> None:
    expected_modules = (
        "adapters",
        "avatar",
        "bootstrap",
        "brain",
        "config",
        "core",
        "desktop",
        "interaction",
        "memory",
        "observability",
        "safety",
        "skills",
        "speech",
        "ui",
        "vision",
    )

    missing = [
        module
        for module in expected_modules
        if not (PACKAGE_ROOT / module / "__init__.py").exists()
    ]

    assert missing == []
