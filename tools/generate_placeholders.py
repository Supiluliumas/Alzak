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

    def polygon(self, points: tuple[tuple[int, int], ...], color: Color) -> None:
        if len(points) < 3:
            return
        min_y = max(0, min(y for _, y in points))
        max_y = min(self.height - 1, max(y for _, y in points))
        for y in range(min_y, max_y + 1):
            intersections: list[float] = []
            for index, (x1, y1) in enumerate(points):
                x2, y2 = points[(index + 1) % len(points)]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    intersections.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
            intersections.sort()
            for index in range(0, len(intersections) - 1, 2):
                self.rect(math.ceil(intersections[index]), y, math.floor(intersections[index + 1] - intersections[index]) + 1, 1, color)


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
    c = Canvas(112, 144)
    outline = (22, 55, 25, 255)
    deep_green = (49, 129, 35, 255)
    green = (91, 190, 47, 255)
    light = (158, 234, 79, 255)
    silver_dark = (73, 94, 105, 255)
    silver = (180, 204, 214, 255)
    silver_light = (238, 247, 247, 255)
    charcoal = (35, 43, 51, 255)
    eye = (247, 252, 246, 255)
    run_pose = {
        "run1": ((28, 122), (69, 128), 6),
        "run2": ((37, 130), (61, 130), 1),
        "run3": ((49, 127), (82, 119), -5),
        "air": ((31, 122), (76, 112), -7),
    }
    left_foot, right_foot, bob = run_pose.get(pose, ((35, 130), (62, 130), 0))
    if pose == "hurt":
        left_foot, right_foot, bob = (41, 131), (70, 129), 3

    # Legs, boots and rear arm.
    c.line(43, 103 + bob, left_foot[0], left_foot[1] - 5, outline, 13)
    c.line(43, 103 + bob, left_foot[0], left_foot[1] - 5, green, 8)
    c.line(62, 103 + bob, right_foot[0], right_foot[1] - 5, outline, 13)
    c.line(62, 103 + bob, right_foot[0], right_foot[1] - 5, deep_green, 8)
    c.ellipse(left_foot[0] + 3, left_foot[1], 16, 8, silver_dark)
    c.ellipse(left_foot[0] + 5, left_foot[1] - 2, 13, 5, silver_light)
    c.ellipse(right_foot[0] + 4, right_foot[1], 16, 8, silver_dark)
    c.ellipse(right_foot[0] + 6, right_foot[1] - 2, 13, 5, silver_light)
    rear_hand = (12, 92 + bob) if pose not in {"run1", "run3", "air"} else (17, 75 + bob)
    c.line(31, 82 + bob, rear_hand[0], rear_hand[1], outline, 13)
    c.line(31, 82 + bob, rear_hand[0], rear_hand[1], deep_green, 8)
    c.circle(rear_hand[0], rear_hand[1], 6, green)

    # Silver utility tunic with a tapered silhouette and material highlights.
    c.polygon(((25, 70 + bob), (67, 67 + bob), (78, 111 + bob), (20, 111 + bob)), silver_dark)
    c.polygon(((28, 72 + bob), (65, 70 + bob), (72, 106 + bob), (24, 106 + bob)), silver)
    c.polygon(((31, 74 + bob), (42, 72 + bob), (38, 105 + bob), (28, 105 + bob)), silver_light)
    c.line(27, 78 + bob, 67, 76 + bob, (247, 252, 252, 255), 3)
    c.line(26, 105 + bob, 70, 105 + bob, charcoal, 2)

    # Pear-shaped side-profile head, antenna and expressive face.
    c.ellipse(43, 43 + bob, 36, 41, outline)
    c.ellipse(43, 43 + bob, 32, 37, green)
    c.ellipse(32, 28 + bob, 17, 23, light)
    c.circle(43, 3 + bob, 9, outline)
    c.circle(43, 3 + bob, 6, light)
    c.circle(72, 50 + bob, 7, green)
    c.ellipse(60, 38 + bob, 13, 17, eye)
    if pose == "blink":
        c.line(51, 38 + bob, 70, 40 + bob, charcoal, 3)
    elif pose == "hurt":
        c.line(51, 31 + bob, 69, 45 + bob, charcoal, 3)
        c.line(68, 31 + bob, 52, 45 + bob, charcoal, 3)
    else:
        c.ellipse(66, 41 + bob, 5, 8, charcoal)
        c.circle(68, 38 + bob, 2, silver_light)
    if pose == "hurt":
        c.ellipse(63, 59 + bob, 9, 6, (91, 34, 37, 255))
    else:
        c.line(53, 57 + bob, 61, 62 + bob, charcoal, 3)
        c.line(61, 62 + bob, 70, 57 + bob, charcoal, 3)
    c.ellipse(29, 23 + bob, 9, 14, (205, 255, 126, 75))

    # Forward arm and compact laser pistol; emitter center is (108, 71+bob).
    shoulder = (66, 79 + bob)
    hand = (79, 76 + bob) if pose != "hurt" else (76, 91 + bob)
    c.line(shoulder[0], shoulder[1], hand[0], hand[1], outline, 13)
    c.line(shoulder[0], shoulder[1], hand[0], hand[1], green, 8)
    gun_y = 64 + bob if pose != "hurt" else 80 + bob
    c.polygon(((75, gun_y), (103, gun_y), (109, gun_y + 7), (103, gun_y + 15), (75, gun_y + 15)), charcoal)
    c.rect(80, gun_y + 3, 23, 9, silver)
    c.rect(84, gun_y + 5, 13, 5, (144, 238, 67, 255))
    c.rect(77, gun_y + 13, 8, 13, silver_dark)
    c.circle(105, gun_y + 7, 6, charcoal)
    c.circle(107, gun_y + 7, 4, (241, 65, 62, 255))
    c.circle(108, gun_y + 6, 2, (255, 220, 125, 255))
    c.circle(hand[0], hand[1], 6, green)
    if pose == "fire":
        c.line(111, gun_y + 7, 111, gun_y + 7, (255, 245, 170, 255), 5)
    return c


