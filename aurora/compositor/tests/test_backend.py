from __future__ import annotations

import pytest

from aurora.compositor.mock_backend import MockCompositorBackend
from aurora.compositor.models import WindowModel


def test_mock_backend_open_close_window():
    backend = MockCompositorBackend()
    window = WindowModel(id="w1", title="Test", workspace=1, x=0, y=0, width=100, height=100)

    backend.open_window(window)
    assert backend.list_windows()[0].id == "w1"

    backend.close_window("w1")
    assert backend.list_windows() == []


def test_mock_backend_move_resize_focus():
    backend = MockCompositorBackend()
    window = WindowModel(id="w1", title="Test", workspace=1, x=0, y=0, width=100, height=100)
    backend.open_window(window)

    backend.move_window("w1", 50, 60)
    backend.resize_window("w1", 320, 240)
    backend.focus_window("w1")

    w = backend.list_windows()[0]
    assert w.x == 50
    assert w.y == 60
    assert w.width == 320
    assert w.height == 240
    assert w.focused


def test_mock_backend_change_workspace():
    backend = MockCompositorBackend()
    backend.change_workspace(2)
    assert backend.list_workspaces()[1].id == 2
