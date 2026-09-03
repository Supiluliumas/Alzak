# Phase 0 — Research: Alzák tech demo

**Feature**: `001-alzak-platformer-demo` | **Date**: 2026-09-03 | **Plan**: [plan.md](./plan.md)

Účel: uzavřít každou technickou neznámou plánu dřív, než vznikne `tasks.md`.
Formát každé položky: **Decision · Rationale · Alternatives considered**.

**Stav NEEDS CLARIFICATION**: žádná otevřená. Všechny produktové otázky uzavřel
`clarify` a OD-006; technické otázky uzavírá tento dokument.

**Změna rozsahu OD-007**: R9–R11 jsou ponechány pouze jako historický záznam
zvažovaného návrhu. Nejsou aktivním rozhodnutím a nesmějí se implementovat.

---

## R1 — Herní smyčka a pevný časový krok

**Decision**: Vykreslování běží na cílených 60 FPS (`pygame.time.Clock.tick(60)`).
Simulace běží odděleně na **pevném kroku `SIM_DT = 1/120 s`** s akumulátorem:

```text
accumulator += min(real_delta, MAX_FRAME_TIME)   # MAX_FRAME_TIME = 0.25 s
while accumulator >= SIM_DT:
    simulate(SIM_DT)
    accumulator -= SIM_DT
render()
```

Simulace **nikdy** nedostane proměnlivé `dt`. Vykreslování stav neinterpoluje —
pro statickou kameru a 60 FPS je rozdíl neviditelný a interpolace by přidala
vrstvu, kterou Princip I nechce.

**Rationale**: SC-003 vyžaduje shodnou výšku skoku, dolet a dobu přehřátí
v mezích 5 % při kolísání 30–60 FPS. Pevný krok to garantuje **exaktně**, ne
v mezích. Zároveň činí simulaci volatelnou v testu bez okna (Princip V) — test
prostě zavolá `simulate(SIM_DT)` N-krát. `MAX_FRAME_TIME` brání spirále smrti
po dlouhém zamrznutí (např. přetažení okna).

Volba 1/120 místo 1/60: při `MAX_FALL_SPEED = 1500 px/s` urazí hráč za krok
12,5 px, což s minimální tloušťkou plošiny 32 px vylučuje tunelování bez potřeby
swept collision (viz R3, RP-05).

**Alternatives considered**:
- *Proměnlivé `dt` přímo do fyziky*: nejjednodušší, ale SC-003 by prošlo jen
  náhodou a testy by musely simulovat čas. Zamítnuto.
- *Pevný krok 1/60*: méně kroků, ale 25 px za krok při maximálním pádu →
  buď tlusté plošiny, nebo swept collision. Zamítnuto jako méně robustní.
- *Pevný krok + interpolace vykreslení*: korektní, ale přidává druhou kopii
  stavu a míchá prezentaci do simulace. Zamítnuto podle Principu I.

---

## R2 — Prezentační vrstva a škálování (Princip VII, FR-002, SC-019)

**Decision**: Herní kód kreslí **výhradně** do `pygame.Surface((1920, 1080))`.
`render/presentation.py` drží okno a při každém snímku:

1. spočítá `scale = min(win_w / 1920, win_h / 1080)` — bez horní i dolní meze,
   takže škáluje **zmenšením i zvětšením**;
2. `dst = (round(1920*scale), round(1080*scale))`;
3. `offset = ((win_w - dst_w) // 2, (win_h - dst_h) // 2)`;
4. vyplní okno černou, `smoothscale` logický surface na `dst`, blit na `offset`.

Je to **jediné** místo v celém kódu, které volá `display.get_surface().get_size()`.
`presentation.to_logical(px, py)` existuje pro případný debug, herní logika ji nepoužívá.

F11 přepíná `pygame.display.set_mode(size)` ↔ `set_mode(size, pygame.FULLSCREEN)`
a nemění nic jiného; logický surface zůstává stejný objekt, takže rozmístění je
z definice nezměněné (US4 scénář 4).

**Rationale**: Přesně splňuje Princip VII i OD-005 (letterbox i pillarbox, oba
směry). Testovatelné bez okna: funkce výpočtu `scale`/`offset` je čistá a dá se
otestovat na vstupech 1280×720, 3840×2160, 2560×1080 (ultrawide) a 1600×1200 (4:3).

