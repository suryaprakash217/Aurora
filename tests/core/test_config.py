from __future__ import annotations

import json
from pathlib import Path

import pytest

from aurora.config import ConfigError, load_config, load_default_config


def test_load_default_config_contains_shell_defaults():
    config = load_default_config()

    assert isinstance(config, dict)
    assert config["shell"]["name"] == "Aurora"
    assert config["shell"]["theme"] == "aurora-dark"
    assert config["shell"]["launcher"]["visible"] is True


def test_load_config_merges_with_default(tmp_path: Path):
    override = {
        "shell": {
            "theme": "aurora-light",
            "clock": {"format": "%H:%M"},
        }
    }
    path = tmp_path / "custom.json"
    path.write_text(json.dumps(override), encoding="utf-8")

    config = load_config(str(path))

    assert config["shell"]["theme"] == "aurora-light"
    assert config["shell"]["clock"]["format"] == "%H:%M"
    assert config["shell"]["name"] == "Aurora"


def test_load_config_missing_file_raises():
    with pytest.raises(ConfigError):
        load_config("nonexistent-config.json")
