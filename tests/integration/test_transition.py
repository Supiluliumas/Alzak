from alzak import config
from alzak.core.clock import FixedStepClock
from alzak.screens.transition import Transition


def test_transition_completes_and_defers_escape() -> None:
    transition = Transition()
    while not transition.complete:
        transition.update(config.SIM["dt"], escape_pressed=transition.elapsed == 0)
        assert 0 <= transition.alpha <= 255
    assert transition.pending_pause
    clock = FixedStepClock()
    clock.consume(0.2)
    clock.reset()
    assert clock.accumulator == 0
