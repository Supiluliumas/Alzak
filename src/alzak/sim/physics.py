from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from alzak.core.geometry import RectF


class MovingBody(Protocol):
    x: float
    y: float
    w: float
    h: float
    vx: float
    vy: float


@dataclass(frozen=True, slots=True)
class CollisionResult:
    left: bool = False
    right: bool = False
    ceiling: bool = False
    ground: bool = False


def move_and_collide(body: MovingBody, solids: Sequence[RectF], dt: float) -> CollisionResult:
    hit_left = hit_right = hit_ceiling = hit_ground = False
    body.x += body.vx * dt
    rect = RectF(body.x, body.y, body.w, body.h)
    for solid in solids:
        if not rect.intersects(solid):
            continue
        if body.vx > 0:
            body.x = solid.left - body.w
            hit_right = True
        elif body.vx < 0:
            body.x = solid.right
            hit_left = True
        body.vx = 0.0
        rect.x = body.x
    body.y += body.vy * dt
    rect = RectF(body.x, body.y, body.w, body.h)
    for solid in solids:
        if not rect.intersects(solid):
            continue
        if body.vy > 0:
            body.y = solid.top - body.h
            hit_ground = True
        elif body.vy < 0:
            body.y = solid.bottom
            hit_ceiling = True
        body.vy = 0.0
        rect.y = body.y
    return CollisionResult(hit_left, hit_right, hit_ceiling, hit_ground)
