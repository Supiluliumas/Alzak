from pathlib import Path

import pygame

from alzak import config
from alzak.app import GameApp
from alzak.assets.registry import AssetRegistry
from alzak.core.input import InputSnapshot
from alzak.data.loader import load_all_levels
from alzak.screens.machine import ScreenState


class SilentAudio:
    def start_music(self): pass
    def stop_all_loops(self): pass
    def set_paused(self, paused): pass
    def handle_events(self, events): pass
    def update_movement(self, moving): pass


def game() -> GameApp:
    registry = AssetRegistry()
    instance = GameApp(registry, load_all_levels(Path("levels"), registry.ids))
    instance.audio = SilentAudio()
    return instance


def enter_play(instance: GameApp) -> None:
    instance.handle_key(pygame.K_RETURN)
    instance.update(InputSnapshot(), config.LEVEL["transition_fade_time"] * 2)
    assert instance.machine.state is ScreenState.PLAY


def test_pause_and_gameover_quit_return_to_title() -> None:
    instance = game()
    enter_play(instance)
    instance.handle_key(pygame.K_ESCAPE)
    instance.selections[ScreenState.PAUSE] = 2
    instance.activate_menu()
    assert instance.machine.state is ScreenState.TITLE and instance.running
    enter_play(instance)
    instance._set_state(ScreenState.GAMEOVER)
    instance.selections[ScreenState.GAMEOVER] = 1
    instance.activate_menu()
    assert instance.machine.state is ScreenState.TITLE and instance.running


def test_only_title_and_finish_quit_application() -> None:
    instance = game()
    instance.selections[ScreenState.TITLE] = 1
    instance.activate_menu()
    assert not instance.running
    instance = game()
    instance._set_state(ScreenState.FINISH)
    instance.selections[ScreenState.FINISH] = 1
    instance.activate_menu()
    assert not instance.running
