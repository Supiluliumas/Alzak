from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.data.loader import load_level
from alzak.screens.play import PlayScreen
from alzak.sim.laser import LaserMode
from alzak.sim.level import LevelState


def test_restart_restores_all_initial_components() -> None:
    registry = AssetRegistry()
    data = load_level(Path("levels/level_01_pobocka.json"), registry.ids)
    play = PlayScreen(LevelState.from_data(data), registry)
    play.state.player.x = 900
    play.state.player.energy = 1
    play.state.laser.heat = 0.9
    play.state.laser.mode = LaserMode.LOCKED
    play.state.enemy.damage(50)
    play.state.exit.active = True
    play.restart()
    state = play.state
    assert (state.player.x, state.player.y) == data.player_start
    assert state.player.energy == 3
    assert state.laser.heat == 0 and state.laser.mode is LaserMode.IDLE
    assert state.enemy.hp == 100 and state.enemy.alive
    assert not state.exit.active
