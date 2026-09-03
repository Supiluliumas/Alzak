from __future__ import annotations

import pygame

from alzak import config
from alzak.render.text import render_text


OPTIONS = ("Opakovat prostředí", "Ukončit hru")


def draw_gameover(surface: pygame.Surface, selected: int = 0) -> None:
    overlay = pygame.Surface(config.DISPLAY["logical_size"], pygame.SRCALPHA)
    overlay.fill(config.UI["overlay_color"])
    surface.blit(overlay, (0, 0))
    render_text(surface, "ENERGIE VYČERPÁNA", (960, 330), config.HUD["font_size_title"], config.HUD["color_warning"], center=True)
    for index, option in enumerate(OPTIONS):
        color = config.UI["menu_selected_color"] if index == selected else config.UI["menu_color"]
        render_text(surface, option, (960, 520 + index * config.UI["menu_line_gap"]), config.HUD["font_size_menu"], color, center=True)
