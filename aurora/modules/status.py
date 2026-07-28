from __future__ import annotations

from typing import Any


class StatusModule:
    """A simple module that reports the shell status payload."""

    name = "status"

    def initialize(self, context: dict[str, Any]) -> None:
        self.context = context

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "module": self.name,
            "status": "ready",
            "timestamp": context.get("timestamp", "unknown"),
        }
