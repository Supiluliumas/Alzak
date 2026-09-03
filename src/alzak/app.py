from __future__ import annotations

import os

import pygame

from alzak import config
from alzak.assets.registry import AssetRegistry
from alzak.audio.mixer import AudioMixer
from alzak.core.clock import FixedStepClock
from alzak.core.input import InputSnapshot, from_pygame
from alzak.data.loader import load_all_levels
from alzak.data.schema import LevelDataError
from alzak.paths import levels_root
from alzak.render.hud import draw_hud
from alzak.render.presentation import Presentation
from alzak.render.world import draw_world
from alzak.screens.error_screen import run_error_screen
from alzak.screens.finish import OPTIONS as FINISH_OPTIONS, draw_finish
from alzak.screens.gameover import OPTIONS as GAMEOVER_OPTIONS, draw_gameover
from alzak.screens.machine import ScreenMachine, ScreenState
from alzak.screens.pause import OPTIONS as PAUSE_OPTIONS, draw_pause
from alzak.screens.title import OPTIONS as TITLE_OPTIONS, draw_title
from alzak.screens.transition import Transition
from alzak.sim.session import Session


class GameApp:
    def __init__(self, registry: AssetRegistry, levels: tuple) -> None:
        self.registry = registry
        self.levels = levels
        self.machine = ScreenMachine()
        self.session: Session | None = None
        self.selections = {
            ScreenState.TITLE: 0,
            ScreenState.PAUSE: 0,
            ScreenState.GAMEOVER: 0,
            ScreenState.FINISH: 0,
        }
        self.transition: Transition | None = None
        self.transition_action = ""
        self.audio = AudioMixer(registry)
        self.audio.start_music()
        self.running = True

    def _set_state(self, state: ScreenState) -> None:
        if self.machine.state is ScreenState.PLAY and state is not ScreenState.PLAY:
            self.audio.stop_all_loops()
        self.machine.change(state)
        self.audio.set_paused(state is ScreenState.PAUSE)

    def _begin_transition(self, action: str) -> None:
        self.transition = Transition()
        self.transition_action = action
        self._set_state(ScreenState.TRANSITION)

    def _apply_transition_action(self) -> None:
        if self.transition_action == "start":
            self.session = Session.start(self.levels)
        elif self.transition_action == "next" and self.session is not None:
            self.session.advance()
        elif self.transition_action == "restart_demo" and self.session is not None:
            self.session.restart_demo()

    def _options(self) -> tuple[str, ...]:
        return {
            ScreenState.TITLE: TITLE_OPTIONS,
            ScreenState.PAUSE: PAUSE_OPTIONS,
            ScreenState.GAMEOVER: GAMEOVER_OPTIONS,
            ScreenState.FINISH: FINISH_OPTIONS,
        }.get(self.machine.state, ())

    def handle_key(self, key: int) -> None:
        state = self.machine.state
        if state is ScreenState.PLAY:
            if key == pygame.K_ESCAPE:
                self._set_state(ScreenState.PAUSE)
            elif key == pygame.K_r and self.session is not None:
                self.session.restart_level()
            return
        if state is ScreenState.TRANSITION:
            if key == pygame.K_ESCAPE and self.transition is not None:
                self.transition.pending_pause = True
            return
        if state is ScreenState.PAUSE and key == pygame.K_ESCAPE:
            self._set_state(ScreenState.PLAY)
            return
        options = self._options()
        if not options:
            return
        selected = self.selections[state]
        if key == pygame.K_UP:
            self.selections[state] = (selected - 1) % len(options)
        elif key == pygame.K_DOWN:
            self.selections[state] = (selected + 1) % len(options)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.activate_menu()

    def activate_menu(self) -> None:
        state = self.machine.state
        selected = self.selections.get(state, 0)
        if state is ScreenState.TITLE:
            if selected == 0:
                self._begin_transition("start")
            else:
                self.running = False
        elif state is ScreenState.PAUSE:
            if selected == 0:
                self._set_state(ScreenState.PLAY)
            elif selected == 1 and self.session is not None:
                self.session.restart_level()
                self._set_state(ScreenState.PLAY)
            else:
                self.session = None
                self._set_state(ScreenState.TITLE)
        elif state is ScreenState.GAMEOVER:
            if selected == 0 and self.session is not None:
                self.session.restart_level()
                self._set_state(ScreenState.PLAY)
            else:
                self.session = None
                self._set_state(ScreenState.TITLE)
        elif state is ScreenState.FINISH:
            if selected == 0:
                self._begin_transition("restart_demo")
            else:
                self.running = False

    def update(self, inputs: InputSnapshot, dt: float) -> None:
        if self.machine.state is ScreenState.TRANSITION and self.transition is not None:
            previous = self.transition.elapsed
            self.transition.update(dt)
            half = config.LEVEL["transition_fade_time"]
            if previous < half <= self.transition.elapsed and not self.transition.switched:
                self._apply_transition_action()
                self.transition.switched = True
            if self.transition.complete:
                pending_pause = self.transition.pending_pause
                target = ScreenState.FINISH if self.session is not None and self.session.finished else ScreenState.PLAY
                self._set_state(ScreenState.PAUSE if pending_pause and target is ScreenState.PLAY else target)
            return
        if self.machine.state is not ScreenState.PLAY or self.session is None:
            return
        events = self.session.current.step(inputs, dt)
        self.audio.handle_events(events)
        player = self.session.current.player
        self.audio.update_movement(player.on_ground and abs(player.vx) > 0.0)
        if self.session.current.failed:
            self._set_state(ScreenState.GAMEOVER)
        elif self.session.current.completed:
            self._begin_transition("next")

    def draw(self, surface: pygame.Surface) -> None:
        state = self.machine.state
        if state is ScreenState.TITLE:
            draw_title(surface, self.registry, self.selections[state])
            return
        if state is ScreenState.FINISH:
            draw_finish(surface, self.selections[state])
            return
        if self.session is not None:
            draw_world(surface, self.session.current, self.registry)
            draw_hud(surface, self.session.current, self.session.level_index, len(self.session.levels), self.registry)
        if state is ScreenState.PAUSE:
            draw_pause(surface, self.selections[state])
        elif state is ScreenState.GAMEOVER:
            draw_gameover(surface, self.selections[state])
        elif state is ScreenState.TRANSITION and self.transition is not None:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.transition.alpha))
            surface.blit(overlay, (0, 0))


