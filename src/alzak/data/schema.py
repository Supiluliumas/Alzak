from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LevelDataError(ValueError):
    file: str
    field: str
    reason: str

    def __str__(self) -> str:
        return (
            "Chyba dat prostředí\n"
            f"Soubor: {self.file}\n"
            f"Pole: {self.field}\n"
            f"Důvod: {self.reason}"
        )


REQUIRED_ROOT_FIELDS = {
    "schema_version",
    "id",
    "display_name",
    "order",
    "background_asset_id",
    "player_start",
    "platforms",
    "pit",
    "enemy",
    "exit",
}