**Alternatives considered**:
- *`pygame.SCALED` flag*: pygame-ce to umí, ale chování napříč platformami a
  fullscreenem je méně předvídatelné a testovat výpočet nelze bez okna. Zamítnuto.
- *Kreslit rovnou do okna a přepočítávat souřadnice*: přímé porušení Principu VII.
  Zamítnuto.
- *`scale` zaokrouhlený na celé číslo (pixel-perfect)*: hezčí u pixel-artu, ale
  na 1920×1080 logice by na 2560×1440 dalo scale 1 a obrovský rám. Zamítnuto proti SC-019.

---

## R3 — Kolize a fyzika (FR-011…FR-018, FR-017)

**Decision**: Osově zarovnané obdélníky (AABB) v `float` souřadnicích. Pohyb se
řeší **po osách zvlášť**, v pořadí X → resolve X → Y → resolve Y. Plošiny jsou
plné obdélníky (ne one-way). Řešení kolize posune entitu na hranu a vynuluje
příslušnou složku rychlosti.

`on_ground` je pravdivé právě tehdy, když v tomto kroku došlo k řešení kolize
zdola. Z toho se odvozuje coyote timer (`COYOTE_TIME = 0.10 s`) i zvuk pohybu.
Jump buffer (`JUMP_BUFFER = 0.12 s`) je timer nastavený stiskem mezerníku a
spotřebovaný v okamžiku, kdy je skok možný.

Proměnlivá výška skoku: uvolnění mezerníku při stoupání násobí `vy` hodnotou
`JUMP_CUT_MULTIPLIER = 0.45`.

Schéma prostředí **vynucuje** `platform.h >= MIN_PLATFORM_THICKNESS` (32 px),
což při `MAX_FALL_SPEED = 1500 px/s` a `SIM_DT = 1/120 s` (12,5 px/krok)
vylučuje tunelování.

