from __future__ import annotations

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry, NoOpSound


class AudioMixer:
    def __init__(self, registry: AssetRegistry | None = None) -> None:
        self.registry = registry
        self.available = False
        self._sounds: dict[str, pygame.mixer.Sound | NoOpSound] = {}
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
        for asset_id in ("sfx.move", "sfx.laser.loop"):
            if asset_id in self._sounds:
                self._sounds[asset_id].stop()
