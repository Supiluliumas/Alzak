from __future__ import annotations

from dataclasses import dataclass

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.render.text import render_text
from alzak.sim.level import LevelState


@dataclass(frozen=True, slots=True)
class HudSnapshot:
    energy: int
    heat: float
    level_name: str
    progress: str


def hud_snapshot(state: LevelState, level_index: int, total: int) -> HudSnapshot:
    return HudSnapshot(state.player.energy, state.laser.heat, state.data.display_name, f"{level_index + 1}/{total}")


def draw_hud(surface: pygame.Surface, state: LevelState, level_index: int, total: int, registry: AssetRegistry) -> None:
    model = hud_snapshot(state, level_index, total)
    icon_size = config.HUD["energy_icon_size"]
    origin_x, origin_y = config.HUD["energy_origin"]
    for index in range(config.ENERGY["max"]):
        asset_id = "img.hud.energy_full" if index < model.energy else "img.hud.energy_empty"
        image = pygame.transform.smoothscale(registry.image(asset_id), icon_size)
        surface.blit(image, (origin_x + index * (icon_size[0] + config.HUD["energy_gap"]), origin_y))
    heat_origin = config.HUD["heat_bar_origin"]
    heat_size = config.HUD["heat_bar_size"]
    fill = pygame.transform.smoothscale(registry.image("img.hud.heat_fill"), heat_size)
    fill_width = round(heat_size[0] * model.heat)
    if fill_width > 0:
        surface.blit(fill.subsurface((0, 0, fill_width, heat_size[1])), heat_origin)
    frame = pygame.transform.smoothscale(registry.image("img.hud.heat_frame"), heat_size)
    surface.blit(frame, heat_origin)
    text_x, text_y = config.HUD["text_origin"]
    render_text(surface, model.level_name, (text_x, text_y), config.HUD["font_size_hud"], config.HUD["color_normal"])
    render_text(surface, model.progress, (text_x, text_y + config.HUD["font_size_hud"] + config.HUD["energy_gap"]), config.HUD["font_size_hud"], config.UI["menu_selected_color"])
