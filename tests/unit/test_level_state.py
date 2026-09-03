from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_level
from alzak.sim.level import LevelState


def state() -> LevelState:
    registry = AssetRegistry()
    return LevelState.from_data(load_level(Path("levels/level_01_pobocka.json"), registry.ids))


def test_exit_only_activates_after_enemy_defeat() -> None:
    level = state()
    level.player.x, level.player.y = level.exit.rect.x, level.exit.rect.y
    level.step(InputSnapshot())
    assert not level.completed and not level.exit.active
    level.enemy.damage(level.enemy.hp)
    level.step(InputSnapshot())
    assert level.exit.active and level.completed
