from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class Event:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[str, list[EventListener]] = {}

    def subscribe(self, event_name: str, listener: EventListener) -> None:
        self._listeners.setdefault(event_name, []).append(listener)

    def publish(self, event: Event) -> None:
        for listener in list(self._listeners.get(event.name, [])):
            listener(event)


EventListener = Callable[[Event], None]
