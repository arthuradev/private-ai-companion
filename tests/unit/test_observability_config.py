from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.config import (
    ObservabilityConfigError,
    load_observability_config,
)


def test_load_observability_config_reads_default_file() -> None:
    config = load_observability_config()

    assert config.enabled is True
    assert config.structured_logging_enabled is True
    assert config.event_replay_enabled is True
    assert config.metrics_enabled is True
    assert config.health_checks_enabled is True


def test_load_observability_config_reads_custom_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "observability.toml"
    config_path.write_text(
        """
[observability]
enabled = true
structured_logging_enabled = false
max_log_records = 10
event_replay_enabled = true
max_replay_events = 12
metrics_enabled = true
health_checks_enabled = false
""".strip(),
        encoding="utf-8",
    )

    config = load_observability_config(config_path)

    assert config.structured_logging_enabled is False
    assert config.max_log_records == 10
    assert config.max_replay_events == 12
    assert config.health_checks_enabled is False


def test_load_observability_config_rejects_invalid_retention(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "observability.toml"
    config_path.write_text(
        """
[observability]
enabled = true
structured_logging_enabled = true
max_log_records = 0
event_replay_enabled = true
max_replay_events = 12
metrics_enabled = true
health_checks_enabled = true
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ObservabilityConfigError):
        load_observability_config(config_path)
