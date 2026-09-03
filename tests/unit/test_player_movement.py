from alzak import config
from alzak.core.geometry import RectF
from alzak.core.input import InputSnapshot
from alzak.sim.player import Player


FLOOR = [RectF(0, 200, 2000, 100)]


def test_acceleration_cap_and_friction() -> None:
    player = Player(20, 104)
    for _ in range(240):
        player.update(InputSnapshot(right=True), FLOOR, config.SIM["dt"])
    assert player.vx == config.PLAYER["max_run_speed"]
    for _ in range(60):
        player.update(InputSnapshot(), FLOOR, config.SIM["dt"])
    assert player.vx == 0


def test_both_arrows_apply_no_acceleration() -> None:
    player = Player(20, 104)
    player.update(InputSnapshot(left=True, right=True), FLOOR, config.SIM["dt"])
    assert player.vx == 0
