from alzak import config
from alzak.core.geometry import RectF
from alzak.core.input import InputSnapshot
from alzak.sim.events import SimEvent
from alzak.sim.player import Player


FLOOR = [RectF(0, 300, 1000, 100)]


def jump_height(held_steps: int) -> float:
    player = Player(20, 204)
    start = player.y
    minimum = start
    for step in range(180):
        held = step < held_steps
        events = player.update(InputSnapshot(jump_pressed=step == 0, jump_held=held), FLOOR, config.SIM["dt"])
        minimum = min(minimum, player.y)
        if step > 2 and SimEvent.LANDED in events:
            break
    return start - minimum


def test_short_and_held_jump_have_different_height() -> None:
    assert jump_height(120) > jump_height(2) * 1.5


def test_coyote_timer_and_jump_buffer_windows() -> None:
    platform = [RectF(0, 300, 100, 100)]
    player = Player(80, 204, vx=520)
    for _ in range(5):
        player.update(InputSnapshot(right=True), platform, config.SIM["dt"])
    assert 0 < player.coyote_timer <= config.JUMP["coyote_time"]
    events = player.update(InputSnapshot(jump_pressed=True, jump_held=True), platform, config.SIM["dt"])
    assert SimEvent.JUMPED in events
    assert config.JUMP["coyote_time"] == 0.10
    assert config.JUMP["buffer_time"] == 0.12
