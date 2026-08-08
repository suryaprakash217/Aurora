from __future__ import annotations

import re

from aurora.ui.clock import ClockWidget


def test_clock_widget_formats_time_correctly(qtbot):
    config = {"shell": {"clock": {"format": "%H:%M:%S"}}}
    widget = ClockWidget(config)
    qtbot.addWidget(widget)
    widget.update_time()

    assert re.match(r"^\d{2}:\d{2}:\d{2}$", widget.text())


def test_clock_widget_falls_back_on_invalid_format(qtbot):
    config = {"shell": {"clock": {"format": "INVALID"}}}
    widget = ClockWidget(config)
    qtbot.addWidget(widget)
    widget.update_time()

    assert widget.text() != "INVALID"
