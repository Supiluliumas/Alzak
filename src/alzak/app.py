from __future__ import annotations

import os

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.core.clock import FixedStepClock
from alzak.core.input import from_pygame
from alzak.data.loader import load_level
from alzak.data.schema import LevelDataError
from alzak.paths import levels_root
from alzak.render.presentation import Presentation
from alzak.screens.error_screen import run_error_screen
from alzak.screens.play import PlayScreen
from alzak.sim.level import LevelState


def run() -> int:
    pygame.init()
    pygame.display.set_caption(config.DISPLAY["title"])
    presentation = Presentation.create()
    registry = AssetRegistry()
    level_data = load_level(levels_root() / "level_01_pobocka.json", registry.ids)
    play = PlayScreen(LevelState.from_data(level_data), registry)
    play.draw(presentation.logical_surface)
    presentation.present()
    if os.environ.get("ALZAK_SMOKE_EXIT") == "1":
        pygame.quit()
        return 0
    clock = pygame.time.Clock()
    fixed = FixedStepClock()
    running = True
    while running:
        jump_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    presentation.toggle_fullscreen()
                elif event.key == pygame.K_r:
                    play.restart()
                elif event.key == pygame.K_SPACE:
                    jump_pressed = True
        frame_dt = clock.tick(config.DISPLAY["target_fps"]) / 1000.0
        inputs = from_pygame(pygame.key.get_pressed(), jump_pressed)
        for _ in range(fixed.consume(frame_dt)):
            play.update(inputs, config.SIM["dt"])
            inputs = type(inputs)(inputs.left, inputs.right, False, inputs.jump_held, inputs.fire_held)
        play.draw(presentation.logical_surface)
        presentation.present()
    pygame.quit()
    return 0


def main() -> int:
    try:
        return run()
    except LevelDataError as error:
        return run_error_screen(error)
