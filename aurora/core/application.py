from __future__ import annotations

from typing import Any

from aurora.core.events import Event, EventBus
from aurora.core.lifecycle import LifecycleState


class AuroraApplication:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.state = LifecycleState.CREATED
        self.events = EventBus()
        self.services: dict[str, object] = {}

    def initialize(self) -> None:
        self.state = LifecycleState.INITIALIZING
        self.events.publish(Event(name="application.initializing", payload={}))
        self.state = LifecycleState.RUNNING
        self.events.publish(Event(name="application.running", payload={}))

    def stop(self) -> None:
        self.state = LifecycleState.STOPPING
        self.events.publish(Event(name="application.stopping", payload={}))
        self.state = LifecycleState.STOPPED
        self.events.publish(Event(name="application.stopped", payload={}))

    def register_service(self, name: str, service: object) -> None:
        self.services[name] = service

    def get_service(self, name: str) -> object | None:
        return self.services.get(name)
