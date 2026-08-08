from __future__ import annotations

import json
import pytest

from aurora.main import main


def test_main_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "show this help message and exit" in captured.out


def test_main_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    # In some python/argparse versions, version output goes to stderr, in others to stdout
    output = captured.out + captured.err
    assert "aurora-shell 0.1.0" in output


def test_main_success(capsys, tmp_path):
    config_file = tmp_path / "custom_config.json"
    config_data = {
        "shell": {
            "name": "Custom Aurora",
            "version": "1.0.0"
        }
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f)

    # Use --cli option to prevent starting the blocking GUI event loop during tests
    exit_code = main(["--config", str(config_file), "--cli"])
    assert exit_code == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert len(payload) == 1
    assert payload[0]["module"] == "status"
    assert payload[0]["status"] == "ready"


def test_main_missing_config(capsys):
    exit_code = main(["--config", "non_existent_file.json"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error loading configuration" in captured.err


def test_main_gui(capsys):
    from unittest.mock import patch
    with patch("aurora.ui.run_aurora_gui") as mock_run:
        mock_run.return_value = 0
        exit_code = main([])
        assert exit_code == 0
        mock_run.assert_called_once()


def test_main_cli(capsys):
    exit_code = main(["--cli"])
    assert exit_code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert len(payload) == 1
    assert payload[0]["module"] == "status"
