from __future__ import annotations


class AvatarError(Exception):
    """Base class for avatar module errors."""


class AvatarProviderError(AvatarError):
    """Raised when an avatar provider cannot apply a visual state."""
