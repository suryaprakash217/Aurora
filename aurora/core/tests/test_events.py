from __future__ import annotations

from aurora.core.events import Event, EventBus


def test_event_bus_publish_subscribe():
    bus = EventBus()
    result: list[str] = []

    def listener(event: Event) -> None:
        result.append(event.name)

    bus.subscribe("test", listener)
    bus.publish(Event(name="test", payload={}))

    assert result == ["test"]
