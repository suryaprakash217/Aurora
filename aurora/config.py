from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


class ConfigError(RuntimeError):
    """Raised when the requested configuration cannot be loaded."""


def _merge_dicts(default: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(default)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(default.get(key), dict):
            merged[key] = _merge_dicts(default[key], value)
        else:
            merged[key] = value
    return merged


@lru_cache(maxsize=8)
def _load_config_from_disk(config_path: str) -> dict[str, Any]:
    with Path(config_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load a JSON configuration file from disk or fall back to defaults."""
    default_path = Path(__file__).resolve().parent.parent / "config" / "defaults.json"
    default_config = _load_config_from_disk(str(default_path.resolve()))
    if config_path:
        config_file = Path(config_path)
        if not config_file.exists():
            raise ConfigError(f"Configuration file not found: {config_file}")
        custom_config = _load_config_from_disk(str(config_file.resolve()))
        return _merge_dicts(default_config, custom_config)

    return default_config


def load_default_config() -> dict[str, Any]:
    """Load the built-in default configuration shipped with the project."""
    return _load_config_from_disk(
        str((Path(__file__).resolve().parent.parent / "config" / "defaults.json").resolve())
    )
