from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from aurora import AuroraEngine, load_config
from aurora.modules.status import StatusModule


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch the Aurora shell core")
    parser.add_argument("--config", type=str, default=None, help="Path to a JSON config file")
    parser.add_argument("--version", action="version", version="aurora-shell 0.1.0")

    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        return 1

    engine = AuroraEngine(config)
    engine.register_module(StatusModule())
    payload = engine.run()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
