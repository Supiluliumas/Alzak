from __future__ import annotations

import pygame

from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.render.world import draw_world
from alzak.sim.events import SimEvent
from alzak.sim.level import LevelState


class PlayScreen:
    def __init__(self, state: LevelState, registry: AssetRegistry) -> None:
        self.state = state
        self.registry = registry

    def update(self, inputs: InputSnapshot, dt: float) -> list[SimEvent]:
        return self.state.step(inputs, dt)

    def restart(self) -> None:
        self.state = self.state.restart()

    def draw(self, surface: pygame.Surface) -> None:
        draw_world(surface, self.state, self.registry)
