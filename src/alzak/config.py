"""Single source of truth for all tunable game values."""

DISPLAY = {
    "logical_size": (1920, 1080),
    "target_fps": 60,
    "window_default_size": (1280, 720),
    "letterbox_color": (0, 0, 0),
    "fullscreen_key": "F11",
    "title": "Alzák: Mise splněna!",
}

SIM = {"dt": 1.0 / 120.0, "max_frame_time": 0.25}

PLAYER = {
    "size": (64.0, 96.0),
    "max_run_speed": 520.0,
    "ground_accel": 3600.0,
    "ground_friction": 4200.0,
    "air_accel": 1800.0,
    "air_friction": 600.0,
    "gravity": 3400.0,
    "max_fall_speed": 1500.0,
    "movement_visual_threshold": 1.0,
}

JUMP = {
    "velocity": -1150.0,
    "cut_multiplier": 0.45,
    "coyote_time": 0.10,
    "buffer_time": 0.12,
}

ENERGY = {
    "max": 3,
    "invuln_time": 1.0,
    "knockback": (420.0, -520.0),
    "hurt_flash_period": 0.10,
}

LASER = {
    "muzzle_offset": (52.0, 38.0),
    "collision_thickness": 16.0,
    "dps": 100.0,
    "heat_time_to_full": 1.5,
    "cool_time_from_full": 2.0,
    "reactivate_threshold": 0.35,
    "draw_core_thickness": 6,
    "draw_glow_thickness": 18,
    "draw_core_color": (255, 255, 255),
    "draw_glow_color": (255, 64, 64),
    "draw_locked_color": (120, 120, 130),
    "impact_radius": 10,
}

ENEMY = {
    "size": (72.0, 72.0),
    "speed": 180.0,
    "hp": 100.0,
    "hit_flash_time": 0.08,
    "hp_epsilon": 1e-9,
}

LEVEL = {
    "min_platform_thickness": 32.0,
    "transition_fade_time": 0.35,
    "pit_visual_height": 160.0,
}

HUD = {
    "energy_icon_size": (48, 48),
    "energy_origin": (48, 42),
    "energy_gap": 12,
    "heat_bar_size": (240, 32),
    "heat_bar_origin": (48, 112),
    "text_origin": (1450, 42),
    "font_size_hud": 34,
    "font_size_menu": 60,
    "font_size_title": 92,
    "color_normal": (235, 245, 250),
    "color_warning": (255, 110, 80),
    "panel_color": (13, 25, 38, 210),
}

AUDIO = {
    "music_volume": 0.60,
    "music_volume_paused": 0.15,
    "sfx_volume": 0.80,
    "frequency": 22050,
    "channels": 1,
    "buffer": 512,
}

UI = {
    "menu_color": (238, 247, 250),
    "menu_selected_color": (167, 239, 69),
    "overlay_color": (5, 12, 22, 205),
    "hint_color": (170, 192, 205),
    "menu_line_gap": 86,
}
