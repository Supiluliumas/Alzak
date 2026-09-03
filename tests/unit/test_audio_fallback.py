import pygame

from alzak.audio.mixer import AudioMixer
from alzak.assets.registry import NoOpSound


def test_audio_initialization_failure_is_noop(monkeypatch) -> None:
    pygame.mixer.quit()
    monkeypatch.setattr(pygame.mixer, "init", lambda **kwargs: (_ for _ in ()).throw(pygame.error("no audio")))
    mixer = AudioMixer()
    assert not mixer.available
    assert isinstance(mixer.sound("sfx.jump"), NoOpSound)
