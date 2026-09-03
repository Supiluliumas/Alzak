from alzak import config
from alzak.sim.enemy import Enemy


def _damage(enemy: Enemy, seconds: float) -> None:
    for _ in range(round(seconds / config.SIM["dt"])):
        enemy.damage(config.LASER["dps"] * config.SIM["dt"])


def test_enemy_defeat_time_and_damage_persistence() -> None:
    continuous = Enemy(0, 0, 0, 1)
    _damage(continuous, 1.0)
    assert not continuous.alive
    split = Enemy(0, 0, 0, 1)
    _damage(split, 0.4)
    hp_after_first_burst = split.hp
    split.update(3.0)
    assert split.hp == hp_after_first_burst
    _damage(split, 0.6)
    assert not split.alive
