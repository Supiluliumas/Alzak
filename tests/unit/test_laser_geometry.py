from alzak import config
from alzak.core.geometry import RectF
from alzak.sim.enemy import Enemy
from alzak.sim.laser import HitKind, LaserState, muzzle, resolve_beam, update_laser
from alzak.sim.player import Player


def test_muzzle_is_mirrored_and_collision_thickness_is_configured() -> None:
    player = Player(100, 200)
    assert muzzle(player) == (211, 218)
    player.facing = -1
    assert muzzle(player) == (53, 218)
    assert config.LASER["collision_thickness"] == 16


def test_nearest_platform_blocks_enemy_and_edge_is_fallback() -> None:
    enemy = Enemy(500, 200, 500, 600)
    end, kind = resolve_beam((100, 238), 1, [RectF(300, 220, 40, 80)], enemy)
    assert (end, kind) == (300, HitKind.PLATFORM)
    end, kind = resolve_beam((100, 238), 1, [], enemy)
    assert (end, kind) == (500, HitKind.ENEMY)
    end, kind = resolve_beam((100, 100), -1, [], None)
    assert (end, kind) == (0, HitKind.NONE)


def test_beam_range_is_finite_and_clamped_to_screen() -> None:
    end, kind = resolve_beam((100, 100), 1, [], None)
    assert (end, kind) == (100 + config.LASER["max_range"], HitKind.NONE)
    end, kind = resolve_beam((1800, 100), 1, [], None)
    assert (end, kind) == (config.DISPLAY["logical_size"][0], HitKind.NONE)


def test_beam_follows_facing_changes_while_fire_is_held() -> None:
    player = Player(100, 200)
    enemy = Enemy(500, 200, 500, 600)
    laser = LaserState()
    update_laser(laser, player, [], enemy, True, config.SIM["dt"])
    right_start = laser.start
    assert laser.end_x == enemy.rect.left

    player.facing = -1
    update_laser(laser, player, [], enemy, True, config.SIM["dt"])
    assert laser.start != right_start
    assert laser.end_x == 0.0