def enemy(hit: bool) -> Canvas:
    c = Canvas(96, 96)
    body = (255, 116, 75, 255) if hit else (111, 71, 190, 255)
    body_light = (255, 181, 112, 255) if hit else (184, 133, 244, 255)
    body_shadow = (155, 55, 51, 255) if hit else (55, 38, 113, 255)
    outline = (27, 24, 48, 255)

    # Reality-inspired high-poly service drone: faceted shell, visor and jointed feet.
    c.ellipse(48, 55, 39, 31, outline)
    c.polygon(((14, 49), (28, 26), (68, 25), (85, 48), (77, 74), (31, 82)), body_shadow)
    c.polygon(((18, 47), (31, 30), (50, 27), (48, 73), (30, 76)), body_light)
    c.polygon(((50, 27), (67, 30), (80, 48), (73, 70), (48, 73)), body)
    c.polygon(((22, 33), (73, 33), (79, 51), (17, 51)), (45, 60, 83, 255))
    c.polygon(((25, 36), (69, 36), (73, 47), (21, 47)), (93, 222, 229, 255))
    c.polygon(((25, 36), (46, 36), (42, 47), (21, 47)), (202, 250, 244, 255))
    c.circle(35, 42, 4, (20, 31, 48, 255))
    c.circle(61, 42, 4, (20, 31, 48, 255))
    c.circle(34, 40, 1, (255, 255, 255, 255))
    c.circle(60, 40, 1, (255, 255, 255, 255))
    c.polygon(((36, 60), (62, 60), (57, 68), (41, 68)), outline)
    c.rect(43, 62, 12, 2, (230, 239, 225, 255))
    c.line(48, 27, 48, 13, outline, 4)
    c.circle(48, 10, 7, outline)
    c.circle(48, 10, 4, (255, 210, 71, 255))
    c.line(27, 74, 18, 88, outline, 8)
    c.line(67, 74, 77, 88, outline, 8)
    c.polygon(((7, 85), (24, 82), (33, 91), (8, 93)), (63, 72, 91, 255))
    c.polygon(((66, 91), (76, 82), (92, 86), (91, 93)), (63, 72, 91, 255))
    return c


def tile(kind: str) -> Canvas:
    palettes = {
        "pobocka": ((36, 126, 156, 255), (72, 178, 194, 255), (220, 244, 245, 255)),
        "sklad": ((104, 80, 55, 255), (181, 132, 70, 255), (238, 186, 75, 255)),
        "kancelar": ((47, 75, 101, 255), (91, 126, 151, 255), (166, 205, 221, 255)),
    }
    c = Canvas(96, 48)
    dark, mid, light = palettes[kind]
    # A seamless catwalk/architectural ledge; collision can be tall while the
    # artwork remains a thin high-poly structure instead of a filled block.
    c.rect(0, 0, 96, 5, light)
    c.rect(0, 5, 96, 8, mid)
    c.rect(0, 13, 96, 5, dark)
    c.polygon(((0, 18), (96, 18), (96, 31), (0, 42)), dark)
    c.polygon(((0, 18), (48, 18), (37, 36), (0, 42)), mid)
    c.polygon(((48, 18), (96, 18), (96, 31), (59, 36)), (25, 37, 48, 230))
    c.line(0, 41, 96, 30, (21, 27, 35, 230), 3)
    c.line(10, 38, 28, 18, light, 2)
    c.line(59, 35, 77, 18, light, 2)
    for x in (12, 48, 84):
        c.circle(x, 8, 3, (188, 246, 255, 255))
        c.circle(x, 8, 1, (255, 255, 255, 255))
    return c


