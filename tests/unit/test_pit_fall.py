from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_level
from alzak.sim.level import LevelState


def test_pit_costs_energy_and_preserves_enemy_state() -> None:
    registry = AssetRegistry()
    level = LevelState.from_data(load_level(Path("levels/level_01_pobocka.json"), registry.ids))
    level.enemy.damage(25)
    level.exit.active = True
    enemy_hp = level.enemy.hp
    enemy_x = level.enemy.x
    level.player.x = level.data.pit.x + 50
    level.player.y = level.data.pit.kill_y
    level.step(InputSnapshot())
    assert level.player.energy == 2
    assert (level.player.x, level.player.y) == level.data.player_start
    assert level.enemy.hp == enemy_hp
    assert level.enemy.x != enemy_x
    assert level.exit.active
