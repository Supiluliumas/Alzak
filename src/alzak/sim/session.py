from __future__ import annotations

from dataclasses import dataclass

from alzak.data.loader import LevelData
from alzak.sim.level import LevelState


@dataclass(slots=True)
class Session:
    levels: tuple[LevelData, ...]
    level_index: int
    current: LevelState
    finished: bool = False

    @classmethod
    def start(cls, levels: tuple[LevelData, ...]) -> "Session":
        if len(levels) != 3:
            raise ValueError("Demo vyžaduje právě tři prostředí")
        return cls(levels, 0, LevelState.from_data(levels[0]))

    @property
    def level_ids(self) -> tuple[str, ...]:
        return tuple(level.id for level in self.levels)

    def restart_level(self) -> None:
        self.current = LevelState.from_data(self.levels[self.level_index])

    def advance(self) -> bool:
        if not self.current.completed:
            return False
        if self.level_index == len(self.levels) - 1:
            self.finished = True
            return True
        self.level_index += 1
        self.current = LevelState.from_data(self.levels[self.level_index])
        return True

    def restart_demo(self) -> None:
        self.level_index = 0
        self.finished = False
        self.current = LevelState.from_data(self.levels[0])
