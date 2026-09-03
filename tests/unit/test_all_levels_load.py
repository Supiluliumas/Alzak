from pathlib import Path

from alzak.assets.registry import AssetRegistry
from alzak.data.loader import load_all_levels


def test_all_three_levels_use_the_shared_loader() -> None:
    registry = AssetRegistry()
    levels = load_all_levels(Path("levels"), registry.ids)
    assert [level.order for level in levels] == [1, 2, 3]
    assert [level.id for level in levels] == ["pobocka", "sklad", "kancelar"]
