"""Aurora desktop shell core package."""

from .config import load_config, load_default_config
from .core import AuroraApplication, Event, EventBus, LifecycleState
from .engine import AuroraEngine
from .compositor import CompositorBackend, CompositorManager, MonitorModel, WorkspaceModel, WindowModel, KeyboardModel, PointerModel
from .ipc import IPCMessage, IPCServer
from .input import InputManager, InputState
from .rendering import Renderer
from .wayland import WaylandBackend

__all__ = [
    "AuroraEngine",
    "load_config",
    "load_default_config",
    "AuroraApplication",
    "Event",
    "EventBus",
    "LifecycleState",
    "CompositorBackend",
    "CompositorManager",
    "MonitorModel",
    "WorkspaceModel",
    "WindowModel",
    "KeyboardModel",
    "PointerModel",
    "IPCMessage",
    "IPCServer",
    "InputManager",
    "InputState",
    "Renderer",
    "WaylandBackend",
]
