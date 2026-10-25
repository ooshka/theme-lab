from __future__ import annotations

import argparse
import json
from pathlib import Path

from .server import serve
from .theme import load_theme


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    root = project_root()
    parser = argparse.ArgumentParser(description="Edit and export a shared color palette")
    parser.add_argument("--theme", type=Path, default=root / "themes" / "nova.json")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="start the local visual editor")
    serve_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="interface to bind (default: 0.0.0.0 for WSL-to-Windows localhost forwarding)",
    )
    serve_parser.add_argument("--port", default=8765, type=int)

    export_parser = subparsers.add_parser("export", help="write the normalized palette JSON")
    export_parser.add_argument("--output", type=Path)

    args = parser.parse_args()
    if args.command == "serve":
        serve(root, args.theme.resolve(), args.host, args.port)
        return

    output = json.dumps(load_theme(args.theme), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()

