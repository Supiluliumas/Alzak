from __future__ import annotations

from dataclasses import dataclass

from alzak import config
from alzak.core.geometry import RectF


@dataclass(slots=True)
class Enemy:
    x: float
    y: float
    patrol_min_x: float
    patrol_max_x: float
    w: float = config.ENEMY["size"][0]
    h: float = config.ENEMY["size"][1]
    direction: int = 1
    hp: float = config.ENEMY["hp"]
    alive: bool = True
    hit_flash_timer: float = 0.0

    @property
    def rect(self) -> RectF:
        return RectF(self.x, self.y, self.w, self.h)

    def update(self, dt: float) -> None:
        self.hit_flash_timer = max(0.0, self.hit_flash_timer - dt)
        if not self.alive:
            return
        self.x += self.direction * config.ENEMY["speed"] * dt
        if self.x <= self.patrol_min_x:
            self.x = self.patrol_min_x
            self.direction = 1
        elif self.x >= self.patrol_max_x:
            self.x = self.patrol_max_x
            self.direction = -1

    def damage(self, amount: float) -> bool:
        if not self.alive:
            return False
        remaining = self.hp - amount
        self.hp = 0.0 if remaining <= config.ENEMY["hp_epsilon"] else remaining
        self.hit_flash_timer = config.ENEMY["hit_flash_time"]
        if self.hp == 0.0:
            self.alive = False
            return True
        return False
