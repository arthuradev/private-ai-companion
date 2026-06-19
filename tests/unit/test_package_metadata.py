from __future__ import annotations

from private_ai_companion import PROJECT_NAME, __version__


def test_package_metadata_is_generic() -> None:
    assert PROJECT_NAME == "private-ai-companion"
    assert __version__ == "0.0.0"
