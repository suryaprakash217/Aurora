from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class InputState:
    keyboard_layout: str
    pointer_x: int
    pointer_y: int
    buttons_pressed: list[str]


class InputManager:
    def __init__(self) -> None:
        self.state = InputState(keyboard_layout="us", pointer_x=0, pointer_y=0, buttons_pressed=[])

    def move_pointer(self, x: int, y: int) -> None:
        self.state.pointer_x = x
        self.state.pointer_y = y

    def press_button(self, button: str) -> None:
        if button not in self.state.buttons_pressed:
            self.state.buttons_pressed.append(button)

    def release_button(self, button: str) -> None:
        self.state.buttons_pressed = [b for b in self.state.buttons_pressed if b != button]
