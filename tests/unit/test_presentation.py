import pytest

from alzak.render.presentation import compute_viewport


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
