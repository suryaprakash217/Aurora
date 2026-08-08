from __future__ import annotations

from aurora.input.manager import InputManager


def test_input_manager_moves_pointer_and_buttons():
    manager = InputManager()
    manager.move_pointer(100, 200)
    assert manager.state.pointer_x == 100
    assert manager.state.pointer_y == 200

    manager.press_button("left")
    assert "left" in manager.state.buttons_pressed

    manager.release_button("left")
    assert manager.state.buttons_pressed == []
