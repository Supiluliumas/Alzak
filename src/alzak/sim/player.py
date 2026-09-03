from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from alzak import config
from alzak.core.geometry import RectF
from alzak.core.input import InputSnapshot
from alzak.sim.events import SimEvent
from alzak.sim.physics import move_and_collide


def _approach(value: float, target: float, amount: float) -> float:
    if value < target:
        return min(target, value + amount)
    return max(target, value - amount)


@dataclass(slots=True)
class Player:
    x: float
    y: float
    w: float = config.PLAYER["size"][0]
    h: float = config.PLAYER["size"][1]
    vx: float = 0.0
    vy: float = 0.0
    facing: int = 1
    on_ground: bool = True
    coyote_timer: float = 0.0
    jump_buffer_timer: float = 0.0
    jump_held: bool = False
    energy: int = config.ENERGY["max"]
    invuln_timer: float = 0.0

    @property
    def rect(self) -> RectF:
        return RectF(self.x, self.y, self.w, self.h)

    def update(self, inputs: InputSnapshot, solids: Sequence[RectF], dt: float) -> list[SimEvent]:
        events: list[SimEvent] = []
        was_grounded = self.on_ground
        self.coyote_timer = max(0.0, self.coyote_timer - dt)
        self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)
        if inputs.jump_pressed:
            self.jump_buffer_timer = config.JUMP["buffer_time"]
        direction = int(inputs.right) - int(inputs.left)
        if direction:
            self.facing = direction
            accel = config.PLAYER["ground_accel"] if self.on_ground else config.PLAYER["air_accel"]
            self.vx = _approach(self.vx, direction * config.PLAYER["max_run_speed"], accel * dt)
        else:
            friction = config.PLAYER["ground_friction"] if self.on_ground else config.PLAYER["air_friction"]
            self.vx = _approach(self.vx, 0.0, friction * dt)
        can_jump = self.on_ground or self.coyote_timer > 0.0
        if self.jump_buffer_timer > 0.0 and can_jump:
            self.vy = config.JUMP["velocity"]
            self.on_ground = False
            self.coyote_timer = 0.0
            self.jump_buffer_timer = 0.0
            self.jump_held = True
            events.append(SimEvent.JUMPED)
        if self.jump_held and not inputs.jump_held and self.vy < 0.0:
            self.vy *= config.JUMP["cut_multiplier"]
            self.jump_held = False
        self.vy = min(self.vy + config.PLAYER["gravity"] * dt, config.PLAYER["max_fall_speed"])
        collision = move_and_collide(self, solids, dt)
        self.on_ground = collision.ground
        if was_grounded and not self.on_ground and self.vy >= 0.0:
            self.coyote_timer = config.JUMP["coyote_time"]
        if self.on_ground:
            self.jump_held = False
            if not was_grounded:
                events.append(SimEvent.LANDED)
            if self.jump_buffer_timer > 0.0:
                self.vy = config.JUMP["velocity"]
                self.on_ground = False
                self.jump_buffer_timer = 0.0
                self.jump_held = True
                events.append(SimEvent.JUMPED)
        self.invuln_timer = max(0.0, self.invuln_timer - dt)
        return events
