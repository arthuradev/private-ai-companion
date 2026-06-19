from __future__ import annotations


class CoreError(Exception):
    """Base class for core runtime errors."""


class EventBusError(CoreError):
    """Base class for event bus errors."""


class EventHandlerError(EventBusError):
    def __init__(self, event_name: str, handler_name: str) -> None:
        self.event_name = event_name
        self.handler_name = handler_name
        super().__init__(f"handler {handler_name!r} failed for event {event_name!r}")


class LifecycleError(CoreError):
    """Raised when runtime lifecycle transitions are invalid."""
