from __future__ import annotations

from dataclasses import dataclass

from alzak import config


@dataclass(slots=True)
class Transition:
    elapsed: float = 0.0
    pending_pause: bool = False

    @property
    def duration(self) -> float:
        return config.LEVEL["transition_fade_time"] * 2.0

    @property
    def complete(self) -> bool:
        return self.elapsed >= self.duration

    @property
    def alpha(self) -> int:
        half = config.LEVEL["transition_fade_time"]
        phase = self.elapsed / half if self.elapsed <= half else (self.duration - self.elapsed) / half
        return round(max(0.0, min(1.0, phase)) * 255)

    def update(self, dt: float, escape_pressed: bool = False) -> None:
        if escape_pressed:
            self.pending_pause = True
        self.elapsed = min(self.duration, self.elapsed + dt)
