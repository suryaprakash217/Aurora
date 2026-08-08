from __future__ import annotations

from typing import Any


class Renderer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def render_frame(self) -> None:
        raise NotImplementedError("Renderer is not implemented yet")
