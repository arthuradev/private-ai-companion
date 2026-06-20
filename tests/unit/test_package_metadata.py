from __future__ import annotations

import tomllib
from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__


def test_package_metadata_is_generic() -> None:
    assert PROJECT_NAME == "private-ai-companion"
    assert __version__ == "0.3.0rc1"


def test_pyproject_metadata_matches_package_metadata() -> None:
    pyproject = tomllib.loads(
        (Path(__file__).parents[2] / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert pyproject["project"]["name"] == PROJECT_NAME
    assert pyproject["project"]["version"] == __version__
    assert (
        pyproject["project"]["scripts"][PROJECT_NAME]
        == "private_ai_companion.__main__:main"
    )
