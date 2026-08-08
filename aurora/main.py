from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from aurora import AuroraEngine, AuroraApplication, load_config
from aurora.compositor import CompositorManager, MockCompositorBackend
from aurora.ipc import IPCServer
from aurora.input import InputManager
from aurora.modules.status import StatusModule


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch the Aurora shell core")
    parser.add_argument("--config", type=str, default=None, help="Path to a JSON config file")
    parser.add_argument("--version", action="version", version="aurora-shell 0.1.0")
    parser.add_argument("--gui", action="store_true", help="Launch the Aurora graphical shell panel")
    parser.add_argument("--cli", action="store_true", help="Run Aurora in command-line mode")

    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        return 1

    if args.cli:
        engine = AuroraEngine(config)
        engine.register_module(StatusModule())
        payload = engine.run()
        print(json.dumps(payload, indent=2))
        return 0

    if args.gui or not args.cli:
        app = AuroraApplication(config)
        app.register_service("compositor", CompositorManager(MockCompositorBackend()))
        app.register_service("input", InputManager())
        app.register_service("ipc", IPCServer())
        app.initialize()

        try:
            from aurora.ui import run_aurora_gui

            exit_code = run_aurora_gui(config)
        except Exception as e:
            print(f"Error launching GUI shell: {e}", file=sys.stderr)
            exit_code = 1

        app.stop()
        return exit_code

    return 0


if __name__ == "__main__":
    sys.exit(main())