def run() -> int:
    pygame.init()
    pygame.display.set_caption(config.DISPLAY["title"])
    presentation = Presentation.create()
    registry = AssetRegistry()
    levels = load_all_levels(levels_root(), registry.ids)
    game = GameApp(registry, levels)
    game.draw(presentation.logical_surface)
    presentation.present()
    if os.environ.get("ALZAK_SMOKE_EXIT") == "1":
        pygame.quit()
        return 0
    clock = pygame.time.Clock()
    fixed = FixedStepClock()
    while game.running:
        jump_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    presentation.toggle_fullscreen()
                else:
                    game.handle_key(event.key)
                    jump_pressed = jump_pressed or (event.key == pygame.K_SPACE and game.machine.state is ScreenState.PLAY)
        frame_dt = clock.tick(config.DISPLAY["target_fps"]) / 1000.0
        if game.machine.simulation_active:
            inputs = from_pygame(pygame.key.get_pressed(), jump_pressed)
            for _ in range(fixed.consume(frame_dt)):
                game.update(inputs, config.SIM["dt"])
                inputs = InputSnapshot(inputs.left, inputs.right, False, inputs.jump_held, inputs.fire_held)
        else:
            fixed.reset()
            game.update(InputSnapshot(), frame_dt)
        game.draw(presentation.logical_surface)
        presentation.present()
    game.audio.stop_all_loops()
    pygame.quit()
    return 0


def main() -> int:
    try:
        return run()
    except LevelDataError as error:
        return run_error_screen(error)
