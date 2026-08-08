from __future__ import annotations

import json
import subprocess
from typing import Any

# Dynamic imports
try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtWidgets


class WorkspaceWidget(QtWidgets.QWidget):
    """Dynamic workspace indicator supporting Hyprland integration and manual switching."""

    def __init__(self, config: dict[str, Any], parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.config = config

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)

        self.buttons: dict[int, QtWidgets.QPushButton] = {}

        # Periodically poll Hyprland active workspaces
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_workspaces)
        self.timer.start(250)
        self.update_workspaces()

    def update_workspaces(self) -> None:
        try:
            res_workspaces = subprocess.run(["hyprctl", "-j", "workspaces"], capture_output=True, text=True, check=True)
            res_active = subprocess.run(["hyprctl", "-j", "activeworkspace"], capture_output=True, text=True, check=True)

            workspaces = json.loads(res_workspaces.stdout)
            active_ws = json.loads(res_active.stdout)
            active_id = active_ws.get("id", 1)

            active_ids = {w["id"] for w in workspaces}
            all_ids = sorted(list(active_ids.union({1, 2, 3, 4, 5})))
        except Exception:
            all_ids = [1, 2, 3, 4, 5]
            active_id = 1

        # Synchronize and clean up unused buttons
        for w_id in list(self.buttons.keys()):
            if w_id not in all_ids:
                btn = self.buttons.pop(w_id)
                self.layout.removeWidget(btn)
                btn.deleteLater()

        # Add or refresh indicator buttons
        for w_id in all_ids:
            if w_id not in self.buttons:
                btn = QtWidgets.QPushButton(str(w_id), self)
                # Apply base workspace button class
                btn.setProperty("class", "WorkspaceButton")
                btn.clicked.connect(lambda checked=False, idx=w_id: self.switch_workspace(idx))
                self.buttons[w_id] = btn

                pos = sorted(list(self.buttons.keys())).index(w_id)
                self.layout.insertWidget(pos, btn)
            else:
                btn = self.buttons[w_id]

            # Style active vs inactive buttons
            if w_id == active_id:
                btn.setProperty("active", True)
                btn.setProperty("class", "WorkspaceButton ActiveWorkspaceButton")
            else:
                btn.setProperty("active", False)
                btn.setProperty("class", "WorkspaceButton")

            # Force QSS style reload
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def switch_workspace(self, workspace_id: int) -> None:
        try:
            subprocess.run(["hyprctl", "dispatch", "workspace", str(workspace_id)], check=False)
        except Exception:
            pass
        self.update_workspaces()
