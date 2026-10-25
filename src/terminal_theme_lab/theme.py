from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

COLOR_KEYS = (
    "background",
    "foreground",
    "cursorColor",
    "selectionBackground",
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "purple",
    "cyan",
    "white",
    "brightBlack",
    "brightRed",
    "brightGreen",
    "brightYellow",
    "brightBlue",
    "brightPurple",
    "brightCyan",
    "brightWhite",
)

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


def validate_theme(theme: Any) -> dict[str, str]:
    if not isinstance(theme, dict):
        raise ValueError("theme must be a JSON object")

    name = theme.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")

    missing = [key for key in COLOR_KEYS if key not in theme]
    if missing:
        raise ValueError(f"missing colors: {', '.join(missing)}")

    invalid = [key for key in COLOR_KEYS if not isinstance(theme[key], str) or not HEX_COLOR.fullmatch(theme[key])]
    if invalid:
        raise ValueError(f"invalid #RRGGBB colors: {', '.join(invalid)}")

    return {"name": name.strip(), **{key: theme[key].upper() for key in COLOR_KEYS}}


def load_theme(path: Path) -> dict[str, str]:
    with path.open(encoding="utf-8") as handle:
        return validate_theme(json.load(handle))


def save_theme(path: Path, theme: Any) -> dict[str, str]:
    validated = validate_theme(theme)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(validated, handle, indent=2)
        handle.write("\n")
    return validated

