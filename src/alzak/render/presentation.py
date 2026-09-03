from __future__ import annotations

from dataclasses import dataclass

import pygame

from alzak import config


def compute_viewport(
    window_w: int, window_h: int
) -> tuple[float, tuple[int, int], tuple[int, int]]:
    logical_w, logical_h = config.DISPLAY["logical_size"]
    if window_w <= 0 or window_h <= 0:
        raise ValueError("window dimensions must be positive")
    scale = min(window_w / logical_w, window_h / logical_h)
    dst = (round(logical_w * scale), round(logical_h * scale))
    offset = ((window_w - dst[0]) // 2, (window_h - dst[1]) // 2)
    return scale, dst, offset


@dataclass(slots=True)
class Presentation:
    window: pygame.Surface
    logical_surface: pygame.Surface
    fullscreen: bool = False

    @classmethod
    def create(cls) -> "Presentation":
        window = pygame.display.set_mode(config.DISPLAY["window_default_size"], pygame.RESIZABLE)
        logical = pygame.Surface(config.DISPLAY["logical_size"]).convert_alpha()
        return cls(window, logical)

    def present(self) -> None:
        window_size = self.window.get_size()
        _, dst, offset = compute_viewport(*window_size)
        self.window.fill(config.DISPLAY["letterbox_color"])
        scaled = pygame.transform.smoothscale(self.logical_surface, dst)
        self.window.blit(scaled, offset)
        pygame.display.flip()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        size = (0, 0) if self.fullscreen else config.DISPLAY["window_default_size"]
        self.window = pygame.display.set_mode(size, flags)
