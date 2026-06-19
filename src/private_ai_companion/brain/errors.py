from __future__ import annotations


class BrainError(Exception):
    """Base class for brain module errors."""


class LLMProviderError(BrainError):
    """Raised by LLM providers when generation fails."""


class LLMRoutingError(BrainError):
    """Raised when the LLM router cannot produce a response."""
