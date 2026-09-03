from alzak import config
from alzak.sim.player import Player


def test_energy_hit_knockback_and_invulnerability() -> None:
    player = Player(100, 100)
    assert player.energy == 3
    assert player.hurt(200)
    assert player.energy == 2 and player.vx < 0 and player.vy < 0
    assert not player.hurt(200)
    assert player.energy == 2
    player.invuln_timer = config.ENERGY["invuln_time"]
    elapsed = 0.0
    while player.invuln_timer > 0:
        player.invuln_timer = max(0, player.invuln_timer - config.SIM["dt"])
        elapsed += config.SIM["dt"]
    assert 0.9 <= elapsed <= 1.1
    assert player.hurt(200) and player.energy == 1
