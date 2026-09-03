from __future__ import annotations

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.sim.laser import LaserMode
from alzak.sim.level import LevelState


def _blit_scaled(surface: pygame.Surface, image: pygame.Surface, rect: pygame.Rect) -> None:
    surface.blit(pygame.transform.smoothscale(image, rect.size), rect)


def draw_world(surface: pygame.Surface, state: LevelState, registry: AssetRegistry) -> None:
    background = registry.image(state.data.background_asset_id)
    _blit_scaled(surface, background, surface.get_rect())
    pit = state.data.pit
    pit_image = registry.image("img.pit")
    pit_height = config.LEVEL["pit_visual_height"]
    pit_rect = pygame.Rect(
        round(pit.x),
        round(pit.kill_y - pit_height),
        round(pit.w),
        round(pit_height),
    )
    _blit_scaled(surface, pit_image, pit_rect)
    for platform in state.data.platforms:
        image = registry.image(platform.asset_id)
        tile_w, tile_h = image.get_size()
        for x in range(round(platform.x), round(platform.x + platform.w), tile_w):
            for y in range(round(platform.y), round(platform.y + platform.h), tile_h):
                surface.blit(image, (x, y))
    exit_id = state.data.exit.asset_id_active if state.exit.active else state.data.exit.asset_id_inactive
    _blit_scaled(surface, registry.image(exit_id), pygame.Rect(round(state.exit.rect.x), round(state.exit.rect.y), round(state.exit.rect.w), round(state.exit.rect.h)))
    if state.enemy.alive:
        enemy_id = "img.enemy.hit" if state.enemy.hit_flash_timer > 0.0 else state.data.enemy.asset_id
        enemy_image = registry.image(enemy_id)
        if state.enemy.direction < 0:
            enemy_image = pygame.transform.flip(enemy_image, True, False)
        _blit_scaled(surface, enemy_image, pygame.Rect(round(state.enemy.x), round(state.enemy.y), round(state.enemy.w), round(state.enemy.h)))
    player = state.player
    if player.invuln_timer > 0.0:
        player_id = "img.player.hurt"
    elif not player.on_ground:
        player_id = "img.player.air"
    elif abs(player.vx) > config.PLAYER["movement_visual_threshold"]:
        player_id = "img.player.run"
    else:
        player_id = "img.player.idle"
    player_image = registry.image(player_id)
    if player.facing < 0:
        player_image = pygame.transform.flip(player_image, True, False)
    _blit_scaled(surface, player_image, pygame.Rect(round(player.x), round(player.y), round(player.w), round(player.h)))
    if state.laser.mode is LaserMode.FIRING:
        start_x, start_y = state.laser.start
        end_x = state.laser.end_x
        glow = config.LASER["draw_glow_color"]
        core = config.LASER["draw_core_color"]
        pygame.draw.line(surface, glow, (round(start_x), round(start_y)), (round(end_x), round(start_y)), config.LASER["draw_glow_thickness"])
        pygame.draw.line(surface, core, (round(start_x), round(start_y)), (round(end_x), round(start_y)), config.LASER["draw_core_thickness"])
