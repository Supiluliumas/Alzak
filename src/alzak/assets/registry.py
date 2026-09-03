from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pygame

from alzak.paths import assets_root


class AssetRegistryError(RuntimeError):
    pass


class NoOpSound:
    def play(self, *args: object, **kwargs: object) -> None:
        return None

    def stop(self) -> None:
        return None

    def set_volume(self, volume: float) -> None:
        return None


class AssetRegistry:
    def __init__(self, root: Path | None = None, *, frozen: bool | None = None) -> None:
        self.root = Path(root) if root is not None else assets_root()
        self.frozen = getattr(sys, "frozen", False) if frozen is None else frozen
        manifest_path = self.root / "manifest.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AssetRegistryError(f"Nelze načíst manifest assetů: {manifest_path}: {exc}") from exc
        if manifest.get("schema_version") != 1 or not isinstance(manifest.get("entries"), dict):
            raise AssetRegistryError("Neplatný formát manifestu assetů")
        self.entries: dict[str, dict[str, Any]] = manifest["entries"]
        self._cache: dict[str, object] = {}

    @property
    def ids(self) -> set[str]:
        return set(self.entries)

    def path(self, asset_id: str) -> Path:
        try:
            relative = self.entries[asset_id]["path"]
        except KeyError as exc:
            raise AssetRegistryError(f"Neznámé asset ID: {asset_id}") from exc
        return self.root / relative

    def image(self, asset_id: str) -> pygame.Surface:
        cached = self._cache.get(asset_id)
        if isinstance(cached, pygame.Surface):
            return cached
        path = self.path(asset_id)
        if path.exists():
            image = pygame.image.load(str(path)).convert_alpha()
            rect = self.entries[asset_id].get("rect")
            if rect is not None:
                image = image.subsurface(pygame.Rect(rect)).copy()
        elif self.frozen:
            raise AssetRegistryError(f"Chybí asset v buildu: {asset_id} ({path})")
        else:
            print(f"Varování: chybí asset {asset_id}: {path}", file=sys.stderr)
            image = pygame.Surface((64, 64), pygame.SRCALPHA)
            image.fill((255, 0, 180, 255))
            pygame.draw.line(image, (20, 20, 20), (0, 0), (63, 63), 5)
            pygame.draw.line(image, (20, 20, 20), (63, 0), (0, 63), 5)
        self._cache[asset_id] = image
        return image

    def sound(self, asset_id: str) -> pygame.mixer.Sound | NoOpSound:
        cached = self._cache.get(asset_id)
        if cached is not None and not isinstance(cached, pygame.Surface):
            return cached  # type: ignore[return-value]
        path = self.path(asset_id)
        if not pygame.mixer.get_init() or not path.exists():
            sound: pygame.mixer.Sound | NoOpSound = NoOpSound()
        else:
            sound = pygame.mixer.Sound(str(path))
        self._cache[asset_id] = sound
        return sound
