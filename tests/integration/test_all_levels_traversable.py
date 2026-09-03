from pathlib import Path

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_all_levels
from alzak.sim.level import LevelState
from alzak.sim.session import Session


def _step_healthy(session: Session, inputs: InputSnapshot) -> None:
    session.current.step(inputs, config.SIM["dt"])
    assert session.current.player.energy == config.ENERGY["max"]
    assert not session.current.failed


def test_all_three_levels_are_physically_traversable_without_teleports() -> None:
    registry = AssetRegistry()
    session = Session.start(load_all_levels(Path("levels"), registry.ids))
    visited: list[str] = []

    while not session.finished:
        level = session.current
        visited.append(level.data.id)

        for _ in range(600):
            _step_healthy(session, InputSnapshot(right=True))
            if level.player.x >= level.data.pit.x - 70:
                break
        else:
            raise AssertionError("player did not reach the jump point")

        for step in range(180):
            _step_healthy(
                session,
                InputSnapshot(right=True, jump_pressed=step == 0, jump_held=True),
            )
            if level.player.on_ground and level.player.x > level.data.pit.x:
                break
        else:
            raise AssertionError("player did not land beyond the pit")

        for _ in range(150):
            _step_healthy(session, InputSnapshot(fire_held=True))
            if not level.enemy.alive:
                break
        else:
            raise AssertionError("enemy was not defeated before laser lockout")

        for _ in range(500):
            _step_healthy(session, InputSnapshot(right=True))
            if level.completed:
                break
        else:
            raise AssertionError("player did not reach the active exit")

        session.advance()

    assert visited == ["pobocka", "sklad", "kancelar"]


def test_every_elevated_platform_is_reachable_by_jumping() -> None:
    registry = AssetRegistry()
    for data in load_all_levels(Path("levels"), registry.ids):
        level = LevelState.from_data(data)

        while level.player.x < data.pit.x - 70:
            level.step(InputSnapshot(right=True), config.SIM["dt"])
        for step in range(180):
            level.step(
                InputSnapshot(right=True, jump_pressed=step == 0, jump_held=True),
                config.SIM["dt"],
            )
            if level.player.on_ground and level.player.x > data.pit.x:
                break

        first, second = data.platforms[2:4]
        while level.player.x < first.x - 90:
            level.step(InputSnapshot(right=True), config.SIM["dt"])
        for step in range(160):
            level.step(
                InputSnapshot(right=step >= 24, jump_pressed=step == 0, jump_held=True),
                config.SIM["dt"],
            )
            if level.player.on_ground and level.player.rect.bottom == first.y:
                break
        assert level.player.rect.bottom == first.y, f"{data.id}: first ledge unreachable"

        while level.player.x < first.x + first.w - 100:
            level.step(InputSnapshot(right=True), config.SIM["dt"])
        for step in range(180):
            level.step(
                InputSnapshot(right=step >= 16, jump_pressed=step == 0, jump_held=True),
                config.SIM["dt"],
            )
            if level.player.on_ground and level.player.rect.bottom == second.y:
                break
        assert level.player.rect.bottom == second.y, f"{data.id}: second ledge unreachable"
        assert level.player.energy == config.ENERGY["max"]
