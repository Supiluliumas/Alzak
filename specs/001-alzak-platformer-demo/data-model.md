# Phase 1 — Data Model: Alzák tech demo

**Feature**: `001-alzak-platformer-demo` | **Date**: 2026-09-03
**Zdroj**: [spec.md](./spec.md) Key Entities · [research.md](./research.md) · Principy II, III, IV, V

Rozdělení podle vrstev: **simulační stav** (bez pygame), **datový vstup**
(JSON), **konfigurace** (jediný modul) a **prezentační stav** (pygame).

---

## 1. Simulační stav (`src/alzak/sim/`)

Vše `dataclass`, žádný pygame typ. Souřadnice `float`, v logickém prostoru
1920 × 1080. Rozměry v pixelech.

### 1.1 `Player`

| Pole | Typ | Význam | Invariant |
|------|-----|--------|-----------|
| `x`, `y` | `float` | levý horní roh | uvnitř `[-w, 1920]` × `[-h, ∞)` |
| `w`, `h` | `float` | rozměr kolizního boxu | z `config.PLAYER` |
| `vx`, `vy` | `float` | rychlost px/s | `abs(vx) <= MAX_RUN_SPEED`, `vy <= MAX_FALL_SPEED` |
| `facing` | `int` | `+1` vpravo, `-1` vlevo | ∈ {−1, +1}; mění se jen při vstupu, ne setrvačností |
| `on_ground` | `bool` | výsledek kolize zdola v tomto kroku | FR-018 |
| `coyote_timer` | `float` | zbývá s | `0 <= t <= COYOTE_TIME` |
| `jump_buffer_timer` | `float` | zbývá s | `0 <= t <= JUMP_BUFFER` |
| `jump_held` | `bool` | mezerník stále držen | řídí proměnlivou výšku |
| `energy` | `int` | body energie | `0 <= energy <= ENERGY_MAX (3)` |
| `invuln_timer` | `float` | zbývá nezranitelnosti s | `0 <= t <= INVULN_TIME` |

**Přechody**: `on_ground` → false ⇒ `coyote_timer = COYOTE_TIME`.
Skok je možný, právě když `on_ground or coyote_timer > 0`; provedením se oba
timery vynulují. Zásah ⇒ `energy -= 1`, `invuln_timer = INVULN_TIME`,
`vx, vy = ±KNOCKBACK`. `energy == 0` ⇒ událost `PLAYER_DEFEATED`.

### 1.2 `Enemy`

| Pole | Typ | Význam | Invariant |
|------|-----|--------|-----------|
| `x`, `y`, `w`, `h` | `float` | box | `w`, `h` z `config.ENEMY` |
| `patrol_min_x`, `patrol_max_x` | `float` | krajní body trasy z JSON | `min < max`; oba nad plošinou |
| `direction` | `int` | `+1` / `−1` | otočí se na krajním bodě (FR-036) |
| `hp` | `float` | zbývající životy | `0 <= hp <= ENEMY_HP` |
| `alive` | `bool` | `hp > 0` | `alive == (hp > 0)` |
| `hit_flash_timer` | `float` | vizuální odezva zásahu | `0 <= t <= HIT_FLASH_TIME` |

**Kumulace poškození (FR-039, SC-020)**: `hp` klesá o `LASER.dps * SIM_DT` za
každý simulační krok kontaktu a **nikdy neroste**. Přerušení střelby, pád hráče
do propasti ani nezranitelnost `hp` nevrací. Jediná cesta zpět na `ENEMY_HP` je
nové sestavení `LevelState` (restart prostředí nebo vstup do prostředí).

### 1.3 `LaserState`

| Pole | Typ | Význam | Invariant |
|------|-----|--------|-----------|
| `mode` | `enum` | `IDLE` / `FIRING` / `LOCKED` | přechody níže |
| `heat` | `float` | teplota | `0.0 <= heat <= 1.0` |
| `start` | `(float, float)` | muzzle bod | odvozen z `Player` + `LASER.muzzle_offset` |
| `end_x` | `float` | konec paprsku | mezi `start.x` a hranou obrazovky |
| `hit_kind` | `enum` | `NONE` / `PLATFORM` / `ENEMY` | co paprsek zastavilo |

**Stavový diagram**:

