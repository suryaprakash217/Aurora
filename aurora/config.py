from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


class ConfigError(RuntimeError):
    """Raised when the requested configuration cannot be loaded."""


@lru_cache(maxsize=8)
def _load_config_from_disk(config_path: str) -> dict[str, Any]:
    with Path(config_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load a JSON configuration file from disk or fall back to defaults."""
    default_path = Path(__file__).resolve().parent.parent / "config" / "defaults.json"
    config_file = Path(config_path) if config_path else default_path

    if not config_file.exists():
        raise ConfigError(f"Configuration file not found: {config_file}")

    return _load_config_from_disk(str(config_file.resolve()))


def load_default_config() -> dict[str, Any]:
    """Load the built-in default configuration shipped with the project."""
    return load_config(None)
