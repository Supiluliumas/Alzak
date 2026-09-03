import hashlib
import json
from pathlib import Path


REQUIRED_IMAGES = {
    "img.player.idle",
    "img.player.run",
    "img.player.air",
    "img.player.hurt",
    "img.enemy.walk",
    "img.enemy.hit",
    "img.platform.pobocka",
    "img.platform.sklad",
    "img.platform.kancelar",
    "img.pit",
    "img.exit.inactive",
    "img.exit.active",
    "img.bg.pobocka",
    "img.bg.sklad",
    "img.bg.kancelar",
    "img.hud.energy_full",
    "img.hud.energy_empty",
    "img.hud.heat_frame",
    "img.hud.heat_fill",
}


def test_manifest_is_complete_and_checksums_match() -> None:
    root = Path("assets")
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    assert REQUIRED_IMAGES <= entries.keys()
    assert len([key for key in entries if key.startswith("sfx.")]) == 5
    assert "music.loop" in entries
    for entry in entries.values():
        path = root / entry["path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