**Rationale**: Nejjednodušší přístup, který splní FR-017 („bez propadání,
zasekávání a chvění"). Osové řešení je standard pro 2D plošinovky a je snadno
jednotkově testovatelné: vstup = pozice + rychlost + seznam obdélníků,
výstup = pozice + rychlost + kolizní příznaky. Žádný pygame typ.

**Alternatives considered**:
- *Swept AABB / continuous collision*: robustnější, ale složitější a při
  garantované tloušťce plošin zbytečné. Zamítnuto podle Principu I.
- *`pygame.Rect` jako nositel pozice*: `Rect` je celočíselný, což by při
  akceleraci způsobilo trhavý pohyb. Pozice je proto `float`, `Rect` vzniká až
  při vykreslení. Zamítnuto jako nositel stavu.
- *One-way plošiny (průchod zdola)*: scope je nepožaduje. Zamítnuto (Princip I).

---

## R4 — Geometrie a kolize laseru (FR-027, FR-028, FR-085…FR-087)

**Decision**: Laser je **vodorovný obdélník** vzniklý z muzzle bodu:

```text
muzzle_x = player.x + (MUZZLE_OFFSET.x if facing_right else player.w - MUZZLE_OFFSET.x)
muzzle_y = player.y + MUZZLE_OFFSET.y
beam = rect(x = muzzle_x .. end_x, y = muzzle_y - THICKNESS/2, h = THICKNESS)
```

`THICKNESS = LASER["collision_thickness"] = 16` (FR-086).
`end_x` se určí takto: z kandidátů — všechny plošiny a živý protivník, které
protínají vodorovný pás `[muzzle_y ± THICKNESS/2]` a leží ve směru pohledu —
se vybere ten s **nejmenší vzdáleností** od `muzzle_x`. Není-li žádný, končí
paprsek na hraně obrazovky (0 nebo 1920).

Zasáhne-li paprsek nejdřív plošinu, protivník poškození nedostává (US1 scénář 7).
Poškození za krok = `LASER["dps"] * SIM_DT`, akumulované v `enemy.hp` — nikdy se
neresetuje mimo restart prostředí (FR-039, SC-020).

Vzhled (tloušťka jádra, tloušťka záře, barvy, případné blikání) je oddělená sada
klíčů v `config.LASER` a **nemá vliv na kolizi** — kolizní tloušťka je jediná,
která rozhoduje o zásahu.

**Rationale**: Vodorovný pás je přesně to, co spec žádá, a je triviálně
testovatelný bez vykreslení: funkce `resolve_beam(muzzle, facing, platforms, enemy)`
vrací `(end_x, hit_target)`. Oddělení kolizní a vykreslovací tloušťky brání tomu,
aby vizuální ladění tiše změnilo pravidla hry.

**Alternatives considered**:
- *Paprsek o tloušťce 1 px (čára)*: uzavřeno OD-006 — nespolehlivé vůči
  pohybujícímu se protivníkovi a citlivé na zaokrouhlení. Zamítnuto.
- *Muzzle odvozený z rozměrů sprite za běhu*: zamítnuto v OD-006 — vázalo by
  herní geometrii na placeholderový asset a porušilo Princip IV.
- *Poškození „za zásah" místo „za sekundu"*: SC-004 a SC-020 mluví o čase
  působení. DPS × dt je jediná formulace, která projde oběma. Zamítnuto.

---

## R5 — Validace JSON prostředí bez závislostí (Princip III, FR-084, SC-018)

**Decision**: Vlastní deklarativní validátor ve `data/schema.py` — asi 120 řádků,
jen stdlib. Schéma je Python struktura popisující pole, typ, povinnost a rozsah;
`contracts/level.schema.json` je jeho **dokumentační zrcadlo** (JSON Schema
draft-07) pro lidi a nástroje, hra jej za běhu nepoužívá.

Chyba vyhodí `LevelDataError(file: str, field: str, reason: str)`. `app.py` ji
chytá na nejvyšší úrovni a:

1. zobrazí `screens/error_screen.py` — název souboru, cesta k poli, důvod;
   ovladatelná klávesnicí (Esc/Enter zavře);
2. zapíše tutéž zprávu na `sys.stderr`;
3. ukončí proces `sys.exit(2)`.

Validují se i sémantické invarianty, ne jen typy: startovní pozice není v propasti,
trasa protivníka leží nad existující plošinou, východ se nepřekrývá s propastí,
tloušťka plošiny ≥ `MIN_PLATFORM_THICKNESS`, všechna `asset_id` existují v manifestu.

**Rationale**: `jsonschema` je runtime závislost — Technology Constraints ji
zakazují. Vlastní validátor je navíc jediný způsob, jak dát chybě tvar
„soubor + pole + důvod", který spec výslovně žádá; `jsonschema` hlásí cestu jinak.
Sémantické kontroly by stejně musely být vlastní.

**Alternatives considered**:
- *`jsonschema` jako runtime závislost*: porušuje Technology Constraints. Zamítnuto.
- *`dataclasses` + `__post_init__`*: čitelné, ale chybová hláška by vznikala
  z `TypeError` a nešla by spolehlivě mapovat na jméno pole. Zamítnuto.
- *Bez validace, spolehnout se na správná data*: přímé porušení Principu III. Zamítnuto.

---

## R6 — Registr assetů a cesty k prostředkům (Princip IV, FR-050, SC-012)

**Decision**: `assets/manifest.json` mapuje **stabilní ID** (např. `img.player.idle`,
`sfx.laser.loop`) na relativní cestu. `assets/registry.py` manifest načte jednou,
soubory načítá líně a cachuje podle ID. Herní kód volá výhradně
`registry.image("img.enemy.walk")` / `registry.sound("sfx.jump")` — **nikdy** cestu.

Kořen prostředků řeší `paths.py`:

```text
if getattr(sys, "frozen", False):  base = Path(sys._MEIPASS)
else:                              base = Path(__file__).parents[2]   # repo root
ASSETS = base / "assets";  LEVELS = base / "levels"
```

Chybějící ID → tvrdá chyba při startu (validace manifestu proti seznamu
požadovaných ID), ne tichý fallback. Chybějící *soubor* při vývoji → registr
vrátí zřetelný růžový placeholder surface a zapíše varování; hra kvůli tomu
nespadne, ale test manifestu selže.

**Rationale**: SC-012 („nahrazení obrázku souborem stejného identifikátoru se
projeví bez změny herní logiky") je splněno z definice. Rozdíl mezi „chybí ID"
(tvrdá chyba) a „chybí soubor" (viditelný placeholder) drží vývoj plynulý,
aniž by chyba prošla do CI.

**Alternatives considered**:
- *Assety uvnitř `src/alzak/assets/`*: mísí kód a data, komplikuje `MANIFEST.in`
  i přehled v Gitu. Zamítnuto.
- *Automatický scan adresáře místo manifestu*: ID by pak bylo jméno souboru,
  takže přejmenování by tiše rozbilo hru. Zamítnuto proti FR-050.

---

## R7 — Headless běh testů (Princip V, FR-062, SC-009)

**Decision**: `tests/conftest.py` nastaví **před** jakýmkoli importem pygame:

```text
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
```

Většina testů (`tests/unit/`) pygame **vůbec neimportuje** — testují `sim/`,
`data/`, `core/`. Test `test_sim_is_display_free` staticky ověří, že žádný modul
pod `src/alzak/sim/` neobsahuje import `pygame.display`, `pygame.mixer` ani
`pygame.font` (parsování AST, ne regex).

`audio/mixer.py` obalí `pygame.mixer.init()` do `try/except pygame.error` a při
selhání přepne do režimu „no audio": všechna volání jsou no-op, hra běží dál
(Edge Case „zvukové zařízení není k dispozici").

**Rationale**: SC-009 žádá průchod headless na Linuxu, Windows i macOS. Dummy
drivery jsou standardní a nevyžadují X server. Statický import test je levná
pojistka, že Princip V nezmizí při pozdější úpravě.

**Alternatives considered**:
- *`xvfb` v CI*: funguje na Linuxu, ne na Windows a macOS runnerech. Zamítnuto.
- *Mockovat pygame*: křehké a testuje mock, ne kód. Zamítnuto.

---

## R8 — Deterministický generátor placeholderů (FR-082, SC-017)

**Decision**: `tools/generate_placeholders.py` používá **výhradně standardní
knihovnu** — žádný pygame, žádný Pillow:

- **Obrázky**: vlastní PNG zapisovač nad `zlib` + `struct`. 8bit RGBA,
  `zlib.compress(data, level=9)`, filtr 0 na každém řádku, žádný `tEXt`,
  žádný časový chunk. Výstup je bajtově determinovaný vstupem.
- **Zvuky a hudba**: modul `wave`, PCM 16 bit, mono, 22 050 Hz. Tóny se počítají
  z pevného seed a pevné notové osnovy; žádný `random` bez seed, žádný čas.
- **Řazení**: generátor prochází seznam položek v pevném, explicitně zapsaném
  pořadí; nikdy nespoléhá na pořadí `os.listdir` ani na iteraci nesetříděného dictu.

Ověření SC-017: generátor má **režim `--verify`**, který nic nezapisuje — spočítá
SHA-256 všech souborů v `assets/`, znovu je vygeneruje do dočasného adresáře a
porovná. Volá jej test `tests/unit/test_placeholder_determinism.py` (T035) i CI
job `test` (T092). Manifest nese checksum každého souboru, takže rozdíl je vidět
i v diffu. Samostatný skript `verify_placeholders.py` **nevzniká** — jeden nástroj
se dvěma režimy stačí (Princip I).

Hra generátor **nikdy nevolá** (FR-081). Není v žádném build ani CI kroku jako
povinnost; CI ho smí spustit pouze ve verifikačním režimu, který nic nepřepisuje.

**Rationale**: Bajtová shoda (SC-017) je nesplnitelná, pokud výstup prochází
knihovnou, jejíž verze může změnit kompresi nebo metadata. Vlastní PNG zapisovač
je ~60 řádků a dává plnou kontrolu. `wave` z stdlib je stabilní formát bez metadat.

**Alternatives considered**:
- *`pygame.image.save`*: pohodlné, ale bajtový výstup závisí na verzi SDL_image;
  SC-017 by bylo mimo naši kontrolu. Zamítnuto.
- *Pillow*: nová závislost (byť vývojová) a stejný problém s verzemi. Zamítnuto.
- *OGG pro hudbu*: menší soubor, ale stdlib enkodér neexistuje. WAV mono 22 kHz
  je pro placeholder dostatečné. Zamítnuto.

**Vlastník**: **Codex** (OD-004). Tento výzkum stanoví jen mantinely.

---

## R9 — VYŘAZENO OD-007: strukturální vyloučení feedback vrstvy

**Decision**: Feedback kód žije v top-level balíčku `alzak_devtools/`, tedy
**mimo** `src/alzak/`. Napojení na hru je jediné místo:

```text
# src/alzak/app.py — jediný dotyk na feedback vrstvu
FEEDBACK = None
if config.FEEDBACK["enabled"]:
    try:    from alzak_devtools.feedback import overlay as FEEDBACK
    except ImportError:  FEEDBACK = None      # produkční build: balíček neexistuje
```

`packaging/alzak.spec` balíček nikdy nezahrne (není v `pathex`, je v `excludes`).
Test `tests/devtools/test_production_exclusion.py` ověří dvě věci:
`importlib.util.find_spec("alzak_devtools") is None` v prostředí simulujícím
produkční balíček, a že v `alzak.spec` je `alzak_devtools` uveden v `excludes`.

`config.FEEDBACK["enabled"]` je odvozeno z `not getattr(sys, "frozen", False)`
plus přepínatelné proměnnou prostředí pro výslovně označený test build.

**Rationale**: §21.2 žádá vyloučení **strukturální, testovatelné a zdokumentované**
a výslovně říká, že runtime příznak nestačí. Oddělený balíček splní všechny tři:
neexistuje-li adresář v balíčku, žádný příznak jej nezapne.

**Alternatives considered**:
- *`if DEBUG:` uvnitř `src/alzak/`*: kód by v balíčku zůstal — §21.2 zamítá.
- *Odstranění souborů build skriptem*: křehké, neověřitelné, a diff by šel proti
  Git policy. Zamítnuto.

---

## R10 — VYŘAZENO OD-007: snímek herní plochy bez ovládacího prvku

**Decision**: Feedback overlay kreslí svůj indikátor a editor **až po** tom, co
si vyžádá kopii logického surface:

```text
frame = presentation.logical_surface.copy()   # před kresbou overlay
```

Uloží se z této kopie. Ověření není architektonické, ale **proti souboru**:
E2E test vykreslí do rohu známý „marker" barvy indikátoru, pořídí snímek a
zkontroluje, že v uloženém PNG na dané pozici marker **není**.

Selže-li pořízení snímku, položka se uloží s příznakem `screenshot: "unavailable"`
a bez obrazového souboru — nikdy s prázdným nebo zastaralým obrázkem (Edge Case).

**Rationale**: §21.3/§21.4 žádá důkaz proti skutečnému souboru, ne úvahu o
vrstvách. Kopie logického surface je jediné místo, kde overlay ještě neexistuje.

**Alternatives considered**:
- *Skrýt overlay na jeden snímek a zachytit okno*: závodní podmínka a závislost
  na snímkování okna. Zamítnuto.
- *Zachytit celou obrazovku OS*: §21.8/§21.23 zakazují zachytávat obsah jiných
  aplikací. Zamítnuto.

---

## R11 — VYŘAZENO OD-007: balíček zpětné vazby

**Decision**:
- **ID**: `FB-<YYYYMMDD>-<uuid4().hex[:12]>`, kde datum je **UTC** (§21.8).
  ID se generuje jednou při `capturing` a od té chvíle se nikdy nemění.
- **Struktura**: `feedback-store/inbox/<ID>/` s `item.json` (kontext, stav,
  odpovědi, historie), `screenshot_original.png`, `screenshot_annotated.png`,
  `annotations.json` (normalizované souřadnice 0–1), `checksums.json` (SHA-256
  každé přílohy) a `manifest.json` (seznam příloh + verze schématu).
- **Atomická publikace**: zapisuje se do `feedback-store/.staging/<ID>/`, po
  dokončení `os.replace(staging, inbox/<ID>)` — na stejném svazku atomické.
  Přerušení procesu uprostřed nechá nedokončený adresář ve `.staging/`, odkud
  jej `doctor` přesune do `quarantine/` s výslovnou chybou.
- **Deduplikace**: primárně podle ID; `pull` je idempotentní — existující
  `inbox/<ID>` se nepřepisuje a původní přílohy se nikdy nemění (SC-016).
- **Immutable evidence**: `screenshot_original.png` a `annotations.json` se po
  publikaci nikdy nepřepisují; nové odpovědi jdou do `item.json` → `responses[]`.

**Rationale**: Přesně kanonické prvky §21.8/§21.9/§21.11, které se podle §21.28
nesmí předefinovávat. `os.replace` je jediné atomické primitivum dostupné ve
stdlib napříč Windows i macOS.

**Alternatives considered**:
- *SQLite index fronty*: rychlejší dotazy, ale zavádí stav mimo soubory a
  komplikuje `verify`. Pro bootstrap minimum zbytečné. Zamítnuto.
- *Datum v ID z lokálního času*: §21.8 žádá UTC. Zamítnuto.

---

## R12 — Distribuce, PyInstaller a GitHub Actions (FR-063…FR-065, SC-010, SC-011)

**Decision**:
- **PyInstaller**, jeden sdílený `packaging/alzak.spec` pro obě platformy.
  `datas` zahrnuje `assets/` a `levels/`; `excludes` obsahuje `pytest` a
  `PyInstaller`. macOS používá **onedir**; Windows používá dle OD-009
  **onefile**, aby dodávkou byl jediný `Alzak.exe`.
- **Lokální buildy**: `packaging/build_windows.ps1`, `packaging/build_macos.sh`;
  oba jen ověří prostředí a zavolají `pyinstaller packaging/alzak.spec`.
- **CI** (`.github/workflows/ci.yml`), jeden běh, čtyři joby:

  | job | runner | výstup |
  |-----|--------|--------|
  | `test` | `ubuntu-latest` | headless `pytest` (brána pro build joby) |
  | `build-windows` | `windows-latest` | artefakt `alzak-windows-x64` |
  | `build-macos-arm` | `macos-15` | artefakt `alzak-macos-arm64` |
  | `build-macos-intel` | `macos-15-intel` | artefakt `alzak-macos-x86_64` |

  Build joby mají `needs: test`, takže artefakt nikdy nevznikne z červené sady.
  Testy se pro jistotu spouští i na všech třech build runnerech (SC-009).
- **Onedir vs onefile**: macOS onedir kvůli rychlému startu; Windows onefile na
  výslovný požadavek zadavatele. Windows Defender může u nepodepsaného souboru
  zobrazit varování — A-009 to nezmírňuje ani neobchází.

**Rationale**: Tři artefakty z jednoho běhu (SC-010) vyžadují tři runnery —
PyInstaller nekříží architektury. `macos-13` je poslední x86_64 runner GitHubu,
`macos-14` je arm64.

**Alternatives considered**:
- *Universal2 binárka z jednoho macOS jobu*: vyžaduje universal2 kolečka
  `pygame-ce`, jejichž dostupnost není zaručená. FR-064 navíc žádá dva
  **oddělené** macOS artefakty. Zamítnuto.
- *Nuitka / cx_Freeze*: Technology Constraints určují PyInstaller. Zamítnuto.

---

## R13 — Sémantika pauzy, přechodů a zvuku laseru (FR-009, FR-048, FR-060)

**Decision**: Obrazovky jsou stavový automat s explicitními stavy
`TITLE · PLAY · PAUSE · TRANSITION · GAMEOVER · FINISH · ERROR`.
Simulace se posouvá **pouze** ve stavu `PLAY`. Pauza nemění stav simulace, jen
ji přestane volat — po `Pokračovat` pokračuje přesně z místa zastavení.

Přechod (`TRANSITION`) má vlastní časovač mimo simulaci; Escape během něj se
**zapamatuje a uplatní až po jeho dokončení** (Edge Case). Akumulátor pevného
kroku se při vstupu do `PAUSE` i `TRANSITION` **vynuluje**, aby se po návratu
nedohnalo více kroků najednou.

Zvuk trvání laseru je jediný smyčkový kanál. Ukončí se okamžitě při: uvolnění X,
přehřátí, pauze, vstupu do východu a jakékoli změně stavu automatu — vše přes
jediný hook `on_state_exit(PLAY)` a `laser.on_deactivate()`, aby nešlo zapomenout
na jednu cestu (FR-060).

**Rationale**: Jediný stavový automat s explicitním „simulace běží jen v PLAY"
uzavírá všechny hraniční případy spec na jednom místě, ne rozptýlenými
podmínkami. Vynulování akumulátoru brání skoku po dlouhé pauze.

**Alternatives considered**:
- *Pauza jako příznak uvnitř simulace*: rozlévá prezentační stav do `sim/` a
  porušuje Princip V. Zamítnuto.
- *Zastavení zvuku v každé obrazovce zvlášť*: přesně to, co FR-060 hlídá.
  Zamítnuto.

---

## R14 — České texty a font (A-004, RP-01)

**Decision**: Veškeré vykreslování textu jde přes `render/text.py`, které má
**jediné** místo výběru fontu. Pořadí:

1. přibalený TTF z `assets/fonts/` podle manifestu (ID `font.ui`), pokud existuje;
2. jinak `pygame.font.Font(None, size)` (vestavěný `freesansbold.ttf`).

Test `test_czech_glyphs` vykreslí řetězec `„ěščřžýáíéúůďťňĚŠČŘŽ"` a ověří, že
žádný znak nevykreslil `.notdef` (porovnáním šířky a bitmapy proti známému
`.notdef` glyfu). Selže-li test s vestavěným fontem, je nutné přibalit font —
což je **assetová práce → Codex** (OD-004).

**Rationale**: A-004 určuje češtinu; nečitelná diakritika by byla viditelná vada
prezentace. Jediné místo výběru fontu znamená, že případná výměna je jednořádková.

**Alternatives considered**:
- *`pygame.font.SysFont("arial", …)*: závislé na systémových fontech, na CI
  runnerech nespolehlivé, nedeterministické napříč platformami. Zamítnuto.
- *Odstranit diakritiku z textů*: porušuje A-004. Zamítnuto.

---

## R15 — Výchozí sada laditelných hodnot

**Decision**: Plán dodává výchozí hodnoty (viz `data-model.md`, sekce
Konfigurace), které jsou **odhad k doladění**, ne požadavek. Musí od začátku
splňovat měřitelná kritéria SC-004…SC-007 a SC-021; jinak jsou volné.
Doladění patří do fáze P9 na základě ručního testu.

**Rationale**: Codex potřebuje spustitelné hodnoty hned; Princip II zaručuje,
že jejich změna je jednořádková a nevyžaduje zásah do logiky.

**Alternatives considered**:
- *Nechat hodnoty na implementaci*: Codex by je vymyslel a rozhodnutí by
  neexistovalo v repozitáři. Zamítnuto podle `CLAUDE.md` §16.

---

## Shrnutí

| ID | Téma | Stav |
|----|------|------|
| R1 | Pevný krok 1/120 s + akumulátor | rozhodnuto |
| R2 | Prezentační škálování, jediné místo | rozhodnuto |
| R3 | AABB po osách, min. tloušťka plošiny 32 px | rozhodnuto |
| R4 | Laser: muzzle → vodorovný pás 16 px → nejbližší zásah | rozhodnuto |
| R5 | Vlastní validátor schématu, stdlib | rozhodnuto |
| R6 | Registr stabilních ID + `paths.py` pro frozen build | rozhodnuto |
| R7 | SDL dummy drivery + statický import test | rozhodnuto |
| R8 | Generátor jen ze stdlib, bajtová shoda | rozhodnuto (vlastník Codex) |
| R9 | feedback balíček | **vyřazeno OD-007** |
| R10 | feedback snímek | **vyřazeno OD-007** |
| R11 | feedback úložiště | **vyřazeno OD-007** |
| R12 | PyInstaller: Windows onefile, macOS onedir, 4 CI joby, 3 artefakty | rozhodnuto (OD-009) |
| R13 | Stavový automat, simulace jen v PLAY | rozhodnuto |
| R14 | Jediné místo výběru fontu + test glyfů | rozhodnuto |
| R15 | Výchozí laditelné hodnoty jako startovní sada | rozhodnuto |

**Žádná NEEDS CLARIFICATION nezůstala otevřená.**
