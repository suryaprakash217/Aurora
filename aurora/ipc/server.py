from __future__ import annotations

from typing import Any, Callable

from aurora.ipc.protocol import IPCMessage


class IPCServer:
    def __init__(self) -> None:
        self._handlers: dict[str, list[IPCHandler]] = {}

    def register_handler(self, message_type: str, handler: IPCHandler) -> None:
        self._handlers.setdefault(message_type, []).append(handler)

    def send(self, message: IPCMessage) -> None:
        for handler in self._handlers.get(message.type, []):
            handler(message)


IPCHandler = Callable[[IPCMessage], None]
