from __future__ import annotations

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.sim.laser import LaserMode
from alzak.sim.level import LevelState


RUN_ASSET_IDS = ("img.player.run", "img.player.run.2", "img.player.run.3")


def _blit_scaled(surface: pygame.Surface, image: pygame.Surface, rect: pygame.Rect) -> None:
    surface.blit(pygame.transform.smoothscale(image, rect.size), rect)


def _blit_platform(surface: pygame.Surface, image: pygame.Surface, x: int, y: int, width: int) -> None:
    tile_w, tile_h = image.get_size()
    right = x + width
    for tile_x in range(x, right, tile_w):
        visible_width = min(tile_w, right - tile_x)
        source = pygame.Rect(0, 0, visible_width, tile_h)
        surface.blit(image, (tile_x, y), source)


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
        _blit_platform(
            surface,
            image,
            round(platform.x),
            round(platform.y),
            round(platform.w),
        )
    exit_id = state.data.exit.asset_id_active if state.exit.active else state.data.exit.asset_id_inactive
    _blit_scaled(surface, registry.image(exit_id), pygame.Rect(round(state.exit.rect.x), round(state.exit.rect.y), round(state.exit.rect.w), round(state.exit.rect.h)))
    if state.enemy.alive:
        enemy_id = "img.enemy.hit" if state.enemy.hit_flash_timer > 0.0 else state.data.enemy.asset_id
        enemy_image = registry.image(enemy_id)
        if state.enemy.direction < 0:
            enemy_image = pygame.transform.flip(enemy_image, True, False)
        enemy_width, enemy_height = config.ENEMY["visual_size"]
        enemy_offset_x, enemy_offset_y = config.ENEMY["visual_offset"]
        enemy_rect = pygame.Rect(
            round(state.enemy.x + enemy_offset_x),
            round(state.enemy.y + enemy_offset_y),
            round(enemy_width),
            round(enemy_height),
        )
        _blit_scaled(surface, enemy_image, enemy_rect)
    player = state.player
    if player.invuln_timer > 0.0:
        player_id = "img.player.hurt"
    elif state.laser.mode is LaserMode.FIRING:
        player_id = "img.player.fire"
    elif not player.on_ground:
        player_id = "img.player.air"
    elif abs(player.vx) > config.PLAYER["movement_visual_threshold"]:
        frame = int(player.animation_time / config.PLAYER["run_frame_time"]) % len(RUN_ASSET_IDS)
        player_id = RUN_ASSET_IDS[frame]
    else:
        idle_phase = player.animation_time % config.PLAYER["idle_cycle_time"]
        player_id = "img.player.idle.blink" if idle_phase >= config.PLAYER["idle_blink_start"] else "img.player.idle"
    player_image = registry.image(player_id)
    if player.facing < 0:
        player_image = pygame.transform.flip(player_image, True, False)
    visual_w, visual_h = config.PLAYER["visual_size"]
    offset_x, offset_y = config.PLAYER["visual_offset"]
    player_rect = pygame.Rect(
        round(player.x + offset_x),
        round(player.y + offset_y),
        round(visual_w),
        round(visual_h),
    )
    _blit_scaled(surface, player_image, player_rect)
    if state.laser.mode is LaserMode.FIRING:
        start_x, start_y = state.laser.start
        end_x = state.laser.end_x
        glow = config.LASER["draw_glow_color"]
        core = config.LASER["draw_core_color"]
        start = (round(start_x), round(start_y))
        end = (round(end_x), round(start_y))
        pygame.draw.line(surface, glow, start, end, config.LASER["draw_glow_thickness"])
        pygame.draw.line(surface, core, start, end, config.LASER["draw_core_thickness"])
