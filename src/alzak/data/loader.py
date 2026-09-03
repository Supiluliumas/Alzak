from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from alzak import config
from alzak.data.schema import LevelDataError, REQUIRED_ROOT_FIELDS


@dataclass(frozen=True, slots=True)
class PlatformData:
    x: float
    y: float
    w: float
    h: float
    asset_id: str


@dataclass(frozen=True, slots=True)
class PitData:
    x: float
    w: float
    kill_y: float


@dataclass(frozen=True, slots=True)
class EnemyData:
    x: float
    y: float
    patrol_min_x: float
    patrol_max_x: float
    asset_id: str


@dataclass(frozen=True, slots=True)
class ExitData:
    x: float
    y: float
    w: float
    h: float
    asset_id_inactive: str
    asset_id_active: str


@dataclass(frozen=True, slots=True)
class LevelData:
    schema_version: int
    id: str
    display_name: str
    order: int
    background_asset_id: str
    player_start: tuple[float, float]
    platforms: tuple[PlatformData, ...]
    pit: PitData
    enemy: EnemyData
    exit: ExitData
    source_file: str


def _fail(path: Path, field: str, reason: str) -> None:
    raise LevelDataError(str(path), field, reason)


def _mapping(path: Path, parent: dict[str, Any], field: str) -> dict[str, Any]:
    value = parent.get(field)
    if not isinstance(value, dict):
        _fail(path, field, "musí být objekt")
    return value


def _number(path: Path, parent: dict[str, Any], field: str, prefix: str = "") -> float:
    value = parent.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail(path, f"{prefix}{field}", "musí být číslo")
    return float(value)


def _string(path: Path, parent: dict[str, Any], field: str, prefix: str = "") -> str:
    value = parent.get(field)
    if not isinstance(value, str) or not value:
        _fail(path, f"{prefix}{field}", "musí být neprázdný text")
    return value


def _require_keys(path: Path, value: dict[str, Any], required: set[str], prefix: str) -> None:
    missing = required - value.keys()
    if missing:
        _fail(path, f"{prefix}{sorted(missing)[0]}", "povinné pole chybí")
    extra = value.keys() - required
    if extra:
        _fail(path, f"{prefix}{sorted(extra)[0]}", "neznámé pole")


