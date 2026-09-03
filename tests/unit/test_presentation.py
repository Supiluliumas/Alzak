import pytest
import pygame

from alzak.render.presentation import Presentation, compute_viewport


@pytest.mark.parametrize(
    ("window", "scale", "size", "offset"),
    [
        ((1920, 1080), 1.0, (1920, 1080), (0, 0)),
        ((1280, 720), 2 / 3, (1280, 720), (0, 0)),
        ((3840, 2160), 2.0, (3840, 2160), (0, 0)),
        ((2560, 1080), 1.0, (1920, 1080), (320, 0)),
        ((1600, 1200), 5 / 6, (1600, 900), (0, 150)),
    ],
)
def test_compute_viewport(window, scale, size, offset) -> None:
    actual_scale, actual_size, actual_offset = compute_viewport(*window)
    assert actual_scale == pytest.approx(scale)
    assert actual_size == size
    assert actual_offset == offset


def test_fullscreen_toggle_preserves_logical_surface(monkeypatch) -> None:
    windows = []

    def set_mode(size, flags=0):
        surface = pygame.Surface((1920, 1080) if size == (0, 0) else size)
        windows.append((size, flags))
        return surface

    monkeypatch.setattr(pygame.display, "set_mode", set_mode)
    logical = pygame.Surface((1920, 1080))
    presentation = Presentation(pygame.Surface((1280, 720)), logical)
    presentation.toggle_fullscreen()
    presentation.toggle_fullscreen()
    assert presentation.logical_surface is logical
    assert len(windows) == 2
