from __future__ import annotations

import time
from typing import Any

# Robust dynamic imports to support PySide6 or PyQt6
try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets


class ClockWidget(QtWidgets.QLabel):
    """Dynamic clock widget updating every second based on configuration formatting."""

    def __init__(self, config: dict[str, Any], parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("ClockWidget")
        self.config = config

        clock_config = config.get("shell", {}).get("clock", {})
        # Map simple QTime-like formats if they are configured, but use strftime formatting by default
        self.format_str = clock_config.get("format", "%a %b %d, %I:%M %p")

        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Set up clock timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self) -> None:
        # Format the current time using python strftime formatting
        fmt = self.format_str
        # Basic helper translation if users input QTime style formats:
        # e.g., yyyy -> %Y, MM -> %m, dd -> %d, hh -> %I, mm -> %M, ss -> %S, AP -> %p
        fmt = (
            fmt.replace("yyyy", "%Y")
            .replace("yy", "%y")
            .replace("MMM", "%b")
            .replace("MM", "%m")
            .replace("ddd", "%a")
            .replace("dd", "%d")
            .replace("hh", "%I")
            .replace("mm", "%M")
            .replace("ss", "%S")
            .replace("AP", "%p")
            .replace("ap", "%p")
        )

        try:
            current_time = time.strftime(fmt)
            if current_time == fmt and "%" not in fmt:
                raise ValueError("Invalid or literal format string")
            self.setText(current_time)
        except Exception:
            self.setText(time.strftime("%a %b %d, %I:%M %p"))
