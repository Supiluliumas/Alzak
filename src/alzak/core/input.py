from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InputSnapshot:
    left: bool = False
    right: bool = False
    jump_pressed: bool = False
    jump_held: bool = False
    fire_held: bool = False


def from_pygame(pressed: object, jump_pressed: bool = False) -> InputSnapshot:
    import pygame

    return InputSnapshot(
        left=bool(pressed[pygame.K_LEFT]),
        right=bool(pressed[pygame.K_RIGHT]),
        jump_pressed=jump_pressed,
        jump_held=bool(pressed[pygame.K_SPACE]),
        fire_held=bool(pressed[pygame.K_x]),
    )