```text
IDLE  --X stisknuto & heat < 1.0-->  FIRING
FIRING --heat dosáhne 1.0-->         LOCKED     (FR-032)
FIRING --X uvolněno-->               IDLE
LOCKED --heat klesne pod REACTIVATE_THRESHOLD--> IDLE
LOCKED --X stále drženo--> zůstává LOCKED, dokud heat neklesne pod práh
IDLE   --pauza / změna stavu obrazovky--> IDLE + okamžité ukončení zvuku (FR-060)
```

`heat += SIM_DT / HEAT_TIME_TO_FULL` ve `FIRING`;
`heat -= SIM_DT / COOL_TIME_FROM_FULL` v `IDLE` i `LOCKED`, ořezáno na `[0, 1]`.

**Muzzle a paprsek** (FR-085, FR-086):

```text
muzzle_x = x + (mx if facing > 0 else w - mx)      # mx = LASER.muzzle_offset[0]
muzzle_y = y + LASER.muzzle_offset[1]
band     = [muzzle_y - T/2, muzzle_y + T/2]        # T = LASER.collision_thickness = 16
end_x    = nejbližší x ve směru facing, kde box protínající band začíná;
           jinak 0 (vlevo) nebo 1920 (vpravo)
```

### 1.4 `Platform`, `Pit`, `Exit`

| Entita | Pole | Poznámka |
|--------|------|----------|
| `Platform` | `x, y, w, h, asset_id` | `h >= MIN_PLATFORM_THICKNESS` (32 px, R3) |
| `Pit` | `x, w, kill_y` | pád pod `kill_y` v rozsahu `[x, x+w]` ⇒ `PLAYER_FELL` |
| `Exit` | `x, y, w, h, active: bool` | `active` false na začátku, true po `enemy.alive == False` (FR-040, FR-044) |

### 1.5 `LevelState`

Běhový stav jednoho prostředí. Vzniká **vždy** z `LevelData` + `config`, nikdy
mutací předchozího — proto je restart triviálně korektní (FR-026).

| Pole | Typ |
|------|-----|
| `data` | `LevelData` (neměnné, viz §2) |
| `player` | `Player` |
| `enemy` | `Enemy` |
| `laser` | `LaserState` |
| `exit` | `Exit` |
| `completed` | `bool` |
| `failed` | `bool` |

**Pořadí vyhodnocení v jednom kroku** (rozhoduje o A-010 a Edge Cases):

```text
1. vstup → záměry (pohyb, skok, střelba)
2. laser: heat, paprsek, poškození protivníka
3. protivník: hlídkování
4. hráč: zrychlení, gravitace, integrace, kolize po osách
5. kontakt hráč × protivník  → případná ztráta energie
6. pád do propasti           → případná ztráta energie + respawn
7. vyhodnocení porážky protivníka → aktivace východu
8. vyhodnocení energie == 0  → failed = True        (má PŘEDNOST, A-010)
9. vyhodnocení vstupu do aktivního východu → completed = True (jen když not failed)
```

### 1.6 `Session`

| Pole | Typ | Význam |
|------|-----|--------|
| `level_index` | `int` | 0..2, pevné pořadí pobočka → sklad → kancelář (FR-041) |
| `level_ids` | `tuple[str, str, str]` | z pořadí souborů v `levels/` |
| `current` | `LevelState` | aktuální prostředí |
| `finished` | `bool` | dokončena všechna tři |

Vstup do nového prostředí ⇒ nová `LevelState` s `energy = ENERGY_MAX` (FR-025).

### 1.7 `InputSnapshot` a `SimEvent`

`InputSnapshot` (čisté booly — Princip V, žádný `pygame.key`):
`left`, `right`, `jump_pressed`, `jump_held`, `fire_held`.

`SimEvent` — výčet toho, co simulace ohlásila prezentační a zvukové vrstvě:
`JUMPED` · `LANDED` · `LASER_STARTED` · `LASER_STOPPED` · `LASER_OVERHEATED` ·
`ENEMY_HIT` · `ENEMY_DEFEATED` · `EXIT_ACTIVATED` · `PLAYER_HURT` ·
`PLAYER_FELL` · `PLAYER_DEFEATED` · `LEVEL_COMPLETED`.

Simulace vrací seznam událostí za krok. **Zvuk se spouští výhradně z událostí**,
nikdy z čtení vnitřního stavu — tím je FR-059 a FR-060 splněno na jednom místě.

---

## 2. Datový vstup — `LevelData` (`levels/*.json`)

Neměnná struktura načtená loaderem. Úplné schéma:
[contracts/level.schema.json](./contracts/level.schema.json),
popis a chybové chování: [contracts/level-format.md](./contracts/level-format.md).

