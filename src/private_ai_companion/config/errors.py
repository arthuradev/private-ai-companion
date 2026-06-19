from __future__ import annotations


class ConfigError(Exception):
    """Base class for configuration errors."""


class PersonaConfigError(ConfigError):
    """Raised when persona configuration is invalid."""
