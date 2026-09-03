import pygame

from alzak.render.text import get_font


def test_builtin_font_renders_czech_glyphs() -> None:
    pygame.font.init()
    font = get_font(36)
    for character in "ěščřžýáíéúůďťňĚŠČŘŽ":
        surface = font.render(character, True, (255, 255, 255))
        assert surface.get_width() > 0
        assert pygame.mask.from_surface(surface).count() > 0