| Pole | Typ | Povinné | Validace |
|------|-----|---------|----------|
| `schema_version` | `int` | ano | `== 1` |
| `id` | `str` | ano | `^[a-z0-9_]+$`, unikátní |
| `display_name` | `str` | ano | neprázdný (čeština, A-004) |
| `order` | `int` | ano | 1..3, unikátní napříč soubory |
| `player_start` | `{x, y}` | ano | uvnitř 1920×1080, ne nad propastí |
| `platforms[]` | `{x, y, w, h, asset_id}` | ano, ≥ 1 | `h >= 32`; `asset_id` v manifestu |
| `pit` | `{x, w, kill_y}` | ano | `0 <= x`, `x+w <= 1920`, `kill_y <= 1080` |
| `enemy` | `{x, y, patrol_min_x, patrol_max_x, asset_id}` | ano | trasa nad existující plošinou |
| `exit` | `{x, y, w, h, asset_id_inactive, asset_id_active}` | ano | nepřekrývá propast |
| `background_asset_id` | `str` | ano | v manifestu |

**Invariant napříč soubory**: `order` tvoří přesně `{1, 2, 3}`; `id` jsou různá.
Porušení ⇒ `LevelDataError` a chybová obrazovka (FR-084).

---

## 3. Konfigurace — `src/alzak/config.py` (Princip II)

Jediné místo s laditelnými hodnotami. **Uvedené hodnoty jsou startovní sada**
(research R15); mění se v P9 podle ručního testu, ale musí trvale splňovat
SC-004…SC-007 a SC-021.

### `DISPLAY`
| Klíč | Hodnota | Pozn. |
|------|---------|-------|
| `logical_size` | `(1920, 1080)` | FR-001, nikdy se nemění |
| `target_fps` | `60` | FR-004 |
| `window_default_size` | `(1280, 720)` | okno při startu |
| `letterbox_color` | `(0, 0, 0)` | FR-002 |
| `fullscreen_key` | `F11` | FR-003 |

### `SIM`
| Klíč | Hodnota |
|------|---------|
| `dt` | `1/120` (research R1) |
| `max_frame_time` | `0.25` |

### `PLAYER`
| Klíč | Hodnota | Vazba |
|------|---------|-------|
| `size` | `(64, 96)` | |
| `max_run_speed` | `520` px/s | FR-011 |
| `ground_accel` | `3600` px/s² | FR-011 |
| `ground_friction` | `4200` px/s² | FR-011 |
| `air_accel` | `1800` px/s² | FR-012 |
| `air_friction` | `600` px/s² | FR-012 |
| `gravity` | `3400` px/s² | FR-013 |
| `max_fall_speed` | `1500` px/s | FR-013, R3 |

### `JUMP`
| Klíč | Hodnota | Vazba |
|------|---------|-------|
| `velocity` | `-1150` px/s | ≈ 194 px výšky |
| `cut_multiplier` | `0.45` | FR-014 |
| `coyote_time` | `0.10` s | FR-015, SC-007 |
| `buffer_time` | `0.12` s | FR-016, SC-007 |

### `ENERGY`
| Klíč | Hodnota | Vazba |
|------|---------|-------|
| `max` | `3` | FR-020 |
| `invuln_time` | `1.0` s | FR-021, SC-006 |
| `knockback` | `(420, -520)` px/s | FR-021 |
| `hurt_flash_period` | `0.1` s | FR-021 vizuální odezva |

### `LASER` — geometrie, chování i vzhled (FR-034, FR-085, FR-086, FR-087)
| Klíč | Hodnota | Vazba |
|------|---------|-------|
| `muzzle_offset` | `(52, 38)` px od levého horního rohu hráče, zrcadleno podle `facing` | **FR-085** |
| `collision_thickness` | `16` px | **FR-086**, OD-006 |
| `dps` | `100.0` (při `ENEMY.hp = 100`) ⇒ 1,0 s | FR-039, SC-004 |
| `heat_time_to_full` | `1.5` s | FR-030, SC-005 |
| `cool_time_from_full` | `2.0` s | FR-031 |
| `reactivate_threshold` | `0.35` | FR-032 |
| `draw_core_thickness` | `6` px | **FR-087** (vzhled ≠ kolize) |
| `draw_glow_thickness` | `18` px | FR-087 |
| `draw_core_color` | `(255, 255, 255)` | FR-087 |
| `draw_glow_color` | `(255, 64, 64)` | FR-087 |
| `draw_locked_color` | `(120, 120, 130)` | vizuál zablokovaného stavu |
| `impact_radius` | `10` px | odezva zásahu |

