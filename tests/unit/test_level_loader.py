import json

import pytest

from alzak.data.loader import load_all_levels, load_level
from alzak.data.schema import LevelDataError


ASSETS = {
    "img.bg.test",
    "img.platform.test",
    "img.enemy.walk",
    "img.exit.inactive",
    "img.exit.active",
}


def valid_level(order=1, level_id="test"):
    return {
        "schema_version": 1,
        "id": level_id,
        "display_name": "Test",
        "order": order,
        "background_asset_id": "img.bg.test",
        "player_start": {"x": 100, "y": 784},
        "platforms": [
            {"x": 0, "y": 880, "w": 1920, "h": 200, "asset_id": "img.platform.test"}
        ],
        "pit": {"x": 700, "w": 200, "kill_y": 1080},
        "enemy": {
            "x": 1100,
            "y": 808,
            "patrol_min_x": 1000,
            "patrol_max_x": 1500,
            "asset_id": "img.enemy.walk",
        },
        "exit": {
            "x": 1700,
            "y": 720,
            "w": 120,
            "h": 160,
            "asset_id_inactive": "img.exit.inactive",
            "asset_id_active": "img.exit.active",
        },
    }


def write(path, data) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


@pytest.mark.parametrize(
    ("mutation", "field"),
    [
        (lambda d: d.pop("pit"), "pit"),
        (lambda d: d.update(order="one"), "order"),
        (lambda d: d["platforms"][0].update(h=12), "platforms[0].h"),
        (lambda d: d["player_start"].update(x=750), "player_start.x"),
        (lambda d: d["enemy"].update(patrol_max_x=2000), "enemy.patrol_min_x"),
        (lambda d: d.update(background_asset_id="img.unknown"), "asset_id"),
    ],
)
def test_invalid_level_reports_field(tmp_path, mutation, field) -> None:
    data = valid_level()
    mutation(data)
    path = tmp_path / "bad.json"
    write(path, data)
    with pytest.raises(LevelDataError) as error:
        load_level(path, ASSETS)
    assert field in error.value.field


def test_duplicate_order_is_rejected_across_levels(tmp_path) -> None:
    for index, level_id in enumerate(("one", "two", "three")):
        write(tmp_path / f"{index}.json", valid_level(order=1, level_id=level_id))
    with pytest.raises(LevelDataError, match="pořadí"):
        load_all_levels(tmp_path, ASSETS)
