from alzak.audio.mixer import AudioMixer
from alzak.sim.events import SimEvent


class FakeChannel:
    def __init__(self) -> None:
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


class FakeSound:
    def __init__(self) -> None:
        self.plays = []
        self.channel = FakeChannel()

    def play(self, **kwargs):
        self.plays.append(kwargs)
        return self.channel


def test_laser_and_movement_loops_end_on_events() -> None:
    mixer = AudioMixer()
    mixer.available = True
    sounds = {name: FakeSound() for name in ("sfx.move", "sfx.laser.start", "sfx.laser.loop", "sfx.laser.end")}
    mixer.sound = lambda asset_id: sounds[asset_id]
    mixer.update_movement(True)
    assert sounds["sfx.move"].plays == [{"loops": -1}]
    move_channel = mixer._move_channel
    mixer.update_movement(False)
    assert move_channel.stopped
    mixer.handle_events([SimEvent.LASER_STARTED])
    laser_channel = mixer._laser_channel
    mixer.handle_events([SimEvent.LASER_OVERHEATED])
    assert laser_channel.stopped
    assert sounds["sfx.laser.end"].plays
