from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_all_levels
from alzak.sim.session import Session


def test_headless_full_three_level_run_and_restart() -> None:
    registry = AssetRegistry()
    game = Session.start(load_all_levels(Path("levels"), registry.ids))
    visited = []
    for _ in range(3):
        visited.append(game.current.data.id)
        game.current.enemy.damage(game.current.enemy.hp)
        game.current.player.x = game.current.exit.rect.x
        game.current.player.y = game.current.exit.rect.y
        game.current.step(InputSnapshot())
        assert game.current.completed
        game.advance()
    assert visited == ["pobocka", "sklad", "kancelar"]
    assert game.finished
    game.restart_demo()
    assert game.current.data.id == "pobocka" and game.current.player.energy == 3
