from alzak.core.clock import FixedStepClock


def simulate(frame_dt: float, seconds: float) -> int:
    clock = FixedStepClock()
    steps = 0
    for _ in range(round(seconds / frame_dt)):
        steps += clock.consume(frame_dt)
    return steps


def test_fixed_step_count_matches_at_30_and_60_fps() -> None:
    assert simulate(1 / 30, 3.0) == simulate(1 / 60, 3.0) == 360
