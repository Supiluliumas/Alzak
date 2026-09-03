from __future__ import annotations

from dataclasses import dataclass

from alzak import config
from alzak.core.geometry import RectF
from alzak.core.input import InputSnapshot
from alzak.data.loader import LevelData
from alzak.sim.enemy import Enemy
from alzak.sim.events import SimEvent
from alzak.sim.laser import LaserState, update_laser
from alzak.sim.player import Player


@dataclass(slots=True)
class ExitState:
    rect: RectF
    active: bool = False


@dataclass(slots=True)
class LevelState:
    data: LevelData
    player: Player
    enemy: Enemy
    laser: LaserState
    exit: ExitState
    completed: bool = False
    failed: bool = False

    @classmethod
    def from_data(cls, data: LevelData) -> "LevelState":
        player = Player(*data.player_start)
        enemy = Enemy(
            data.enemy.x,
            data.enemy.y,
            data.enemy.patrol_min_x,
            data.enemy.patrol_max_x,
        )
        exit_state = ExitState(RectF(data.exit.x, data.exit.y, data.exit.w, data.exit.h))
        return cls(data, player, enemy, LaserState(), exit_state)

    @property
    def platforms(self) -> tuple[RectF, ...]:
        return tuple(RectF(item.x, item.y, item.w, item.h) for item in self.data.platforms)

    def restart(self) -> "LevelState":
        return LevelState.from_data(self.data)

    def step(self, inputs: InputSnapshot, dt: float = config.SIM["dt"]) -> list[SimEvent]:
        if self.completed or self.failed:
            return []
        events = update_laser(self.laser, self.player, self.platforms, self.enemy, inputs.fire_held, dt)
        self.enemy.update(dt)
        events.extend(self.player.update(inputs, self.platforms, dt))
        if self.enemy.alive and self.player.rect.intersects(self.enemy.rect):
            if self.player.hurt(self.enemy.rect.centerx):
                events.append(SimEvent.PLAYER_HURT)
        pit = self.data.pit
        player_center_x = self.player.rect.centerx
        if pit.x <= player_center_x <= pit.x + pit.w and self.player.rect.bottom >= pit.kill_y:
            self.player.fall_and_respawn(self.data.player_start)
            events.extend(self.laser.deactivate())
            events.append(SimEvent.PLAYER_FELL)
        if not self.enemy.alive and not self.exit.active:
            self.exit.active = True
            events.append(SimEvent.EXIT_ACTIVATED)
        if self.player.energy <= 0:
            self.failed = True
            self.completed = False
            events.extend(self.laser.deactivate())
            events.append(SimEvent.PLAYER_DEFEATED)
            return events
        if self.exit.active and self.player.rect.intersects(self.exit.rect):
            self.completed = True
            events.append(SimEvent.LEVEL_COMPLETED)
        return events
