import hashlib
import json
from pathlib import Path


REQUIRED_IMAGES = {
    "img.player.idle",
    "img.player.idle.blink",
    "img.player.run",
    "img.player.run.2",
    "img.player.run.3",
    "img.player.air",
    "img.player.fire",
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
    for asset_id in ("img.bg.pobocka", "img.bg.sklad", "img.bg.kancelar"):
        assert entries[asset_id]["generated"] is False
        assert entries[asset_id]["source"] == "imagegen"
    player_entries = [entry for asset_id, entry in entries.items() if asset_id.startswith("img.player.")]
    assert len(player_entries) == 8
    assert {entry["path"] for entry in player_entries} == {"images/alzak_atlas.png"}
    for entry in player_entries:
        assert entry["generated"] is False
        assert entry["source"] == "imagegen"
        assert len(entry["rect"]) == 4