def pit() -> Canvas:
    c = Canvas(96, 200)
    for y in range(200):
        alpha = min(245, 80 + y)
        c.rect(0, y, 96, 1, (4, 6, 18, alpha))
    c.rect(0, 0, 96, 5, (102, 221, 242, 220))
    c.rect(0, 5, 96, 5, (89, 49, 142, 210))
    for radius, color in ((43, (40, 19, 72, 230)), (29, (75, 28, 101, 235)), (14, (3, 4, 13, 255))):
        c.ellipse(48, 38, radius, max(6, radius // 4), color)
    return c


def exit_door(active: bool) -> Canvas:
    c = Canvas(120, 160)
    frame = (157, 239, 76, 255) if active else (91, 113, 126, 255)
    frame_light = (223, 255, 178, 255) if active else (185, 207, 214, 255)
    glow = (95, 220, 100, 75) if active else (32, 42, 48, 55)
    # Faceted portal frame and recessed glass panel.
    c.polygon(((7, 18), (22, 3), (98, 3), (114, 18), (114, 160), (7, 160)), glow)
    c.polygon(((14, 21), (27, 9), (94, 9), (106, 21), (106, 160), (14, 160)), frame)
    c.polygon(((24, 29), (33, 20), (88, 20), (97, 29), (97, 160), (24, 160)), frame_light)
    c.polygon(((31, 34), (89, 34), (89, 160), (31, 160)), (19, 42, 54, 255))
    c.polygon(((35, 39), (58, 39), (50, 155), (35, 155)), (45, 91, 103, 255))
    c.polygon(((58, 39), (85, 39), (85, 155), (50, 155)), (24, 60, 72, 255))
    c.circle(78, 98, 7, (25, 35, 42, 255))
    c.circle(78, 98, 4, frame)
    if active:
        for y in range(48, 145, 22):
            c.polygon(((36, y), (84, y), (80, y + 5), (35, y + 5)), (122, 255, 137, 180))
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
    ("img.enemy.walk", "images/enemy_walk.png", lambda: enemy(False)),
    ("img.enemy.hit", "images/enemy_hit.png", lambda: enemy(True)),
    ("img.platform.pobocka", "images/platform_pobocka.png", lambda: tile("pobocka")),
    ("img.platform.sklad", "images/platform_sklad.png", lambda: tile("sklad")),
    ("img.platform.kancelar", "images/platform_kancelar.png", lambda: tile("kancelar")),
    ("img.pit", "images/pit.png", pit),
    ("img.exit.inactive", "images/exit_inactive.png", lambda: exit_door(False)),
    ("img.exit.active", "images/exit_active.png", lambda: exit_door(True)),
    ("img.hud.energy_full", "images/hud_energy_full.png", lambda: hud_energy(True)),
    ("img.hud.energy_empty", "images/hud_energy_empty.png", lambda: hud_energy(False)),
    ("img.hud.heat_frame", "images/hud_heat_frame.png", lambda: heat_bar(True)),
    ("img.hud.heat_fill", "images/hud_heat_fill.png", lambda: heat_bar(False)),
)

AUTHORED_IMAGE_SPECS = (
    ("img.bg.pobocka", "images/bg_pobocka.png"),
    ("img.bg.sklad", "images/bg_sklad.png"),
    ("img.bg.kancelar", "images/bg_kancelar.png"),
)

AUTHORED_ATLAS_SPECS = (
    ("img.player.idle", "images/alzak_atlas.png", (20, 220, 250, 375)),
    ("img.player.idle.blink", "images/alzak_atlas.png", (270, 220, 230, 375)),
    ("img.player.run", "images/alzak_atlas.png", (480, 235, 290, 365)),
    ("img.player.run.2", "images/alzak_atlas.png", (750, 225, 280, 360)),
    ("img.player.run.3", "images/alzak_atlas.png", (1020, 195, 270, 355)),
    ("img.player.air", "images/alzak_atlas.png", (1280, 160, 265, 430)),
    ("img.player.fire", "images/alzak_atlas.png", (1530, 255, 310, 345)),
    ("img.player.hurt", "images/alzak_atlas.png", (1820, 255, 228, 345)),
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
    for asset_id, relative in AUTHORED_IMAGE_SPECS:
        source = ASSETS / relative
        payload = source.read_bytes()
        path = destination / relative
        if path.resolve() != source.resolve():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        entries[asset_id] = {
            "path": relative,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "generated": False,
            "source": "imagegen",
        }
    for asset_id, relative, rect in AUTHORED_ATLAS_SPECS:
        source = ASSETS / relative
        payload = source.read_bytes()
        path = destination / relative
        if path.resolve() != source.resolve():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        entries[asset_id] = {
            "path": relative,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "generated": False,
            "source": "imagegen",
            "rect": rect,
        }
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
    print(
        "Asset verification passed "
        f"({len(IMAGE_SPECS)} deterministic images, "
        f"{len(AUTHORED_IMAGE_SPECS)} authored backgrounds, "
        f"{len(AUTHORED_ATLAS_SPECS)} authored sprite frames, 1 music loop, 5 SFX)."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        return verify()
    generate(ASSETS)
    print(
        f"Generated {len(IMAGE_SPECS)} deterministic images and indexed "
        f"{len(AUTHORED_IMAGE_SPECS)} authored backgrounds plus "
        f"{len(AUTHORED_ATLAS_SPECS)} authored sprite frames, "
        f"1 music loop and 5 SFX in {ASSETS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
