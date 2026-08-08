from __future__ import annotations

from abc import ABC, abstractmethod

from aurora.compositor.models import MonitorModel, WorkspaceModel, WindowModel


class CompositorBackend(ABC):
    @abstractmethod
    def open_window(self, window: WindowModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def close_window(self, window_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def move_window(self, window_id: str, x: int, y: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def resize_window(self, window_id: str, width: int, height: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def focus_window(self, window_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def change_workspace(self, workspace_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_windows(self) -> list[WindowModel]:
        raise NotImplementedError

    @abstractmethod
    def list_workspaces(self) -> list[WorkspaceModel]:
        raise NotImplementedError

    @abstractmethod
    def list_monitors(self) -> list[MonitorModel]:
        raise NotImplementedError
