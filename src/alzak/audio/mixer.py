from __future__ import annotations

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry, NoOpSound
from alzak.sim.events import SimEvent


class AudioMixer:
    def __init__(self, registry: AssetRegistry | None = None) -> None:
        self.registry = registry
        self.available = False
        self._sounds: dict[str, pygame.mixer.Sound | NoOpSound] = {}
        self._move_channel: pygame.mixer.Channel | None = None
        self._laser_channel: pygame.mixer.Channel | None = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=config.AUDIO["frequency"],
                    size=-16,
                    channels=config.AUDIO["channels"],
                    buffer=config.AUDIO["buffer"],
                )
            self.available = True
        except pygame.error:
            self.available = False

    def sound(self, asset_id: str) -> pygame.mixer.Sound | NoOpSound:
        if not self.available or self.registry is None:
            return NoOpSound()
        if asset_id not in self._sounds:
            self._sounds[asset_id] = self.registry.sound(asset_id)
            self._sounds[asset_id].set_volume(config.AUDIO["sfx_volume"])
        return self._sounds[asset_id]

    def start_music(self) -> None:
        if not self.available or self.registry is None:
            return
        try:
            pygame.mixer.music.load(str(self.registry.path("music.loop")))
            pygame.mixer.music.set_volume(config.AUDIO["music_volume"])
            pygame.mixer.music.play(-1)
        except pygame.error:
            self.available = False

    def set_paused(self, paused: bool) -> None:
        if self.available:
            volume = config.AUDIO["music_volume_paused"] if paused else config.AUDIO["music_volume"]
            pygame.mixer.music.set_volume(volume)

    def stop_all_loops(self) -> None:
        if self._move_channel is not None:
            self._move_channel.stop()
            self._move_channel = None
        if self._laser_channel is not None:
            self._laser_channel.stop()
            self._laser_channel = None

    def update_movement(self, moving_on_ground: bool) -> None:
        if not self.available:
            return
        if moving_on_ground and self._move_channel is None:
            channel = self.sound("sfx.move").play(loops=-1)
            self._move_channel = channel
        elif not moving_on_ground and self._move_channel is not None:
            self._move_channel.stop()
            self._move_channel = None

    def handle_events(self, events: list[SimEvent]) -> None:
        for event in events:
            if event is SimEvent.JUMPED:
                self.sound("sfx.jump").play()
            elif event is SimEvent.LASER_STARTED:
                self.sound("sfx.laser.start").play()
                channel = self.sound("sfx.laser.loop").play(loops=-1)
                self._laser_channel = channel
            elif event in (SimEvent.LASER_STOPPED, SimEvent.LASER_OVERHEATED):
                if self._laser_channel is not None:
                    self._laser_channel.stop()
                    self._laser_channel = None
                self.sound("sfx.laser.end").play()
