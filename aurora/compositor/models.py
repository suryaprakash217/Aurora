from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class WindowState(str, Enum):
    MINIMIZED = "MINIMIZED"
    MAXIMIZED = "MAXIMIZED"
    RESTORED = "RESTORED"


@dataclass
class WindowModel:
    id: str
    title: str
    workspace: int
    x: int
    y: int
    width: int
    height: int
    focused: bool = False
    state: WindowState = WindowState.RESTORED


@dataclass
class WorkspaceModel:
    id: int
    name: str
    windows: list[WindowModel]


@dataclass
class MonitorModel:
    id: str
    width: int
    height: int
    scale: float = 1.0


@dataclass
class KeyboardModel:
    layout: str
    repeat_rate: float
    repeat_delay: float


@dataclass
class PointerModel:
    x: int
    y: int
    button_pressed: bool
    modifiers: list[str] = None
