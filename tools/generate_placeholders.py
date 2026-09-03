#!/usr/bin/env python3
"""Deterministically generate all committed placeholder PNG and WAV assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import tempfile
import wave
import zlib
from array import array
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SAMPLE_RATE = 22050
Color = tuple[int, int, int, int]


class Canvas:
    def __init__(self, width: int, height: int, color: Color = (0, 0, 0, 0)) -> None:
        self.width = width
        self.height = height
        self.pixels = bytearray(color * (width * height))

    def set(self, x: int, y: int, color: Color) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            index = (y * self.width + x) * 4
            alpha = color[3]
            if alpha == 255:
                self.pixels[index : index + 4] = bytes(color)
            elif alpha:
                old = self.pixels[index : index + 4]
                inv = 255 - alpha
                self.pixels[index : index + 4] = bytes(
                    ((color[i] * alpha + old[i] * inv) // 255 for i in range(3))
                ) + bytes((min(255, alpha + old[3] * inv // 255),))

    def fill(self, color: Color) -> None:
        self.pixels[:] = bytes(color) * (self.width * self.height)

    def rect(self, x: int, y: int, w: int, h: int, color: Color) -> None:
        left, top = max(0, x), max(0, y)
        right, bottom = min(self.width, x + w), min(self.height, y + h)
        row = bytes(color) * max(0, right - left)
        for py in range(top, bottom):
            start = (py * self.width + left) * 4
            self.pixels[start : start + len(row)] = row

    def circle(self, cx: int, cy: int, radius: int, color: Color) -> None:
        radius_sq = radius * radius
        for y in range(cy - radius, cy + radius + 1):
            dy_sq = (y - cy) ** 2
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx) ** 2 + dy_sq <= radius_sq:
                    self.set(x, y, color)

    def ellipse(self, cx: int, cy: int, rx: int, ry: int, color: Color) -> None:
        if rx <= 0 or ry <= 0:
            return
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x - cx) ** 2) * ry * ry + ((y - cy) ** 2) * rx * rx <= rx * rx * ry * ry:
                    self.set(x, y, color)

    def line(self, x0: int, y0: int, x1: int, y1: int, color: Color, width: int = 1) -> None:
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        error = dx + dy
        while True:
            self.circle(x0, y0, max(0, width // 2), color)
            if x0 == x1 and y0 == y1:
                return
            double = 2 * error
            if double >= dy:
                error += dy
                x0 += sx
            if double <= dx:
                error += dx
                y0 += sy


def png_bytes(canvas: Canvas) -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)

    raw = bytearray()
    stride = canvas.width * 4
    for y in range(canvas.height):
        raw.append(0)
        raw.extend(canvas.pixels[y * stride : (y + 1) * stride])
    header = struct.pack(">IIBBBBB", canvas.width, canvas.height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")


def hero(pose: str) -> Canvas:
    c = Canvas(64, 96)
    outline, green, light = (30, 66, 25, 255), (92, 190, 45, 255), (152, 235, 78, 255)
    silver, dark = (205, 221, 226, 255), (75, 98, 105, 255)
    leg_shift = 0 if pose in {"idle", "hurt"} else 4
    c.ellipse(32, 30, 25, 28, outline)
    c.ellipse(32, 30, 22, 25, green)
    c.circle(32, 4, 6, outline)
    c.circle(32, 4, 4, light)
    c.ellipse(23, 27, 8, 10, (245, 250, 245, 255))
    c.ellipse(42, 27, 7, 10, (245, 250, 245, 255))
    c.circle(26, 29, 3, (15, 24, 20, 255))
    c.circle(44, 29, 3, (15, 24, 20, 255))
    if pose == "hurt":
        c.line(17, 21, 27, 31, dark, 2)
        c.line(27, 21, 17, 31, dark, 2)
        c.line(37, 21, 47, 31, dark, 2)
        c.line(47, 21, 37, 31, dark, 2)
        c.ellipse(32, 42, 7, 4, (65, 35, 35, 255))
    else:
        c.line(24, 42, 30, 45, dark, 2)
        c.line(30, 45, 40, 41, dark, 2)
    c.ellipse(32, 63, 24, 25, outline)
    c.rect(11, 52, 42, 24, silver)
    c.line(14, 55, 49, 55, (245, 250, 250, 255), 2)
    c.rect(15, 73, 12, 14, green)
    c.rect(38, 73, 12, 14, green)
    c.ellipse(20 - leg_shift, 88, 13, 6, dark)
    c.ellipse(45 + leg_shift, 88, 13, 6, dark)
    arm_y = 58 if pose != "air" else 48
    c.line(12, 57, 3, arm_y + (8 if pose == "run" else 0), green, 7)
    c.line(51, 57, 61, arm_y - (7 if pose == "air" else 0), green, 7)
    if pose == "run":
        c.line(14, 78, 7, 89, green, 7)
        c.line(45, 78, 58, 84, green, 7)
    return c


def enemy(hit: bool) -> Canvas:
    c = Canvas(72, 72)
    body = (255, 112, 72, 255) if hit else (116, 79, 190, 255)
    outline = (35, 28, 55, 255)
    c.ellipse(36, 37, 29, 25, outline)
    c.ellipse(36, 37, 25, 21, body)
    c.rect(18, 18, 36, 17, (54, 65, 87, 255))
    c.circle(27, 27, 5, (245, 245, 220, 255))
    c.circle(46, 27, 5, (245, 245, 220, 255))
    c.circle(28, 28, 2, outline)
    c.circle(47, 28, 2, outline)
    c.rect(24, 49, 24, 6, outline)
    c.line(36, 18, 36, 7, outline, 3)
    c.circle(36, 5, 4, (255, 205, 62, 255))
    c.rect(10, 57, 19, 8, outline)
    c.rect(43, 57, 19, 8, outline)
    return c


def tile(kind: str) -> Canvas:
    palettes = {
        "pobocka": ((36, 126, 156, 255), (72, 178, 194, 255), (220, 244, 245, 255)),
        "sklad": ((104, 80, 55, 255), (181, 132, 70, 255), (238, 186, 75, 255)),
        "kancelar": ((47, 75, 101, 255), (91, 126, 151, 255), (166, 205, 221, 255)),
    }
    c = Canvas(64, 64, palettes[kind][0])
    c.rect(0, 0, 64, 10, palettes[kind][2])
    for x in range(-20, 80, 24):
        c.line(x, 10, x + 28, 64, palettes[kind][1], 5)
    return c


def pit() -> Canvas:
    c = Canvas(64, 64, (8, 11, 25, 255))
    for radius, color in ((28, (22, 11, 45, 255)), (20, (47, 18, 62, 255)), (11, (8, 5, 16, 255))):
        c.ellipse(32, 31, radius, max(5, radius // 3), color)
    return c


def exit_door(active: bool) -> Canvas:
    c = Canvas(120, 160)
    frame = (157, 239, 76, 255) if active else (90, 106, 112, 255)
    glow = (95, 220, 100, 90) if active else (32, 42, 48, 80)
    c.rect(4, 4, 112, 156, glow)
    c.rect(18, 16, 84, 144, frame)
    c.rect(29, 30, 62, 130, (20, 47, 51, 255))
    c.circle(78, 96, 6, frame)
    if active:
        for y in range(40, 145, 18):
            c.rect(33, y, 54, 7, (122, 255, 137, 190))
    return c


def hud_energy(full: bool) -> Canvas:
    c = Canvas(48, 48)
    edge = (37, 75, 40, 255)
    fill = (151, 237, 66, 255) if full else (55, 67, 71, 255)
    c.circle(24, 25, 18, edge)
    c.circle(24, 25, 14, fill)
    c.circle(24, 8, 5, edge)
    c.circle(24, 8, 3, fill)
    return c


def heat_bar(frame: bool) -> Canvas:
    c = Canvas(240, 32)
    if frame:
        c.rect(0, 0, 240, 32, (210, 228, 233, 255))
        c.rect(4, 4, 232, 24, (22, 37, 48, 210))
    else:
        for x in range(240):
            c.rect(x, 0, 1, 32, (90 + min(165, x), max(45, 220 - x // 2), 62, 255))
    return c


def background(kind: str) -> Canvas:
    palettes = {
        "pobocka": ((25, 83, 108), (68, 154, 172), (205, 239, 236, 255)),
        "sklad": ((57, 45, 38), (128, 91, 51), (230, 174, 72, 255)),
        "kancelar": ((25, 45, 69), (65, 103, 132), (158, 205, 222, 255)),
    }
    top, bottom, accent = palettes[kind]
    c = Canvas(1920, 1080)
    for y in range(1080):
        t = y / 1079
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
        c.rect(0, y, 1920, 1, color)
    if kind == "pobocka":
        c.rect(90, 110, 1740, 520, (220, 242, 239, 215))
        for x in range(150, 1800, 310):
            c.rect(x, 170, 220, 330, (91, 174, 193, 255))
            c.rect(x + 18, 188, 184, 294, (164, 222, 226, 255))
        c.rect(120, 650, 1680, 24, accent)
    elif kind == "sklad":
        for x in range(80, 1880, 290):
            c.rect(x, 160, 30, 640, accent)
            c.rect(x + 210, 160, 30, 640, accent)
            for y in range(210, 790, 145):
                c.rect(x, y, 240, 18, (211, 151, 62, 255))
                c.rect(x + 24, y - 78, 82, 72, (155, 103, 54, 255))
                c.rect(x + 120, y - 65, 88, 59, (183, 127, 63, 255))
    else:
        for x in range(80, 1880, 290):
            c.rect(x, 100, 225, 410, (97, 151, 174, 255))
            c.rect(x + 12, 112, 201, 386, (157, 211, 224, 255))
            c.line(x + 112, 112, x + 112, 498, (82, 126, 147, 255), 5)
        for x in range(160, 1800, 350):
            c.rect(x, 655, 260, 80, (141, 105, 68, 255))
            c.rect(x + 25, 735, 24, 145, (68, 61, 60, 255))
            c.rect(x + 210, 735, 24, 145, (68, 61, 60, 255))
    return c


IMAGE_SPECS: tuple[tuple[str, str, Callable[[], Canvas]], ...] = (
    ("img.player.idle", "images/player_idle.png", lambda: hero("idle")),
    ("img.player.run", "images/player_run.png", lambda: hero("run")),
    ("img.player.air", "images/player_air.png", lambda: hero("air")),
    ("img.player.hurt", "images/player_hurt.png", lambda: hero("hurt")),
    ("img.enemy.walk", "images/enemy_walk.png", lambda: enemy(False)),
    ("img.enemy.hit", "images/enemy_hit.png", lambda: enemy(True)),
    ("img.platform.pobocka", "images/platform_pobocka.png", lambda: tile("pobocka")),
    ("img.platform.sklad", "images/platform_sklad.png", lambda: tile("sklad")),
    ("img.platform.kancelar", "images/platform_kancelar.png", lambda: tile("kancelar")),
    ("img.pit", "images/pit.png", pit),
    ("img.exit.inactive", "images/exit_inactive.png", lambda: exit_door(False)),
    ("img.exit.active", "images/exit_active.png", lambda: exit_door(True)),
    ("img.bg.pobocka", "images/bg_pobocka.png", lambda: background("pobocka")),
    ("img.bg.sklad", "images/bg_sklad.png", lambda: background("sklad")),
    ("img.bg.kancelar", "images/bg_kancelar.png", lambda: background("kancelar")),
    ("img.hud.energy_full", "images/hud_energy_full.png", lambda: hud_energy(True)),
    ("img.hud.energy_empty", "images/hud_energy_empty.png", lambda: hud_energy(False)),
    ("img.hud.heat_frame", "images/hud_heat_frame.png", lambda: heat_bar(True)),
    ("img.hud.heat_fill", "images/hud_heat_fill.png", lambda: heat_bar(False)),
)


def pcm_wave(duration: float, synth: Callable[[float], float]) -> bytes:
    samples = array("h")
    count = round(duration * SAMPLE_RATE)
    for index in range(count):
        value = max(-1.0, min(1.0, synth(index / SAMPLE_RATE)))
        samples.append(round(value * 18000))
    if struct.pack("=h", 1) != struct.pack("<h", 1):
        samples.byteswap()
    with tempfile.SpooledTemporaryFile() as output:
        with wave.open(output, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes(samples.tobytes())
        output.seek(0)
        return output.read()


def music() -> bytes:
    notes = (220.0, 277.18, 329.63, 440.0, 329.63, 277.18, 246.94, 329.63)
    beat = 0.5

    def synth(t: float) -> float:
        note = notes[int(t / beat) % len(notes)]
        phase = t % beat
        envelope = min(1.0, phase * 12.0) * min(1.0, (beat - phase) * 7.0)
        bass = notes[(int(t / beat) // 2) % len(notes)] / 2.0
        return envelope * (0.24 * math.sin(2 * math.pi * note * t) + 0.10 * math.sin(2 * math.pi * bass * t))

    return pcm_wave(len(notes) * beat, synth)


def effect(kind: str) -> bytes:
    if kind == "move":
        return pcm_wave(0.28, lambda t: 0.18 * math.sin(2 * math.pi * 90 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 7.14 * t)))
    if kind == "jump":
        return pcm_wave(0.22, lambda t: (1 - t / 0.22) * 0.45 * math.sin(2 * math.pi * (320 + 900 * t) * t))
    if kind == "laser_start":
        return pcm_wave(0.16, lambda t: (1 - t / 0.16) * 0.42 * math.sin(2 * math.pi * (480 + 1400 * t) * t))
    if kind == "laser_loop":
        return pcm_wave(0.30, lambda t: 0.24 * math.sin(2 * math.pi * 610 * t) + 0.10 * math.sin(2 * math.pi * 1220 * t))
    return pcm_wave(0.18, lambda t: (1 - t / 0.18) * 0.38 * math.sin(2 * math.pi * (720 - 500 * t) * t))


SOUND_SPECS = (
    ("music.loop", "music/alzak_loop.wav", music),
    ("sfx.move", "sfx/move.wav", lambda: effect("move")),
    ("sfx.jump", "sfx/jump.wav", lambda: effect("jump")),
    ("sfx.laser.start", "sfx/laser_start.wav", lambda: effect("laser_start")),
    ("sfx.laser.loop", "sfx/laser_loop.wav", lambda: effect("laser_loop")),
    ("sfx.laser.end", "sfx/laser_end.wav", lambda: effect("laser_end")),
)


def generate(destination: Path) -> None:
    entries: dict[str, dict[str, object]] = {}
    for asset_id, relative, factory in IMAGE_SPECS:
        payload = png_bytes(factory())
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        entries[asset_id] = {"path": relative, "sha256": hashlib.sha256(payload).hexdigest(), "generated": True}
    for asset_id, relative, factory in SOUND_SPECS:
        payload = factory()
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        entries[asset_id] = {"path": relative, "sha256": hashlib.sha256(payload).hexdigest(), "generated": True}
    manifest = {"schema_version": 1, "generator_version": 1, "entries": entries}
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify() -> int:
    with tempfile.TemporaryDirectory(prefix="alzak-placeholders-") as temp:
        generated = Path(temp) / "assets"
        generate(generated)
        expected = sorted(path.relative_to(generated) for path in generated.rglob("*") if path.is_file())
        mismatches = [str(relative) for relative in expected if not (ASSETS / relative).exists() or (ASSETS / relative).read_bytes() != (generated / relative).read_bytes()]
        if mismatches:
            print("Placeholder verification failed: " + ", ".join(mismatches))
            return 1
    print(f"Placeholder verification passed ({len(IMAGE_SPECS)} images, 1 music loop, 5 SFX).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        return verify()
    generate(ASSETS)
    print(f"Generated {len(IMAGE_SPECS)} images, 1 music loop and 5 SFX in {ASSETS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
