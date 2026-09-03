from __future__ import annotations

from dataclasses import dataclass

from alzak import config


@dataclass(slots=True)
class FixedStepClock:
    step: float = config.SIM["dt"]
    max_frame_time: float = config.SIM["max_frame_time"]
    accumulator: float = 0.0

    def consume(self, frame_time: float) -> int:
        self.accumulator += min(max(frame_time, 0.0), self.max_frame_time)
        steps = int((self.accumulator + 1e-12) / self.step)
        self.accumulator -= steps * self.step
        return steps

    def reset(self) -> None:
        self.accumulator = 0.0
