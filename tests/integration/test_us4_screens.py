from pathlib import Path

import pygame

from alzak import config
from alzak.app import GameApp
from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_all_levels
from alzak.screens.machine import ScreenState


def test_keyboard_only_screen_flow_and_rendering() -> None:
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    registry = AssetRegistry()
    game = GameApp(registry, load_all_levels(Path("levels"), registry.ids))
    surface = pygame.Surface(config.DISPLAY["logical_size"])
    game.draw(surface)
    game.handle_key(pygame.K_RETURN)
    game.update(InputSnapshot(), config.LEVEL["transition_fade_time"] * 2)
    assert game.machine.state is ScreenState.PLAY
    game.handle_key(pygame.K_ESCAPE)
    assert game.machine.state is ScreenState.PAUSE
    game.handle_key(pygame.K_ESCAPE)
    assert game.machine.state is ScreenState.PLAY
    game.session.current.enemy.damage(game.session.current.enemy.hp)
    game.session.current.player.x = game.session.current.exit.rect.x
    game.session.current.player.y = game.session.current.exit.rect.y
    game.update(InputSnapshot(), config.SIM["dt"])
    assert game.machine.state is ScreenState.TRANSITION
