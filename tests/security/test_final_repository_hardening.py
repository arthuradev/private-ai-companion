from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]


def tracked_files() -> tuple[str, ...]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return tuple(line.strip().replace("\\", "/") for line in result.stdout.splitlines())


def test_prompt_codex_artifact_is_not_tracked() -> None:
    assert "PROMPT-CODEX.md" not in tracked_files()


def test_no_private_runtime_or_build_artifacts_are_tracked() -> None:
    forbidden_prefixes = (
        "data/",
        "logs/",
        "dist/",
        "build/",
        ".venv/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".pyright/",
    )
    violations = [
        path for path in tracked_files() if path.startswith(forbidden_prefixes)
    ]

    assert violations == []


def test_no_secret_file_patterns_are_tracked() -> None:
    allowed = {".env.example"}
    forbidden_suffixes = (".pem", ".key", ".p12", ".pfx", ".sqlite", ".sqlite3", ".db")
    violations = [
        path
        for path in tracked_files()
        if path not in allowed
        and (Path(path).name == ".env" or path.endswith(forbidden_suffixes))
    ]

    assert violations == []


def test_pyproject_has_no_streaming_platform_dependencies() -> None:
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    forbidden_fragments = ("twitch", "youtube", "obs", "streamlink")

    for fragment in forbidden_fragments:
        assert fragment not in pyproject


def test_start_bat_does_not_log_raw_arguments_or_secret_env_names() -> None:
    launcher = (REPO_ROOT / "Start.bat").read_text(encoding="utf-8")
    forbidden_fragments = (
        "call :log %*",
        "echo %*",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "OPENROUTER_API_KEY",
        "PRIVATE_AI_COMPANION_VTS_TOKEN",
    )

    for fragment in forbidden_fragments:
        assert fragment not in launcher
