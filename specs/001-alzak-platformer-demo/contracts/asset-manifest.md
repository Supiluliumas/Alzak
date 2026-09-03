# Kontrakt: registr assetů a manifest stabilních ID

**Vazba**: FR-049, FR-050, FR-081, FR-082 · Princip IV · SC-012, SC-017
**Vlastník implementace**: **Codex** (OD-004) — generátor, soubory i manifest.

## Pravidlo

Herní pravidla **nikdy** nepracují se jménem souboru. Veškerý přístup vede přes
stabilní ID:

```python
surface = registry.image("img.player.idle")     # ANO
sound   = registry.sound("sfx.laser.loop")      # ANO
surface = pygame.image.load("assets/images/player.png")   # ZAKÁZÁNO
```

Nahrazení placeholderu finální grafikou = **výměna souboru** + případně jeden
řádek v manifestu. Žádná změna herní logiky (SC-012).

## Formát `assets/manifest.json`

```json
{
  "schema_version": 1,
  "generator_version": 1,
  "entries": {
    "img.player.idle": {
      "path": "images/alzak_atlas.png",
      "sha256": "…64 hex…",
      "generated": false,
      "source": "imagegen",
      "rect": [20, 220, 250, 375]
    },
    "sfx.jump": {
      "path": "sfx/jump.wav",
      "sha256": "…64 hex…",
      "generated": true
    }
  }
}
```

- `path` je relativní vůči `assets/`.
- `sha256` slouží k ověření SC-017 (bajtová shoda po opětovném běhu generátoru).
- `generated: false` označuje autorský nebo ručně dodaný soubor — generátor jej
  nepřepisuje, ale zahrne jeho checksum do výstupního manifestu.
- Volitelné `rect: [x, y, w, h]` vybírá snímek z atlasu; registr vrátí průhlednou
  kopii tohoto obdélníku.

## Povinná sada ID (FR-049)

| ID | Rozlišuje | Formát |
|----|-----------|--------|
| `img.player.idle` | Alzák stojící | obdélník z transparentního RGBA atlasu |
| `img.player.idle.blink` | Alzák mrkající | obdélník z téhož atlasu |
| `img.player.run`, `.run.2`, `.run.3` | tři fáze běhu | obdélníky z téhož atlasu |
| `img.player.air` | Alzák ve vzduchu | obdélník z téhož atlasu |
| `img.player.fire` | Alzák střílející z pistole | obdélník z téhož atlasu |
| `img.player.hurt` | Alzák po zásahu | obdélník z téhož atlasu |
| `img.enemy.walk` | fasetovaný protivník | PNG RGBA 96×96 |
| `img.enemy.hit` | protivník zasažený | PNG RGBA 96×96 |
| `img.platform.pobocka` | tenká lávka pobočky | PNG RGBA dlaždice 96×48 |
| `img.platform.sklad` | tenká lávka skladu | PNG RGBA dlaždice 96×48 |
| `img.platform.kancelar` | tenká lávka kanceláře | PNG RGBA dlaždice 96×48 |
| `img.pit` | propast | PNG RGBA 96×200 |
| `img.exit.inactive` | **neaktivní** východ | PNG RGBA 120×160 |
| `img.exit.active` | **aktivní** východ, jasně odlišný | PNG RGBA 120×160 |
| `img.bg.pobocka` | high-poly pozadí pobočky | autorské PNG RGB, škálované na 1920×1080 |
| `img.bg.sklad` | high-poly pozadí skladu | autorské PNG RGB, škálované na 1920×1080 |
| `img.bg.kancelar` | high-poly pozadí kanceláře | autorské PNG RGB, škálované na 1920×1080 |
| `img.hud.energy_full` | plný bod energie | PNG RGBA 48×48 |
| `img.hud.energy_empty` | prázdný bod energie | PNG RGBA 48×48 |
| `img.hud.heat_frame` | rám ukazatele teploty | PNG RGBA 240×32 |
| `img.hud.heat_fill` | výplň ukazatele teploty | PNG RGBA 240×32 |
| `music.loop` | hudební smyčka | WAV PCM16 mono 22050 Hz |
| `sfx.move` | pohyb po zemi (smyčka) | WAV PCM16 mono 22050 Hz |
| `sfx.jump` | skok | WAV |
| `sfx.laser.start` | spuštění laseru | WAV |
| `sfx.laser.loop` | trvání laseru (smyčka) | WAV |
| `sfx.laser.end` | ukončení laseru | WAV |
| `font.ui` | font UI, jen pokud vestavěný nestačí (research R14) | TTF, `generated: false` |

Přesně **5 zvukových efektů** (FR-058, A-003) — žádný zvuk zásahu ani ztráty
energie.

## Chování registru

| Situace | Chování |
|---------|---------|
| ID chybí v manifestu | **tvrdá chyba při startu** — hra se nespustí |
| ID je v manifestu, soubor chybí (vývoj) | zřetelný růžový placeholder + varování na stderr; test manifestu selže |
| ID je v manifestu, soubor chybí (frozen build) | tvrdá chyba — build je vadný |
| zvukové zařízení nedostupné | `registry.sound()` vrací no-op objekt, hra běží dál |

Načítání je líné a cachované podle ID; stejné ID se nikdy nenačte dvakrát.

## Generátor (FR-082, SC-017)

`tools/generate_placeholders.py`:

- používá **výhradně standardní knihovnu** (`zlib`, `struct`, `wave`, `hashlib`)
  pro procedurálně generované soubory;
- prochází položky v pevném zapsaném pořadí;
- žádný `random` bez pevného seed, žádný časový údaj v metadatech;
- přepíše jen procedurální soubory v `assets/`, autorský atlas a pozadí pouze
  indexuje, kopíruje do dočasného ověřovacího výstupu a aktualizuje jejich `sha256`;
- `--verify` režim pouze porovná checksumy a **nic nezapisuje** (pro CI).

**Zakázáno**: hra generátor volá za běhu (FR-081); build nebo CI ho volá jako
povinný krok, který přepisuje soubory.

## Ověření SC-017

```text
1. sha256 všech souborů v assets/  → A
2. python tools/generate_placeholders.py
3. sha256 všech souborů v assets/  → B
4. A == B   (bajtová shoda, jinak SC-017 selhalo)
```
