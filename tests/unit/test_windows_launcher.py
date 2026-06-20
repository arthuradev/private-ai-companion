from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
START_BAT = REPO_ROOT / "Start.bat"
RELEASE_CHECK = REPO_ROOT / "scripts" / "release-check.ps1"


def test_start_bat_delegates_to_locked_official_entrypoint() -> None:
    launcher = START_BAT.read_text(encoding="utf-8")

    assert "uv run --locked private-ai-companion %*" in launcher
    assert "py -3 -c" in launcher
    assert "sys.version_info >= (3, 12)" in launcher


def test_start_bat_logs_startup_without_logging_arguments() -> None:
    launcher = START_BAT.read_text(encoding="utf-8")

    assert 'set "LAUNCHER_LOG_DIR=logs"' in launcher
    assert 'set "LAUNCHER_LOG=%LAUNCHER_LOG_DIR%\\startup.log"' in launcher
    assert "Secrets stay local and are not logged." in launcher
    assert "uv will sync locked dependencies if needed." in launcher
    assert "call :log %*" not in launcher
    assert "echo %*" not in launcher


def test_start_bat_has_no_product_or_dangerous_logic() -> None:
    launcher = START_BAT.read_text(encoding="utf-8").lower()

    forbidden_fragments = (
        "openai",
        "anthropic",
        "vtube",
        "sqlite",
        "screen-context",
        "desktop-action",
        "skill-input",
        " del ",
        " rmdir ",
        " rd /",
        "curl ",
    )

    for fragment in forbidden_fragments:
        assert fragment not in launcher


def test_release_check_runs_quality_build_and_launcher_validation() -> None:
    release_check = RELEASE_CHECK.read_text(encoding="utf-8")

    assert "uv run --locked ruff format --check" in release_check
    assert "uv run --locked ruff check" in release_check
    assert "uv run --locked pytest" in release_check
    assert "uv run --locked pyright" in release_check
    assert "uv build --sdist --wheel" in release_check
    assert "cmd /c Start.bat --diagnostics" in release_check
