# Kontrakt: formát prostředí (`levels/*.json`)

**Vazba**: FR-046, FR-047, FR-084 · Princip III · SC-008, SC-018
**Strojové schéma**: [level.schema.json](./level.schema.json)

Tři soubory, **jedno schéma, jeden loader**. Přidání nebo změna prostředí nesmí
vyžadovat žádnou změnu herní logiky.

```text
levels/
├── level_01_pobocka.json     # order 1, id "pobocka"
├── level_02_sklad.json       # order 2, id "sklad"
└── level_03_kancelar.json    # order 3, id "kancelar"
```

## Příklad (zkrácený, ilustrační — skutečné hodnoty doladí návrh prostředí)

```json
{
  "schema_version": 1,
  "id": "pobocka",
  "display_name": "Obchodní pobočka",
  "order": 1,
  "background_asset_id": "img.bg.pobocka",
  "player_start": { "x": 160, "y": 760 },
  "platforms": [
    { "x": 0,    "y": 880, "w": 640,  "h": 200, "asset_id": "img.platform.pobocka" },
    { "x": 1000, "y": 880, "w": 920,  "h": 200, "asset_id": "img.platform.pobocka" },
    { "x": 1180, "y": 620, "w": 420,  "h": 40,  "asset_id": "img.platform.pobocka" }
  ],
  "pit": { "x": 640, "w": 360, "kill_y": 1080 },
  "enemy": {
    "x": 1240, "y": 548,
    "patrol_min_x": 1180, "patrol_max_x": 1528,
    "asset_id": "img.enemy.walk"
  },
  "exit": {
    "x": 1740, "y": 720, "w": 120, "h": 160,
    "asset_id_inactive": "img.exit.inactive",
    "asset_id_active": "img.exit.active"
  }
}
```

## Validace

Loader ověřuje ve dvou vrstvách. Obě selhávají stejně — `LevelDataError`.

### Vrstva 1 — strukturální (odpovídá `level.schema.json`)

Přítomnost povinných polí · typy · rozsahy · žádná pole navíc ·
`schema_version == 1` · `platform.h >= 32` · `asset_id` odpovídá vzoru.

### Vrstva 2 — sémantická (nad rámec JSON Schema)

| Kontrola | Důvod |
|----------|-------|
| `pit.x + pit.w <= 1920` | propast musí ležet v obraze |
| `player_start` neleží vodorovně nad propastí | jinak hráč padá hned po startu |
| `player_start` stojí nad některou plošinou | US1 scénář 1 „stojí na pevné ploše a nepropadá" |
| `enemy.patrol_min_x < enemy.patrol_max_x` | FR-036 |
| trasa protivníka celá nad jednou plošinou | FR-036 — jinak protivník hlídkuje ve vzduchu |
| `enemy.x` uvnitř `[patrol_min_x, patrol_max_x]` | konzistence startovní pozice |
| `exit` se nepřekrývá s obdélníkem propasti | FR-044 — východ musí být dosažitelný |
| všechna `asset_id` existují v `assets/manifest.json` | FR-050, Princip IV |
| `order` napříč soubory tvoří přesně `{1, 2, 3}` | FR-041 |
| `id` jsou navzájem různá | FR-041 |

## Chybové chování (FR-084, SC-018)

`LevelDataError(file, field, reason)` → aplikace:

1. zobrazí **chybovou obrazovku uvnitř aplikace**;
2. zapíše tutéž zprávu na `sys.stderr`;
3. skončí s návratovým kódem **2**.

Text obrazovky i stderr má tvar:

```text
Chyba dat prostředí
Soubor: levels/level_02_sklad.json
Pole:   platforms[1].h
Důvod:  hodnota 12 je menší než minimální tloušťka plošiny 32
```

Obrazovka je ovladatelná klávesnicí (Esc nebo Enter ukončí) a musí fungovat
i v zabaleném buildu bez konzole. Tiché ukončení ani neošetřená výjimka nejsou
přípustné.

## Co do JSON prostředí NEPATŘÍ

Laditelné herní hodnoty (rychlosti, gravitace, HP, teplota laseru, muzzle offset,
kolizní tloušťka). Ty patří **výhradně** do `src/alzak/config.py` — Princip II.
JSON popisuje **rozmístění a identitu**, nikdy pravidla.
