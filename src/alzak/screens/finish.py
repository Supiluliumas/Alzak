from __future__ import annotations

import pygame

from alzak import config
from alzak.render.text import render_text


OPTIONS = ("Spustit znovu", "Ukončit")


def draw_finish(surface: pygame.Surface, selected: int = 0) -> None:
    surface.fill((18, 58, 55))
    render_text(surface, "DEMO DOKONČENO!", (960, 285), config.HUD["font_size_title"], config.UI["menu_selected_color"], center=True)
    render_text(surface, "Pobočka, sklad i kancelář jsou v bezpečí.", (960, 400), 36, config.UI["hint_color"], center=True)
    for index, option in enumerate(OPTIONS):
        color = config.UI["menu_selected_color"] if index == selected else config.UI["menu_color"]
        render_text(surface, option, (960, 570 + index * config.UI["menu_line_gap"]), config.HUD["font_size_menu"], color, center=True)
