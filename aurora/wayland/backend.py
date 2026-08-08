from __future__ import annotations

from typing import Any


class WaylandBackend:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def start(self) -> None:
        raise NotImplementedError("Wayland backend is not implemented yet")

    def stop(self) -> None:
        raise NotImplementedError("Wayland backend is not implemented yet")
