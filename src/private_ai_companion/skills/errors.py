from __future__ import annotations


class SkillError(RuntimeError):
    """Base error for skill registry and execution failures."""


class SkillManifestError(SkillError):
    """Raised when a skill manifest is invalid."""


class SkillRegistryError(SkillError):
    """Raised when a skill cannot be registered or resolved."""
