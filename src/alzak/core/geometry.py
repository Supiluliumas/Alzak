from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RectF:
    x: float
    y: float
    w: float
    h: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def centerx(self) -> float:
        return self.x + self.w / 2.0

    @property
    def centery(self) -> float:
        return self.y + self.h / 2.0

    def intersects(self, other: "RectF") -> bool:
        return (
            self.left < other.right
            and self.right > other.left
            and self.top < other.bottom
            and self.bottom > other.top
        )

    def copy(self) -> "RectF":
        return RectF(self.x, self.y, self.w, self.h)
