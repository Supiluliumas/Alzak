from alzak.sim.enemy import Enemy


def test_enemy_turns_at_both_patrol_edges() -> None:
    enemy = Enemy(0, 0, 0, 10)
    for _ in range(100):
        enemy.update(0.01)
        assert 0 <= enemy.x <= 10
    assert enemy.direction in (-1, 1)
    enemy.x = 10
    enemy.direction = 1
    enemy.update(0.01)
    assert enemy.x == 10 and enemy.direction == -1
    enemy.x = 0
    enemy.direction = -1
    enemy.update(0.01)
    assert enemy.x == 0 and enemy.direction == 1
