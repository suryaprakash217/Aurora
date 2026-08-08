from __future__ import annotations

from typing import Optional

from aurora.compositor.backend import CompositorBackend
from aurora.compositor.models import WorkspaceModel, WindowModel


class CompositorManager:
    def __init__(self, backend: CompositorBackend) -> None:
        self.backend = backend
        self.active_workspace: Optional[int] = None

    def open_window(self, window: WindowModel) -> None:
        self.backend.open_window(window)

    def close_window(self, window_id: str) -> None:
        self.backend.close_window(window_id)

    def move_window(self, window_id: str, x: int, y: int) -> None:
        self.backend.move_window(window_id, x, y)

    def resize_window(self, window_id: str, width: int, height: int) -> None:
        self.backend.resize_window(window_id, width, height)

    def focus_window(self, window_id: str) -> None:
        self.backend.focus_window(window_id)

    def change_workspace(self, workspace_id: int) -> None:
        self.active_workspace = workspace_id
        self.backend.change_workspace(workspace_id)

    def list_windows(self) -> list[WindowModel]:
        return self.backend.list_windows()

    def list_workspaces(self) -> list[WorkspaceModel]:
        return self.backend.list_workspaces()
