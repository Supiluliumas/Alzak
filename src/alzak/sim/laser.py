from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Sequence

from alzak import config
from alzak.core.geometry import RectF
from alzak.sim.enemy import Enemy
from alzak.sim.events import SimEvent
from alzak.sim.player import Player


class LaserMode(Enum):
    IDLE = auto()
    FIRING = auto()
    LOCKED = auto()


class HitKind(Enum):
    NONE = auto()
    PLATFORM = auto()
    ENEMY = auto()


@dataclass(slots=True)
class LaserState:
    mode: LaserMode = LaserMode.IDLE
    heat: float = 0.0
    start: tuple[float, float] = (0.0, 0.0)
    end_x: float = 0.0
    hit_kind: HitKind = HitKind.NONE

    def deactivate(self) -> list[SimEvent]:
        if self.mode is LaserMode.FIRING:
            self.mode = LaserMode.IDLE
            return [SimEvent.LASER_STOPPED]
        return []


def muzzle(player: Player) -> tuple[float, float]:
    offset_x, offset_y = config.LASER["muzzle_offset"]
    x = player.x + (offset_x if player.facing > 0 else player.w - offset_x)
    return x, player.y + offset_y


def resolve_beam(
    start: tuple[float, float],
    facing: int,
    platforms: Sequence[RectF],
    enemy: Enemy | None,
) -> tuple[float, HitKind]:
    start_x, start_y = start
    half = config.LASER["collision_thickness"] / 2.0
    top, bottom = start_y - half, start_y + half
    logical_width = float(config.DISPLAY["logical_size"][0])
    max_range = config.LASER["max_range"]
    limit = max(0.0, start_x - max_range) if facing < 0 else min(logical_width, start_x + max_range)
    candidates: list[tuple[float, HitKind]] = []

    def consider(rect: RectF, kind: HitKind) -> None:
        if rect.bottom <= top or rect.top >= bottom:
            return
        edge = rect.right if facing < 0 else rect.left
        if (facing < 0 and edge <= start_x) or (facing > 0 and edge >= start_x):
            candidates.append((edge, kind))

    for platform in platforms:
        consider(platform, HitKind.PLATFORM)
    if enemy is not None and enemy.alive:
        consider(enemy.rect, HitKind.ENEMY)
    if not candidates:
        return limit, HitKind.NONE
    candidates.sort(key=lambda item: abs(item[0] - start_x))
    return candidates[0]


def update_laser(
    laser: LaserState,
    player: Player,
    platforms: Sequence[RectF],
    enemy: Enemy,
    fire_held: bool,
    dt: float,
) -> list[SimEvent]:
    events: list[SimEvent] = []
    was_firing = laser.mode is LaserMode.FIRING
    if laser.mode is LaserMode.LOCKED:
        laser.heat = max(0.0, laser.heat - dt / config.LASER["cool_time_from_full"])
        if laser.heat <= config.LASER["reactivate_threshold"]:
            laser.mode = LaserMode.IDLE
    elif fire_held:
        if laser.mode is LaserMode.IDLE:
            laser.mode = LaserMode.FIRING
            events.append(SimEvent.LASER_STARTED)
        laser.heat = min(1.0, laser.heat + dt / config.LASER["heat_time_to_full"])
        laser.start = muzzle(player)
        laser.end_x, laser.hit_kind = resolve_beam(laser.start, player.facing, platforms, enemy)
        if laser.hit_kind is HitKind.ENEMY:
            defeated = enemy.damage(config.LASER["dps"] * dt)
            events.append(SimEvent.ENEMY_HIT)
            if defeated:
                events.append(SimEvent.ENEMY_DEFEATED)
        if laser.heat >= 1.0:
            laser.mode = LaserMode.LOCKED
            events.extend((SimEvent.LASER_OVERHEATED, SimEvent.LASER_STOPPED))
    else:
        if laser.mode is LaserMode.FIRING:
            laser.mode = LaserMode.IDLE
            events.append(SimEvent.LASER_STOPPED)
        laser.heat = max(0.0, laser.heat - dt / config.LASER["cool_time_from_full"])
    if not was_firing and laser.mode is not LaserMode.FIRING:
        laser.hit_kind = HitKind.NONE
    return events
