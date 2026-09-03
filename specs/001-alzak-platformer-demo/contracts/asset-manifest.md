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
      "path": "images/player_idle.png",
      "sha256": "…64 hex…",
      "generated": true
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
- `generated: false` označuje ručně dodaný soubor (např. přibalený font) —
  generátor jej nepřepisuje.

## Povinná sada ID (FR-049)

| ID | Rozlišuje | Formát |
|----|-----------|--------|
| `img.player.idle` | Alzák stojící | PNG RGBA 64×96 |
| `img.player.run` | Alzák v pohybu | PNG RGBA 64×96 |
| `img.player.air` | Alzák ve vzduchu | PNG RGBA 64×96 |
| `img.player.hurt` | Alzák v nezranitelnosti | PNG RGBA 64×96 |
| `img.enemy.walk` | protivník | PNG RGBA 72×72 |
| `img.enemy.hit` | protivník zasažený | PNG RGBA 72×72 |
| `img.platform.pobocka` | plošina pobočky | PNG RGBA dlaždice 64×64 |
| `img.platform.sklad` | plošina skladu | PNG RGBA dlaždice 64×64 |
| `img.platform.kancelar` | plošina kanceláře | PNG RGBA dlaždice 64×64 |
| `img.pit` | propast | PNG RGBA dlaždice 64×64 |
| `img.exit.inactive` | **neaktivní** východ | PNG RGBA 120×160 |
| `img.exit.active` | **aktivní** východ, jasně odlišný | PNG RGBA 120×160 |
| `img.bg.pobocka` | pozadí pobočky | PNG RGB 1920×1080 |
| `img.bg.sklad` | pozadí skladu | PNG RGB 1920×1080 |
| `img.bg.kancelar` | pozadí kanceláře | PNG RGB 1920×1080 |
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

Načítání je líné a cachované podle ID; jeden soubor se nikdy nenačte dvakrát.

## Generátor (FR-082, SC-017)

`tools/generate_placeholders.py`:

- používá **výhradně standardní knihovnu** (`zlib`, `struct`, `wave`, `hashlib`);
- prochází položky v pevném zapsaném pořadí;
- žádný `random` bez pevného seed, žádný časový údaj v metadatech;
- přepíše soubory v `assets/` a aktualizuje `sha256` v manifestu;
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
