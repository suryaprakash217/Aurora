from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Module(Protocol):
    """Minimal interface for shell modules."""

    name: str

    def initialize(self, context: dict[str, Any]) -> None:
        ...

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        ...


class ModuleError(RuntimeError):
    """Raised when a module cannot complete its lifecycle step."""
