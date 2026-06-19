from __future__ import annotations

from pathlib import Path

import pytest

from private_ai_companion.brain import LLMProviderKind
from private_ai_companion.config import ProvidersConfigError, load_providers_config


def test_load_providers_config_reads_default_file() -> None:
    config = load_providers_config()

    assert config.llm.default_provider == "fake-local"
    assert config.llm.enabled_providers[0].kind is LLMProviderKind.FAKE
    assert all(provider.provider_id for provider in config.llm.providers)


def test_load_providers_config_rejects_missing_default_provider(tmp_path: Path) -> None:
    config_path = tmp_path / "providers.toml"
    config_path.write_text(
        """
[llm]
default_provider = "missing"
fallback_order = []

[[llm.providers]]
id = "fake-local"
kind = "fake"
model = "fake-local-v0"
enabled = true
requires_api_key = false
api_key_env = ""
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ProvidersConfigError):
        load_providers_config(config_path)


def test_load_providers_config_keeps_api_key_names_without_secret_values() -> None:
    config = load_providers_config()
    cloud_providers = [
        provider
        for provider in config.llm.providers
        if provider.kind is LLMProviderKind.CLOUD
    ]

    assert cloud_providers
    assert all(provider.requires_api_key for provider in cloud_providers)
    assert all(provider.api_key_env for provider in cloud_providers)
