from __future__ import annotations

from typing import Any

# Dynamic imports
try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets

from aurora.services.system import get_system_usage


class StatusWidget(QtWidgets.QWidget):
    """Sleek CPU and Memory usage indicator panel widget."""

    def __init__(self, config: dict[str, Any], parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("StatusContainer")
        self.config = config

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(6, 2, 6, 2)
        self.layout.setSpacing(0)

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("StatusLabel")
        self.layout.addWidget(self.label)

        # Update loop timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)
        self.update_status()

    def update_status(self) -> None:
        usage = get_system_usage()
        cpu = usage.get("cpu", 0.0)
        mem = usage.get("memory", 0.0)
        self.label.setText(f"CPU: {cpu:.1f}% | MEM: {mem:.1f}%")