def load_level(path: Path, known_asset_ids: set[str] | None = None) -> LevelData:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LevelDataError(str(path), "$", str(exc)) from exc
    if not isinstance(raw, dict):
        _fail(path, "$", "kořen musí být objekt")
    _require_keys(path, raw, REQUIRED_ROOT_FIELDS, "")
    if raw["schema_version"] != 1:
        _fail(path, "schema_version", "podporovaná hodnota je 1")
    level_id = _string(path, raw, "id")
    if not re.fullmatch(r"[a-z0-9_]+", level_id):
        _fail(path, "id", "povolená jsou malá písmena, číslice a podtržítko")
    display_name = _string(path, raw, "display_name")
    order = raw["order"]
    if isinstance(order, bool) or not isinstance(order, int) or order not in (1, 2, 3):
        _fail(path, "order", "musí být celé číslo 1 až 3")
    background_id = _string(path, raw, "background_asset_id")
    start = _mapping(path, raw, "player_start")
    _require_keys(path, start, {"x", "y"}, "player_start.")
    start_x = _number(path, start, "x", "player_start.")
    start_y = _number(path, start, "y", "player_start.")
    platforms_raw = raw["platforms"]
    if not isinstance(platforms_raw, list) or not platforms_raw:
        _fail(path, "platforms", "musí být neprázdný seznam")
    platforms: list[PlatformData] = []
    for index, item in enumerate(platforms_raw):
        prefix = f"platforms[{index}]."
        if not isinstance(item, dict):
            _fail(path, f"platforms[{index}]", "musí být objekt")
        _require_keys(path, item, {"x", "y", "w", "h", "asset_id"}, prefix)
        x = _number(path, item, "x", prefix)
        y = _number(path, item, "y", prefix)
        w = _number(path, item, "w", prefix)
        h = _number(path, item, "h", prefix)
        if w <= 0:
            _fail(path, f"{prefix}w", "musí být větší než 0")
        if h < config.LEVEL["min_platform_thickness"]:
            _fail(path, f"{prefix}h", f"minimum je {config.LEVEL['min_platform_thickness']:g}")
        platforms.append(PlatformData(x, y, w, h, _string(path, item, "asset_id", prefix)))
    pit_raw = _mapping(path, raw, "pit")
    _require_keys(path, pit_raw, {"x", "w", "kill_y"}, "pit.")
    pit = PitData(
        _number(path, pit_raw, "x", "pit."),
        _number(path, pit_raw, "w", "pit."),
        _number(path, pit_raw, "kill_y", "pit."),
    )
    if pit.x < 0 or pit.w <= 0 or pit.x + pit.w > config.DISPLAY["logical_size"][0]:
        _fail(path, "pit", "propast musí ležet uvnitř obrazu")
    if pit.x <= start_x < pit.x + pit.w:
        _fail(path, "player_start.x", "start nesmí být nad propastí")
    player_w, player_h = config.PLAYER["size"]
    stands = any(
        p.x <= start_x + player_w / 2 <= p.x + p.w and abs((start_y + player_h) - p.y) <= 2.0
        for p in platforms
    )
    if not stands:
        _fail(path, "player_start", "hráč musí stát na plošině")
    enemy_raw = _mapping(path, raw, "enemy")
    _require_keys(path, enemy_raw, {"x", "y", "patrol_min_x", "patrol_max_x", "asset_id"}, "enemy.")
    enemy = EnemyData(
        _number(path, enemy_raw, "x", "enemy."),
        _number(path, enemy_raw, "y", "enemy."),
        _number(path, enemy_raw, "patrol_min_x", "enemy."),
        _number(path, enemy_raw, "patrol_max_x", "enemy."),
        _string(path, enemy_raw, "asset_id", "enemy."),
    )
    if enemy.patrol_min_x >= enemy.patrol_max_x:
        _fail(path, "enemy.patrol_min_x", "musí být menší než patrol_max_x")
    if not enemy.patrol_min_x <= enemy.x <= enemy.patrol_max_x:
        _fail(path, "enemy.x", "musí ležet v trase hlídky")
    enemy_w, enemy_h = config.ENEMY["size"]
    patrol_supported = any(
        p.x <= enemy.patrol_min_x
        and enemy.patrol_max_x + enemy_w <= p.x + p.w
        and abs((enemy.y + enemy_h) - p.y) <= 2.0
        for p in platforms
    )
    if not patrol_supported:
        _fail(path, "enemy.patrol_min_x", "celá trasa musí ležet na jedné plošině")
    exit_raw = _mapping(path, raw, "exit")
    _require_keys(path, exit_raw, {"x", "y", "w", "h", "asset_id_inactive", "asset_id_active"}, "exit.")
    exit_data = ExitData(
        _number(path, exit_raw, "x", "exit."),
        _number(path, exit_raw, "y", "exit."),
        _number(path, exit_raw, "w", "exit."),
        _number(path, exit_raw, "h", "exit."),
        _string(path, exit_raw, "asset_id_inactive", "exit."),
        _string(path, exit_raw, "asset_id_active", "exit."),
    )
    if exit_data.w <= 0 or exit_data.h <= 0:
        _fail(path, "exit", "rozměry musí být kladné")
    if exit_data.x < pit.x + pit.w and exit_data.x + exit_data.w > pit.x:
        _fail(path, "exit.x", "východ se nesmí překrývat s propastí")
    asset_ids = [background_id, *(p.asset_id for p in platforms), enemy.asset_id, exit_data.asset_id_inactive, exit_data.asset_id_active]
    if known_asset_ids is not None:
        for asset_id in asset_ids:
            if asset_id not in known_asset_ids:
                _fail(path, "asset_id", f"neznámé asset ID {asset_id}")
    return LevelData(1, level_id, display_name, order, background_id, (start_x, start_y), tuple(platforms), pit, enemy, exit_data, str(path))


def load_all_levels(directory: Path, known_asset_ids: set[str] | None = None) -> tuple[LevelData, ...]:
    levels = tuple(load_level(path, known_asset_ids) for path in sorted(directory.glob("*.json")))
    if not levels:
        raise LevelDataError(str(directory), "$", "nebyla nalezena žádná prostředí")
    orders = [level.order for level in levels]
    if sorted(orders) != [1, 2, 3]:
        raise LevelDataError(str(directory), "order", "pořadí musí být právě 1, 2, 3 bez duplicit")
    ids = [level.id for level in levels]
    if len(ids) != len(set(ids)):
        raise LevelDataError(str(directory), "id", "identifikátory musí být unikátní")
    return tuple(sorted(levels, key=lambda level: level.order))
