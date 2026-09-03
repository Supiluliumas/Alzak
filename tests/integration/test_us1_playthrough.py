from pathlib import Path

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_level
from alzak.sim.level import LevelState


def test_move_jump_laser_exit_cycle() -> None:
    registry = AssetRegistry()
    level = LevelState.from_data(load_level(Path("levels/level_01_pobocka.json"), registry.ids))
    for _ in range(96):
        level.step(InputSnapshot(right=True), config.SIM["dt"])
    for step in range(130):
        level.step(InputSnapshot(right=True, jump_pressed=step == 0, jump_held=step < 70), config.SIM["dt"])
    assert level.player.x > level.data.pit.x + level.data.pit.w
    level.player.x = 950
    level.player.y = level.enemy.y + level.enemy.h - level.player.h
    level.player.vx = level.player.vy = 0
    level.player.facing = 1
    for _ in range(125):
        level.step(InputSnapshot(fire_held=True), config.SIM["dt"])
    assert not level.enemy.alive and level.exit.active
    level.player.x, level.player.y = level.exit.rect.x, level.exit.rect.y
    level.step(InputSnapshot(), config.SIM["dt"])
    assert level.completed
