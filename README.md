# Aurora

Aurora is a modular desktop shell environment and window manager foundation for Linux. It is designed to scale from a highly modular desktop shell on Hyprland to an original Wayland compositor/window manager.

All Aurora implementation is designed from the ground up using standard Wayland, Linux, and Qt APIs, prioritizing clean decoupling of visual and logical layers.

## Repository Structure

- `aurora/` — Python package housing core systems and graphical interfaces:
  - `core/` — Lifecycle transitions, event loop integrations, and service registration.
  - `compositor/` — High-level interfaces for window, workspace, monitor, keyboard, and pointer. Includes `MockCompositorBackend` for local development.
  - `wayland/` — Protocols and Wayland event listener loops.
  - `ipc/` — Inter-process message protocols and dispatcher.
  - `input/` — Keyboard layout and cursor state managers.
  - `rendering/` — Rendering interface.
  - `ui/` — PySide6/PyQt6 graphical panels, launcher overlay, and indicators.
- `config/` — Shell layout, clock formats, and theme configuration defaults.
- `tests/` — Segmented test suites (core logic vs. graphical Qt components).
- `docs/` — Concise architecture blueprints and guides.

---

## Quick Start

1. **Review the architecture** in [docs/architecture.md](docs/architecture.md).
2. **Install system-level dependencies** (Arch Linux example):
   ```bash
   sudo pacman -S python-gobject gtk3 gtk-layer-shell
   ```
3. **Set up the virtual environment** ensuring it has access to system site-packages:
   ```bash
   python -m venv --system-site-packages .venv
   source .venv/bin/activate
   pip install -e .
   ```
4. **Launch the shell panel CLI** (without GUI):
   ```bash
   aurora-shell --cli
   ```
5. **Launch the graphical panel** (GUI):
   ```bash
   aurora-shell --gui
   ```
6. **Run the test suite**:
   **Core (Non-GUI) Tests**:
   ```bash
   .venv/bin/python -m pytest tests/core aurora/core/tests aurora/compositor/tests aurora/input/tests
   ```
   **GUI (Qt) Tests** (requires `pytest-qt` package and active display):
   ```bash
   .venv/bin/python -m pytest tests/gui
   ```

---

## Graphical Shell Features

Aurora includes a minimal, hardware-accelerated top panel styled with glassmorphism aesthetics.
* **Launcher Button**: A styled interactive placeholder which opens/closes the menu overlay.
* **Workspace Indicator**: Automatically parses active and configured workspaces.
* **System Status Area**: Displays CPU & Memory usage updated periodically.
* **Date & Clock**: Local time display refreshed every second.

---

## Documentation

- [docs/architecture.md](docs/architecture.md) — detailed system layout and subsystem details.
- [docs/developer-guide.md](docs/developer-guide.md) — instructions for setting up testing and adding code.
- [docs/user-guide.md](docs/user-guide.md) — overview of desktop commands and configuration keys.
- [docs/configuration-guide.md](docs/configuration-guide.md) — configuration conventions and JSON schema structures.

## License

Aurora is released under the MIT License.
