from __future__ import annotations

import os

import pygame

from alzak import config
from alzak.data.schema import LevelDataError
from alzak.render.text import render_text


def draw_error(surface: pygame.Surface, error: LevelDataError) -> None:
    surface.fill((35, 11, 18))
    render_text(surface, "Chyba dat prostředí", (960, 245), 72, (255, 110, 110), center=True)
    render_text(surface, f"Soubor: {error.file}", (180, 420), 34, (245, 235, 235))
    render_text(surface, f"Pole: {error.field}", (180, 480), 34, (245, 235, 235))
    render_text(surface, f"Důvod: {error.reason}", (180, 540), 34, (245, 235, 235))
    render_text(surface, "Stiskněte Enter nebo Escape", (960, 735), 32, (190, 170, 175), center=True)


def run_error_screen(error: LevelDataError) -> int:
    print(str(error), file=__import__("sys").stderr)
    if os.environ.get("ALZAK_NONINTERACTIVE_ERROR") == "1":
        return 2
    pygame.init()
    window = pygame.display.set_mode(config.DISPLAY["window_default_size"])
    logical = pygame.Surface(config.DISPLAY["logical_size"])
    draw_error(logical, error)
    scaled = pygame.transform.smoothscale(logical, window.get_size())
    window.blit(scaled, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN)
            ):
                pygame.quit()
                return 2
