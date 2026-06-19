from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from private_ai_companion.brain import LLMProviderKind
from private_ai_companion.config.errors import ConfigError

DEFAULT_PROVIDERS_CONFIG_PATH = Path("configs/providers.default.toml")


class ProvidersConfigError(ConfigError):
    """Raised when providers configuration is invalid."""


@dataclass(frozen=True, slots=True)
class LLMProviderConfig:
    provider_id: str
    kind: LLMProviderKind
    model: str
    enabled: bool
    requires_api_key: bool
    api_key_env: str | None = None


@dataclass(frozen=True, slots=True)
class LLMRouterConfig:
    default_provider: str
    fallback_order: tuple[str, ...]
    providers: tuple[LLMProviderConfig, ...]

    @property
    def enabled_providers(self) -> tuple[LLMProviderConfig, ...]:
        return tuple(provider for provider in self.providers if provider.enabled)


@dataclass(frozen=True, slots=True)
class ProvidersConfig:
    llm: LLMRouterConfig


def load_providers_config(path: Path | None = None) -> ProvidersConfig:
    config_path = path or DEFAULT_PROVIDERS_CONFIG_PATH
    if not config_path.exists():
        return default_providers_config()

    with config_path.open("rb") as file:
        raw = cast(Mapping[str, object], tomllib.load(file))

    llm_raw = _required_mapping(raw, "llm")
    providers_raw = _required_list(llm_raw, "providers")
    providers = tuple(_parse_llm_provider(item) for item in providers_raw)
    config = ProvidersConfig(
        llm=LLMRouterConfig(
            default_provider=_required_text(llm_raw, "default_provider"),
            fallback_order=_required_text_tuple(llm_raw, "fallback_order"),
            providers=providers,
        )
    )
    _validate_llm_config(config.llm)
    return config


def default_providers_config() -> ProvidersConfig:
    return ProvidersConfig(
        llm=LLMRouterConfig(
            default_provider="fake-local",
            fallback_order=("fake-local",),
            providers=(
                LLMProviderConfig(
                    provider_id="fake-local",
                    kind=LLMProviderKind.FAKE,
                    model="fake-local-v0",
                    enabled=True,
                    requires_api_key=False,
                ),
            ),
        )
    )


def _parse_llm_provider(raw: object) -> LLMProviderConfig:
    if not isinstance(raw, Mapping):
        raise ProvidersConfigError("LLM provider entries must be tables")
    provider_raw = cast(Mapping[str, object], raw)
    return LLMProviderConfig(
        provider_id=_required_text(provider_raw, "id"),
        kind=_provider_kind(_required_text(provider_raw, "kind")),
        model=_required_text(provider_raw, "model"),
        enabled=_required_bool(provider_raw, "enabled"),
        requires_api_key=_required_bool(provider_raw, "requires_api_key"),
        api_key_env=_optional_text(provider_raw, "api_key_env"),
    )


def _validate_llm_config(config: LLMRouterConfig) -> None:
    provider_ids = {provider.provider_id for provider in config.providers}
    if config.default_provider not in provider_ids:
        raise ProvidersConfigError("default LLM provider must exist in providers list")
    missing_fallbacks = [
        provider_id
        for provider_id in config.fallback_order
        if provider_id not in provider_ids
    ]
    if missing_fallbacks:
        raise ProvidersConfigError(
            "LLM fallback providers must exist in providers list"
        )


def _required_mapping(
    mapping: Mapping[str, object],
    key: str,
) -> Mapping[str, object]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise ProvidersConfigError(f"providers config section {key!r} must be a table")
    return cast(Mapping[str, object], value)


def _required_list(mapping: Mapping[str, object], key: str) -> list[object]:
    value = mapping.get(key)
    if not isinstance(value, list):
        raise ProvidersConfigError(f"providers config field {key!r} must be a list")
    return cast(list[object], value)


def _required_text(mapping: Mapping[str, object], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProvidersConfigError(f"providers config field {key!r} must be text")
    return value.strip()


def _optional_text(mapping: Mapping[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ProvidersConfigError(f"providers config field {key!r} must be text")
    stripped = value.strip()
    return stripped or None


def _required_text_tuple(mapping: Mapping[str, object], key: str) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, list):
        raise ProvidersConfigError(f"providers config field {key!r} must be a list")

    result: list[str] = []
    items = cast(list[object], value)
    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ProvidersConfigError(
                f"providers config field {key!r} must contain only text"
            )
        result.append(item.strip())
    return tuple(result)


def _required_bool(mapping: Mapping[str, object], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ProvidersConfigError(f"providers config field {key!r} must be boolean")
    return value


def _provider_kind(value: str) -> LLMProviderKind:
    try:
        return LLMProviderKind(value)
    except ValueError as error:
        raise ProvidersConfigError(f"unknown LLM provider kind {value!r}") from error
