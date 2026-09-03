from __future__ import annotations

import pygame

from alzak.paths import assets_root


def get_font(size: int) -> pygame.font.Font:
    if not pygame.font.get_init():
        pygame.font.init()
    bundled = assets_root() / "fonts" / "DejaVuSans-Bold.ttf"
    return pygame.font.Font(str(bundled) if bundled.exists() else None, size)


def render_text(
    surface: pygame.Surface,
    value: str,
    position: tuple[int, int],
    size: int,
    color: tuple[int, int, int],
    *,
    center: bool = False,
) -> pygame.Rect:
    image = get_font(size).render(value, True, color)
    rect = image.get_rect(center=position) if center else image.get_rect(topleft=position)
    surface.blit(image, rect)
    return rect
