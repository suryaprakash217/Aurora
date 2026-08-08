from __future__ import annotations

from typing import Any

from aurora.modules.base import Module


class AuroraEngine:
    """Coordinate shell modules through a simple, testable lifecycle."""

    __slots__ = ("config", "modules", "_initialized")

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.modules: list[Module] = []
        self._initialized = False

    def register_module(self, module: Module) -> None:
        self.modules.append(module)
        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return

        for module in self.modules:
            module.initialize(self.config)

        self._initialized = True

    def run(self) -> list[dict[str, Any]]:
        self.initialize()
        return [module.run(self.config) for module in self.modules]
