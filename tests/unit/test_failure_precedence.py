from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_level
from alzak.sim.level import LevelState


def test_failure_wins_over_enemy_defeat_and_exit_completion() -> None:
    registry = AssetRegistry()
    level = LevelState.from_data(load_level(Path("levels/level_01_pobocka.json"), registry.ids))
    level.player.energy = 1
    level.player.x = level.data.pit.x + 20
    level.player.y = level.data.pit.kill_y
    level.enemy.damage(level.enemy.hp)
    level.step(InputSnapshot())
    assert level.failed
    assert not level.completed
    assert level.exit.active
