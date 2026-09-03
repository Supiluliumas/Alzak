from alzak.screens.machine import ScreenMachine, ScreenState


def test_simulation_only_runs_in_play() -> None:
    machine = ScreenMachine()
    assert not machine.simulation_active
    machine.change(ScreenState.PLAY)
    assert machine.simulation_active
    machine.change(ScreenState.PAUSE)
    assert not machine.simulation_active
