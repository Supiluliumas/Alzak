import json

import pygame
import pytest

from alzak.assets.registry import AssetRegistry, AssetRegistryError


def _manifest(root, entries) -> None:
    root.mkdir()
    (root / "manifest.json").write_text(
        json.dumps({"schema_version": 1, "entries": entries}), encoding="utf-8"
    )


def test_unknown_id_is_hard_error(tmp_path) -> None:
    _manifest(tmp_path / "assets", {})
    registry = AssetRegistry(tmp_path / "assets")
    with pytest.raises(AssetRegistryError, match="Neznámé asset ID"):
        registry.path("img.missing")


def test_missing_development_file_is_visible_and_cached(tmp_path) -> None:
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    root = tmp_path / "assets"
    _manifest(root, {"img.test": {"path": "missing.png"}})
    registry = AssetRegistry(root, frozen=False)
    first = registry.image("img.test")
    assert first is registry.image("img.test")
    assert first.get_at((2, 2))[:3] != (0, 0, 0)


def test_missing_frozen_file_is_hard_error(tmp_path) -> None:
    root = tmp_path / "assets"
    _manifest(root, {"img.test": {"path": "missing.png"}})
    with pytest.raises(AssetRegistryError, match="Chybí asset v buildu"):
        AssetRegistry(root, frozen=True).image("img.test")
