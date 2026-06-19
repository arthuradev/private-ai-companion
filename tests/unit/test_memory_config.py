from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import MemoryConfigError, load_memory_config


def test_load_memory_config_reads_default_file() -> None:
    config = load_memory_config()

    assert config.database_path == Path("data/memory.sqlite3")
    assert config.auto_approve_low_sensitivity is False
    assert config.retention_days == 365
    assert config.policy.reject_sensitive_by_default is True
    assert config.policy.minimum_confidence == 0.40


def test_load_memory_config_reads_custom_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "memory.toml"
    config_path.write_text(
        """
[memory]
database_path = "tmp/memory.sqlite3"
auto_approve_low_sensitivity = true
retention_days = 30

[memory.policy]
reject_sensitive_by_default = true
minimum_confidence = 0.75
""".strip(),
        encoding="utf-8",
    )

    config = load_memory_config(config_path)

    assert config.database_path == Path("tmp/memory.sqlite3")
    assert config.auto_approve_low_sensitivity is True
    assert config.retention_days == 30
    assert config.policy.minimum_confidence == 0.75


def test_load_memory_config_rejects_invalid_confidence(tmp_path: Path) -> None:
    config_path = tmp_path / "memory.toml"
    config_path.write_text(
        """
[memory]
database_path = "tmp/memory.sqlite3"
auto_approve_low_sensitivity = false
retention_days = 30

[memory.policy]
reject_sensitive_by_default = true
minimum_confidence = 1.25
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(MemoryConfigError):
        load_memory_config(config_path)
