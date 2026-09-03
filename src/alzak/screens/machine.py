from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class ScreenState(Enum):
    TITLE = auto()
    PLAY = auto()
    PAUSE = auto()
    TRANSITION = auto()
    GAMEOVER = auto()
    FINISH = auto()
    ERROR = auto()


@dataclass(slots=True)
class ScreenMachine:
    state: ScreenState = ScreenState.TITLE

    def change(self, new_state: ScreenState) -> None:
        self.state = new_state

    @property
    def simulation_active(self) -> bool:
        return self.state is ScreenState.PLAY
