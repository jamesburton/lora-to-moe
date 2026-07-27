"""Command-line validation for portable expert and graph manifests."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .contracts import ExpertManifest, GraphManifest, ValidationError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lora-moe")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate an expert manifest")
    validate.add_argument("path", type=Path)
    graph = commands.add_parser("validate-graph", help="validate an expert graph")
    graph.add_argument("path", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        manifest = (
            ExpertManifest.load(args.path)
            if args.command == "validate"
            else GraphManifest.load(args.path)
        )
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        print(f"invalid: {error}")
        return 1
    print(json.dumps({"status": "valid", "manifest": asdict(manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
