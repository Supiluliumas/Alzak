from __future__ import annotations

import sys
from pathlib import Path


def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parents[2]


def assets_root() -> Path:
    return resource_root() / "assets"


def levels_root() -> Path:
    return resource_root() / "levels"
