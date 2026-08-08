from __future__ import annotations

from typing import List

from aurora.compositor.backend import CompositorBackend
from aurora.compositor.models import MonitorModel, WorkspaceModel, WindowModel


class MockCompositorBackend(CompositorBackend):
    def __init__(self) -> None:
        self._windows: dict[str, WindowModel] = {}
        self._workspaces: dict[int, WorkspaceModel] = {
            1: WorkspaceModel(id=1, name="Workspace 1", windows=[]),
            2: WorkspaceModel(id=2, name="Workspace 2", windows=[]),
            3: WorkspaceModel(id=3, name="Workspace 3", windows=[]),
        }
        self._monitors: list[MonitorModel] = [MonitorModel(id="primary", width=1920, height=1080)]
        self._active_workspace = 1

    def open_window(self, window: WindowModel) -> None:
        self._windows[window.id] = window
        self._workspaces.setdefault(window.workspace, WorkspaceModel(id=window.workspace, name=f"Workspace {window.workspace}", windows=[])).windows.append(window)

    def close_window(self, window_id: str) -> None:
        window = self._windows.pop(window_id, None)
        if not window:
            return
        workspace = self._workspaces.get(window.workspace)
        if workspace:
            workspace.windows = [w for w in workspace.windows if w.id != window_id]

    def move_window(self, window_id: str, x: int, y: int) -> None:
        window = self._windows.get(window_id)
        if window:
            window.x = x
            window.y = y

    def resize_window(self, window_id: str, width: int, height: int) -> None:
        window = self._windows.get(window_id)
        if window:
            window.width = width
            window.height = height

    def focus_window(self, window_id: str) -> None:
        for window in self._windows.values():
            window.focused = window.id == window_id

    def change_workspace(self, workspace_id: int) -> None:
        self._active_workspace = workspace_id

    def list_windows(self) -> List[WindowModel]:
        return list(self._windows.values())

    def list_workspaces(self) -> List[WorkspaceModel]:
        return list(self._workspaces.values())

    def list_monitors(self) -> List[MonitorModel]:
        return self._monitors
