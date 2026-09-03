from __future__ import annotations

import os

import pygame

from alzak import config
from alzak.data.schema import LevelDataError
from alzak.render.presentation import Presentation
from alzak.render.text import render_text
from alzak.screens.error_screen import run_error_screen


def _draw_foundational_title(surface: pygame.Surface) -> None:
    surface.fill((15, 31, 47))
    render_text(surface, config.DISPLAY["title"], (960, 455), 84, (168, 238, 75), center=True)
    render_text(surface, "Načítání dema…", (960, 560), 34, (215, 228, 235), center=True)


def run() -> int:
    pygame.init()
    pygame.display.set_caption(config.DISPLAY["title"])
    presentation = Presentation.create()
    _draw_foundational_title(presentation.logical_surface)
    presentation.present()
    if os.environ.get("ALZAK_SMOKE_EXIT") == "1":
        pygame.quit()
        return 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                presentation.toggle_fullscreen()
        presentation.present()
        clock.tick(config.DISPLAY["target_fps"])
    pygame.quit()
    return 0


def main() -> int:
    try:
        return run()
    except LevelDataError as error:
        return run_error_screen(error)
