from alzak.core.clock import FixedStepClock


def test_accumulator_is_stable_across_variable_frames() -> None:
    clock = FixedStepClock(step=1.0 / 120.0)
    steps = sum(clock.consume(dt) for dt in (1 / 30, 1 / 60, 1 / 60, 1 / 30))
    assert steps == 12
    assert abs(clock.accumulator) < 1e-9


def test_accumulator_clamps_long_frames_and_resets() -> None:
    clock = FixedStepClock(step=0.01, max_frame_time=0.25)
    assert clock.consume(2.0) == 25
    clock.consume(0.005)
    clock.reset()
    assert clock.accumulator == 0.0
