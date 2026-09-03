from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.data.loader import load_all_levels
from alzak.sim.session import Session


def session() -> Session:
    registry = AssetRegistry()
    return Session.start(load_all_levels(Path("levels"), registry.ids))


def test_order_energy_refill_and_finish() -> None:
    game = session()
    assert game.level_ids == ("pobocka", "sklad", "kancelar")
    for expected_index in (1, 2):
        game.current.player.energy = 1
        game.current.completed = True
        assert game.advance()
        assert game.level_index == expected_index
        assert game.current.player.energy == 3
    game.current.completed = True
    game.advance()
    assert game.finished


def test_restart_demo_returns_to_first_level() -> None:
    game = session()
    game.current.completed = True
    game.advance()
    game.restart_demo()
    assert game.level_index == 0 and not game.finished and game.current.player.energy == 3
