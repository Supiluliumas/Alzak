from alzak import config
from alzak.core.geometry import RectF
from alzak.sim.enemy import Enemy
from alzak.sim.laser import HitKind, muzzle, resolve_beam
from alzak.sim.player import Player


def test_muzzle_is_mirrored_and_collision_thickness_is_configured() -> None:
    player = Player(100, 200)
    assert muzzle(player) == (152, 238)
    player.facing = -1
    assert muzzle(player) == (112, 238)
    assert config.LASER["collision_thickness"] == 16


def test_nearest_platform_blocks_enemy_and_edge_is_fallback() -> None:
    enemy = Enemy(500, 200, 500, 600)
    end, kind = resolve_beam((100, 238), 1, [RectF(300, 220, 40, 80)], enemy)
    assert (end, kind) == (300, HitKind.PLATFORM)
    end, kind = resolve_beam((100, 238), 1, [], enemy)
    assert (end, kind) == (500, HitKind.ENEMY)
    end, kind = resolve_beam((100, 100), -1, [], None)
    assert (end, kind) == (0, HitKind.NONE)
