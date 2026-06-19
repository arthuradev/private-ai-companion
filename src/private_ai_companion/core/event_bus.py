from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from inspect import isawaitable

from private_ai_companion.core.errors import EventHandlerError
from private_ai_companion.core.events import BaseEvent

EventHandler = Callable[[BaseEvent], Awaitable[None] | None]


@dataclass(frozen=True, slots=True)
class Subscription:
    event_type: type[BaseEvent]
    handler: EventHandler


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type[BaseEvent], list[EventHandler]] = {}

    def subscribe(
        self,
        event_type: type[BaseEvent],
        handler: EventHandler,
    ) -> Subscription:
        self._handlers.setdefault(event_type, []).append(handler)
        return Subscription(event_type=event_type, handler=handler)

    def unsubscribe(self, subscription: Subscription) -> None:
        handlers = self._handlers.get(subscription.event_type)
        if handlers is None:
            return

        self._handlers[subscription.event_type] = [
            handler for handler in handlers if handler is not subscription.handler
        ]
        if not self._handlers[subscription.event_type]:
            del self._handlers[subscription.event_type]

    async def publish(self, event: BaseEvent) -> None:
        for handler in self._matching_handlers(event):
            try:
                result = handler(event)
                if isawaitable(result):
                    await result
            except Exception as error:
                raise EventHandlerError(
                    event_name=event.name,
                    handler_name=self._handler_name(handler),
                ) from error

    def _matching_handlers(self, event: BaseEvent) -> list[EventHandler]:
        handlers: list[EventHandler] = []
        for event_type, registered_handlers in self._handlers.items():
            if isinstance(event, event_type):
                handlers.extend(registered_handlers)
        return handlers

    @staticmethod
    def _handler_name(handler: EventHandler) -> str:
        return getattr(handler, "__qualname__", repr(handler))
