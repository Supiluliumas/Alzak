from alzak import config
from alzak.sim.enemy import Enemy
from alzak.sim.laser import LaserMode, LaserState, update_laser
from alzak.sim.player import Player


def test_overheat_lock_and_reactivation_while_held() -> None:
    laser = LaserState()
    player = Player(10, 10)
    enemy = Enemy(1000, 10, 900, 1100)
    steps = 0
    while laser.mode is not LaserMode.LOCKED:
        update_laser(laser, player, [], enemy, True, config.SIM["dt"])
        steps += 1
    assert 1.4 <= steps * config.SIM["dt"] <= 1.6
    while laser.heat > config.LASER["reactivate_threshold"]:
        update_laser(laser, player, [], enemy, True, config.SIM["dt"])
    assert laser.mode is LaserMode.IDLE
    update_laser(laser, player, [], enemy, True, config.SIM["dt"])
    assert laser.mode is LaserMode.FIRING
