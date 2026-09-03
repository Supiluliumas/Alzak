import ast
from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.data.loader import load_all_levels
from alzak.render.hud import hud_snapshot
from alzak.sim.level import LevelState


def test_hud_snapshot_has_energy_heat_name_and_progress() -> None:
    registry = AssetRegistry()
    data = load_all_levels(Path("levels"), registry.ids)[1]
    state = LevelState.from_data(data)
    state.player.energy = 2
    state.laser.heat = 0.75
    model = hud_snapshot(state, 1, 3)
    assert (model.energy, model.heat, model.level_name, model.progress) == (2, 0.75, "Logistický sklad", "2/3")


def test_hud_module_uses_central_config() -> None:
    tree = ast.parse(Path("src/alzak/render/hud.py").read_text(encoding="utf-8"))
    numeric = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, (int, float))]
    assert set(numeric) <= {0, 1}