> **Kontrola Principu II**: v `sim/laser.py` ani v `render/world.py` nesmí být
> jediné číslo popisující laser. Ověřuje SC-021.

### `ENEMY`
| Klíč | Hodnota | Vazba |
|------|---------|-------|
| `size` | `(72, 72)` | |
| `speed` | `180` px/s | FR-036 |
| `hp` | `100.0` | FR-039 |
| `hit_flash_time` | `0.08` s | FR-038 |
| `hp_epsilon` | `1e-9` | numerická stabilita nulových HP |

### `LEVEL`
| Klíč | Hodnota | Vazba |
|------|---------|-------|
| `min_platform_thickness` | `32` px | R3, RP-05 |
| `transition_fade_time` | `0.35` s (každý směr) | FR-048 |
| `pit_visual_height` | `160` px | centrální prezentační ladění |

### `HUD`
`energy_icon_size`, `energy_origin`, `heat_bar_size`, `heat_bar_origin`,
`text_origin`, `font_size_hud`, `font_size_menu`, `color_normal`,
`color_warning` — FR-052.

### `AUDIO`
`music_volume` `0.6` · `music_volume_paused` `0.15` (FR-057) · `sfx_volume` `0.8` ·
`frequency` `22050` · `channels` `1` · `buffer` `512`.

### `UI`
Barvy menu, barva vybrané položky, barva overlay, barva nápovědy a rozestup
řádků menu. Všechny prezentační konstanty sdílené obrazovkami zůstávají v
centrální konfiguraci.

---

## 4. Prezentační stav (`src/alzak/render/`, `screens/`)

| Entita | Pole | Poznámka |
|--------|------|----------|
| `Presentation` | `window`, `logical_surface`, `scale`, `offset`, `fullscreen` | **jediný** držitel velikosti okna (Princip VII) |
| `AssetRegistry` | `manifest: dict[str, str]`, `_cache` | stabilní ID → soubor (FR-050) |
| `ScreenMachine` | `state`, `pending_state`, `transition_timer` | stavy níže |
| `AudioMixer` | `music_channel`, `laser_loop_channel`, `available: bool` | `available=False` ⇒ vše no-op (Edge Case) |

**Stavy obrazovek** (research R13):

```text
TITLE ──Spustit──> TRANSITION ──> PLAY
PLAY  ──Escape──> PAUSE ──Pokračovat──> PLAY
                        ──Restartovat prostředí──> PLAY (nová LevelState)
                        ──Ukončit hru──> TITLE            (FR-053, FR-083)
PLAY  ──energie 0──> GAMEOVER ──Opakovat prostředí──> PLAY (nová LevelState)
                              ──Ukončit hru──> TITLE      (FR-054, FR-083)
PLAY  ──dokončeno & index<2──> TRANSITION ──> PLAY (další prostředí)
PLAY  ──dokončeno & index==2──> TRANSITION ──> FINISH
FINISH ──Spustit znovu──> TRANSITION ──> PLAY (index 0)
FINISH ──Ukončit──> konec aplikace                        (FR-055, FR-083)
TITLE  ──Ukončit──> konec aplikace                        (FR-051, FR-083)
libovolný stav ──LevelDataError──> ERROR ──klávesa──> exit(2)  (FR-084)
```

Aplikaci lze ukončit **pouze** z `TITLE` a `FINISH` (FR-083). Simulace se
posouvá **pouze** ve stavu `PLAY`.

---

## 5. Mapování entit na požadavky

| Entita | Pokrývá |
|--------|---------|
| `Player` | FR-006, FR-007, FR-011…FR-018, FR-020…FR-023 |
| `Enemy` | FR-035…FR-039 |
| `LaserState` | FR-008, FR-027…FR-034, FR-085…FR-087 |
| `Platform` / `Pit` / `Exit` | FR-017, FR-023, FR-040, FR-043…FR-045 |
| `LevelState` | FR-026, FR-042, FR-045 |
| `Session` | FR-025, FR-041, FR-048 |
| `LevelData` | FR-046, FR-047, FR-084 |
| `config` | FR-019, FR-034, FR-085…FR-087 |
| `AssetRegistry` | FR-049, FR-050, FR-081 |
| `ScreenMachine` | FR-005, FR-009, FR-024, FR-051…FR-055, FR-083 |
| `AudioMixer` | FR-056…FR-060 |
