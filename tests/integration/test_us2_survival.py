from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_level
from alzak.sim.level import LevelState


def test_three_contacts_reach_failure_and_knockback_can_fall() -> None:
    registry = AssetRegistry()
    level = LevelState.from_data(load_level(Path("levels/level_01_pobocka.json"), registry.ids))
    for expected in (2, 1, 0):
        level.player.x = level.enemy.x
        level.player.y = level.enemy.y + level.enemy.h - level.player.h
        level.player.vx = level.player.vy = 0
        level.player.invuln_timer = 0
        level.step(InputSnapshot())
        assert level.player.energy == expected
    assert level.failed

    level = level.restart()
    level.player.x = level.data.pit.x + 10
    level.player.y = level.data.pit.kill_y
    level.player.vx = -100
    level.step(InputSnapshot())
    assert level.player.energy == 2
