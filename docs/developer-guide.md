# Developer Guide

Welcome to the Aurora developer guide. This guide explains repository workflows, contribution standards, and testing procedures.

---

## 1. Development Principles

1. **Strict Decoupling**: Do not import `aurora/ui` inside core logical subsystems (`core`, `compositor`, `ipc`, etc.).
2. **Type Hints**: All new functions, class properties, and parameters should be annotated with Python type hints.
3. **No Placeholders**: When adding new features, include functioning fallback paths or mock implementations.
4. **Cascade Configuration**: Drive behaviors using config values instead of hardcoding parameters.

---

## 2. Directory Layout

- [aurora/core/](file:///home/surya/Projects/Aurora/Aurora/aurora/core/) — Shell event loop and state machine
- [aurora/compositor/](file:///home/surya/Projects/Aurora/Aurora/aurora/compositor/) — Compositor backend interfaces and models
- [aurora/ui/](file:///home/surya/Projects/Aurora/Aurora/aurora/ui/) — PySide6/PyQt6 graphical shell
- [tests/core/](file:///home/surya/Projects/Aurora/Aurora/tests/core/) — Pure Python core logic tests
- [tests/gui/](file:///home/surya/Projects/Aurora/Aurora/tests/gui/) — Qt-based GUI tests (requiring active display/pytest-qt)

---

## 3. Running Tests

Due to the headless environments in CI or server setups, the test suite is partitioned.

### 3.1 Core (Non-GUI) Tests
To run core logic and engine tests, use:
```bash
.venv/bin/python -m pytest tests/core aurora/core/tests aurora/compositor/tests aurora/input/tests
```
These tests have no dependency on active X11/Wayland displays and do not require `pytest-qt`. They will execute quickly and reliably.

### 3.2 GUI (Qt) Tests
To run the user interface tests (which verify the clock format, status panel widgets, and launcher overlays), you must have `pytest-qt` installed in your virtual environment and a valid display server connection (or offscreen rendering plugins configuration).

To run them:
```bash
# Ensure pytest-qt is installed
.venv/bin/pip install pytest-qt

# Run GUI tests
.venv/bin/python -m pytest tests/gui
```

### 3.3 Adding Tests
- Core logical components must have accompanying tests in their respective folders or inside `tests/core/`.
- Graphical widgets should verify rendering outputs in `tests/gui/` using the `qtbot` helper.
