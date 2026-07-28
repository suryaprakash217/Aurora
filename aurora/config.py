from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigError(RuntimeError):
    """Raised when the requested configuration cannot be loaded."""


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load a JSON configuration file from disk or fall back to defaults."""
    default_path = Path(__file__).resolve().parent.parent / "config" / "defaults.json"
    config_file = Path(config_path) if config_path else default_path

    if not config_file.exists():
        raise ConfigError(f"Configuration file not found: {config_file}")

    with config_file.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_default_config() -> dict[str, Any]:
    """Load the built-in default configuration shipped with the project."""
    return load_config(None)
