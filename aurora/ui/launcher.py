from __future__ import annotations

from typing import Any

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:  # pragma: no cover
    from PyQt6 import QtCore, QtGui, QtWidgets


class LauncherButton(QtWidgets.QPushButton):
    """Placeholder launcher button for the Aurora shell panel."""

    def __init__(self, config: dict[str, Any], parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__("Aurora Launcher", parent)
        self.setObjectName("LauncherButton")
        self.config = config
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.clicked.connect(self.on_click)

    def on_click(self) -> None:
        print("Aurora launcher placeholder clicked.")
