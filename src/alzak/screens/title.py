from __future__ import annotations

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.render.text import render_text


OPTIONS = ("Spustit", "Ukončit")


def draw_title(surface: pygame.Surface, registry: AssetRegistry, selected: int = 0) -> None:
    background = pygame.transform.smoothscale(registry.image("img.bg.pobocka"), surface.get_size())
    surface.blit(background, (0, 0))
    veil = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    veil.fill(config.UI["overlay_color"])
    surface.blit(veil, (0, 0))
    hero = pygame.transform.smoothscale(registry.image("img.player.idle"), (192, 288))
    surface.blit(hero, hero.get_rect(center=(420, 565)))
    render_text(surface, "ALZÁK", (1120, 260), config.HUD["font_size_title"], config.UI["menu_selected_color"], center=True)
    render_text(surface, "MISE SPLNĚNA!", (1120, 355), 54, config.UI["menu_color"], center=True)
    for index, option in enumerate(OPTIONS):
        color = config.UI["menu_selected_color"] if index == selected else config.UI["menu_color"]
        render_text(surface, option, (1120, 540 + index * config.UI["menu_line_gap"]), config.HUD["font_size_menu"], color, center=True)
    render_text(surface, "Šipky nahoru/dolů: výběr  |  Enter: potvrdit", (1120, 775), 28, config.UI["hint_color"], center=True)
    render_text(surface, "Pohyb: šipky  |  Skok: mezerník  |  Laser: X  |  Pauza: Esc  |  Restart: R", (960, 980), 25, config.UI["hint_color"], center=True)
