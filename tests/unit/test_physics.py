from dataclasses import dataclass

from alzak.core.geometry import RectF
from alzak.sim.physics import move_and_collide


@dataclass
class Body:
    x: float
    y: float
    w: float
    h: float
    vx: float
    vy: float


def test_landing_and_side_collision() -> None:
    floor = RectF(0, 100, 300, 40)
    falling = Body(40, 70, 20, 20, 0, 100)
    collision = move_and_collide(falling, [floor], 0.2)
    assert collision.ground and falling.y == 80 and falling.vy == 0
    wall = RectF(100, 0, 40, 200)
    runner = Body(70, 30, 20, 20, 100, 0)
    collision = move_and_collide(runner, [wall], 0.2)
    assert collision.right and runner.x == 80 and runner.vx == 0


def test_max_fall_step_does_not_tunnel_and_corner_does_not_stick() -> None:
    floor = RectF(0, 100, 300, 32)
    body = Body(20, 76, 20, 20, 70, 1500)
    collision = move_and_collide(body, [floor], 1 / 120)
    assert collision.ground
    assert body.y == 80
    body.vx = -70
    body.vy = -20
    move_and_collide(body, [floor], 1 / 120)
    assert body.vx < 0
