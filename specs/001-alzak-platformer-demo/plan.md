# Implementation Plan: Alzák — technologické demo 2D plošinovky

**Branch**: `001-alzak-platformer-demo` | **Date**: 2026-09-03 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-alzak-platformer-demo/spec.md`

**Governing**: `.specify/memory/constitution.md` v1.1.1 · `AGENTS.md` · `CLAUDE.md` ·
`feedback_pipeline_standalone.md` · rozhodnutí v [open-decisions.md](./open-decisions.md)

**Precedence**: dle `spec.md` A-011 — scope zadavatele má autoritu 1, tento plán
autoritu 6. Rozsah US6 se řídí A-012 a OD-001.

**Role**: Tento plán a všechny navazující artefakty (`research.md`, `data-model.md`,
`contracts/`, `quickstart.md`, `checklists/`, `tasks.md`) vytváří Claude.
**Implementaci provádí Codex** — plán je předávacím bodem, ne implementačním deníkem.

---

## Summary

Postavit samostatně spustitelné technologické demo 2D plošinovky v Pythonu 3.12
a pygame-ce: tři datově popsaná prostředí, hráč s laditelným pohybem, souvislý
laser s přehříváním, jeden typ hlídkujícího protivníka, kompletní obrazovky,
zvuk, headless testovatelná simulace, lokální i CI buildy pro Windows a macOS a
minimální vývojářský feedback pipeline.

Technický přístup stojí na pěti pilířích, které přímo vycházejí z principů ústavy:

1. **Čistá simulační vrstva bez pygame displeje** (`src/alzak/sim/`) běžící na
   **pevném časovém kroku** s akumulátorem. Fyzika, energie, laser, protivník a
   postup prostředími jsou volatelné bez okna a bez zvuku → Princip V, FR-062, SC-009.
2. **Jediná centrální konfigurace** `src/alzak/config.py` obsahující *každou*
   laditelnou hodnotu včetně geometrie a vzhledu laseru → Princip II, FR-019,
   FR-034, FR-085…FR-087.
3. **Logický prostor 1920 × 1080 jako jediný souřadnicový systém.** Herní kód
   kreslí do logického `Surface`; prezentační vrstva jej jedním krokem škáluje
   na okno se zachováním 16:9 a doplní letterbox/pillarbox → Princip VII, FR-001,
   FR-002, SC-019.
4. **Data-driven prostředí**: tři JSON soubory se společným schématem, jeden
   loader se striktní validací a chybovou obrazovkou uvnitř aplikace → Princip III,
   FR-046, FR-047, FR-084, SC-008, SC-018.
5. **Assety výhradně přes registr stabilních ID**; placeholdery jsou verzované
   soubory vyrobené deterministickým generátorem ze standardní knihovny →
   Princip IV, FR-049, FR-050, FR-081, FR-082, SC-012, SC-017.

Feedback vrstva (US6, P6) žije v **samostatném top-level balíčku mimo `src/alzak/`**,
takže její vyloučení z produkčního buildu je strukturální a testovatelné, ne jen
runtime příznak → FR-066, SC-014.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: `pygame-ce` — **jediná runtime závislost**.
Vývojové (nikdy v produkčním balíčku): `pytest`, `PyInstaller`.
Feedback vrstva podle A-013 nesmí přidat runtime závislost; její potřeby
(PNG zápis, checksumy, JSON, WAV) pokrývá standardní knihovna.

**Storage**: soubory na disku. Prostředí = `levels/*.json`; assety = `assets/`
+ `assets/manifest.json`; feedback = repo-local `feedback-store/`
(`inbox/`, `archive/`, `quarantine/`), gitignorováno dle A-014. Žádná databáze,
žádné ukládání postupu (A-007).

**Testing**: `pytest`. Simulační testy běží bez pygame displeje.
Testy dotýkající se pygame běží headless přes `SDL_VIDEODRIVER=dummy` a
`SDL_AUDIODRIVER=dummy` nastavené v `tests/conftest.py` **před** importem pygame.

**Target Platform**: desktop — Windows x64, macOS Apple Silicon (arm64),
macOS Intel (x86_64). Linux je cílem pouze pro běh testů v CI, ne pro distribuci.

**Project Type**: single-project desktop application (`src/` layout).

**Performance Goals**: 60 FPS vykreslování; simulace na pevném kroku
`SIM_DT = 1/120 s` s akumulátorem, takže výška skoku, dolet i časovače jsou
nezávislé na FPS (SC-002, SC-003).

**Constraints**:
- Herní logika nikdy nečte skutečné rozlišení okna (Princip VII).
- Žádné číselné herní konstanty mimo `config.py` a JSON dat prostředí (Princip II).
- Žádná runtime závislost mimo `pygame-ce` (Technology Constraints).
- Hra nikdy negeneruje assety za běhu (FR-081).
- Produkční build neobsahuje feedback modul (FR-066).
- Buildy jsou nepodepsané (A-009).

**Scale/Scope**: 3 prostředí · 1 typ protivníka · 6 obrazovek (úvodní, hra, pauza,
neúspěch, závěrečná, chybová) + přechod · 5 zvukových efektů + 1 hudební smyčka ·
~11 tříd placeholderových obrázků · 88 funkčních požadavků · 22 kritérií úspěchu.

---

## Constitution Check

*GATE: musí projít před Phase 0 a znovu po Phase 1.*

| # | Princip | Jak jej návrh plní | Kde se to ověří |
|---|---------|--------------------|-----------------|
| I | Scope-First, Demo-Scale (NON-NEGOTIABLE) | Žádná vrstva navíc: jeden proces, jeden balíček, žádné ECS, žádný plugin systém, žádné abstrakce „do budoucna". Feedback vrstva je v rozsahu jen proto, že ji nařizuje OD-001. Vyloučené věci (checkpointy, více typů protivníků, scrollující kamera, ukládání, nastavení ovládání, lokalizace, podepisování, procedurální generování) v plánu nikde nefigurují. | `checklists/`, `analyze` |
| II | Centrální konfigurace (NON-NEGOTIABLE) | Jediný modul `src/alzak/config.py` se skupinami `DISPLAY`, `SIM`, `PLAYER`, `JUMP`, `ENERGY`, `LASER`, `ENEMY`, `LEVEL`, `HUD`, `AUDIO`, `FEEDBACK`. Geometrie i vzhled laseru (muzzle offset, kolizní tloušťka 16 px, tloušťky a barvy vykreslení) jsou zde — FR-085…FR-087. Rozměry a pozice konkrétního prostředí jsou naopak v JSON. | test `test_no_magic_numbers` + code review |
| III | Data-Driven prostředí | `data/schema.py` (deklarativní popis) + `data/loader.py` (jeden loader pro všechny tři soubory). Chyba → `LevelDataError(file, field, reason)` → chybová obrazovka + stderr + nenulový exit kód. | SC-008, SC-018 |
| IV | Oddělené vrstvy a nahraditelné assety | Balíčky `app` · `config` · `core` · `sim` · `data` · `render` · `screens` · `audio` · `assets`. Herní pravidla nikdy nesahají na cestu k souboru; jen na stabilní ID z `assets/manifest.json`. | SC-012 |
| V | Deterministická, testovatelná simulace (NON-NEGOTIABLE) | `src/alzak/sim/` neimportuje `pygame.display`, `pygame.mixer` ani `pygame.font`. Vstup přichází jako `InputSnapshot` (čisté booly), výstup je stav + seznam událostí. Pevný krok + akumulátor v `core/clock.py`. | SC-003, SC-009, import test |
| VI | Test po každé funkci (NON-NEGOTIABLE) | `tasks.md` má testovací úkol u každé funkční skupiny a checkpoint „spusť celou sadu" na konci každé fáze. Pro feedback vrstvu platí zúžený rozsah dle OD-001 bodu 2. | `tasks.md`, checkpointy |
| VII | 1920×1080 jako jediný souřadnicový systém | `render/presentation.py` je **jediné** místo, které zná velikost okna. Vše ostatní kreslí do logického `Surface` 1920×1080. Škáluje se oběma směry, poměr 16:9, letterbox i pillarbox. | SC-019 |

**Technology Constraints**: Python 3.12 ✓ · pygame-ce ✓ · pytest ✓ · PyInstaller ✓ ·
JSON ✓ · GitHub Actions ✓ · žádná runtime závislost navíc ✓.

**Výsledek brány (před Phase 0)**: **PROŠLA**, bez porušení a bez potřeby
zápisu do Complexity Tracking.

**Výsledek brány (po Phase 1)**: **PROŠLA** — viz sekce „Post-Design Constitution
Re-Check" níže.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-alzak-platformer-demo/
├── spec.md                  # hotovo (specify + clarify + OD-006)
├── open-decisions.md        # hotovo, OD-001…OD-006
├── analysis-report.md       # hotovo (audit MD ↔ artefakty)
├── plan.md                  # tento soubor
├── research.md              # Phase 0
├── data-model.md            # Phase 1
├── quickstart.md            # Phase 1
├── contracts/               # Phase 1
│   ├── level.schema.json
│   ├── level-format.md
│   ├── asset-manifest.md
│   ├── input-map.md
│   ├── feedback-package.md
│   ├── feedbackctl.md
│   └── build-and-ci.md
├── checklists/              # fáze checklist
└── tasks.md                 # fáze tasks
```

### Source Code (repository root)

```text
src/alzak/
├── __init__.py              # __version__
├── __main__.py              # `python -m alzak`
├── app.py                   # okno, hlavní smyčka, pevný krok, přepínání obrazovek
├── config.py                # VŠECHNY laditelné hodnoty (Princip II)
├── paths.py                 # kořen prostředků: zdroj vs. PyInstaller (sys._MEIPASS)
├── core/
│   ├── __init__.py
│   ├── clock.py             # akumulátor pevného kroku
│   ├── geometry.py          # AABB, Vec2 v logickém prostoru
│   └── input.py             # InputSnapshot: čisté booly, bez pygame v sim vrstvě
├── data/
│   ├── __init__.py
│   ├── schema.py            # deklarativní schéma + LevelDataError
│   └── loader.py            # jeden loader pro všechna prostředí
├── sim/                     # ŽÁDNÝ import pygame.display/mixer/font
│   ├── __init__.py
│   ├── physics.py           # gravitace, AABB kolize po osách, coyote, buffer
│   ├── player.py
│   ├── enemy.py
│   ├── laser.py             # muzzle → vodorovný paprsek → první zásah
│   ├── level.py             # běhový stav jednoho prostředí
│   ├── session.py           # postup třemi prostředími
│   └── events.py            # SimEvent: co se stalo (pro zvuk a UI)
├── render/
│   ├── __init__.py
│   ├── presentation.py      # JEDINÉ místo, které zná velikost okna
│   ├── world.py             # plošiny, propast, hráč, protivník, východ, laser
│   ├── hud.py               # energie, teplota, název, „2/3"
│   └── text.py              # font, české diakritiky
├── screens/
│   ├── __init__.py
│   ├── machine.py           # stavový automat obrazovek
│   ├── title.py · play.py · pause.py · gameover.py · finish.py
│   ├── transition.py        # zatmavení / rozsvícení
│   └── error_screen.py      # FR-084
├── audio/
│   ├── __init__.py
│   └── mixer.py             # hudební smyčka, 5 SFX, bezpečné bez zvuk. zařízení
└── assets/
    ├── __init__.py
    └── registry.py          # stabilní ID → soubor, cache, žádné cesty v logice

assets/                      # VERZOVANÉ placeholdery (FR-081) — vlastník Codex
├── manifest.json
├── images/
├── music/
└── sfx/

levels/                      # VERZOVANÁ data prostředí
├── level_01_pobocka.json
├── level_02_sklad.json
└── level_03_kancelar.json

tools/
└── generate_placeholders.py # deterministický generátor (FR-082) — vlastník Codex

alzak_devtools/              # US6, P6 — MIMO src/alzak, vyloučeno z prod buildu
├── __init__.py
├── feedback/
│   ├── overlay.py           # F8, klávesová aktivace, indikátor
│   ├── capture.py           # snímek herní plochy bez ovládacího prvku
│   ├── annotate.py          # volná tužka + normalizovaná anotační vrstva
│   ├── package.py           # stabilní ID, kontext, checksumy, atomická publikace
│   └── queue.py             # capturing/queued/transferring/synced/transfer_failed
└── feedbackctl.py           # doctor/pull/list/show/respond/claim/release/
                             # complete/reopen/sync-status/verify

tests/
├── conftest.py              # SDL dummy drivery PŘED importem pygame
├── unit/                    # fyzika, laser, energie, protivník, schéma, registr
├── integration/             # průchod prostředím, přechody, obrazovky
└── devtools/                # feedback: prod-exclusion, E2E, ID, checksum, dedup

build/                       # gitignored
dist/                        # gitignored
feedback-store/              # gitignored (A-014)
├── inbox/ · archive/ · quarantine/

packaging/
├── alzak.spec               # PyInstaller
├── build_windows.ps1
└── build_macos.sh

.github/workflows/ci.yml     # testy headless + 3 artefakty
README.md                    # spuštění, build, F8, rozsah feedback adaptéru
```

**Structure Decision**: Jediný projekt s `src/` layoutem. Vertikální řez
`sim` (pravidla, bez pygame) / `render` + `screens` (prezentace) / `data` +
`assets` (vstupy) přesně odpovídá Principu IV a je nutnou podmínkou Principu V —
bez něj by testy vyžadovaly displej. Feedback vrstva je **samostatný top-level
balíček** `alzak_devtools/`, protože jen tak lze produkční vyloučení prokázat
strukturálně (PyInstaller nikdy nevidí adresář, který nezabalí) a otestovat
jediným importním testem, místo aby se spoléhalo na runtime příznak — což
`feedback_pipeline_standalone.md` §21.2 výslovně nepovažuje za dostatečné.

---

## Implementační fáze a stop-pointy

Mapování na `CLAUDE.md` §4 a scope §19. Toto je **vstup pro `tasks.md`**, ne
náhrada za něj.

| Fáze | Obsah | Úkoly | Odpovídá scope §19 | Stop-point |
|------|-------|-------|--------------------|------------|
| **F1 Setup** | repo skeleton, `pyproject.toml`, `conftest.py`, CI kostra, `.gitignore` | T001–T006 | §19/1 | ✅ |
| **F2 Foundational** | `config.py`, `paths.py`, `core/`, `render/presentation.py`, `render/text.py`, `assets/registry.py`, `data/schema.py`, `data/loader.py`, `screens/machine.py`, `screens/error_screen.py`, `app.py`, `audio/mixer.py` | T007–T029 | §19/2–4, 6–7 | ✅ |
| **F3 Assety (Codex)** | generátor placeholderů, obrázky, hudba, SFX, `manifest.json` | T030–T036 | §19/5 | ✅ **assetový stop-point (OD-004)** |
| **F4 US1 (P1)** | fyzika, hráč, protivník, laser, prostředí 1, východ, dokončení | T037–T056 | §19/8–12 | ✅ **MVP** |
| **F5 US2 (P2)** | energie, zásah, odhození, nezranitelnost, propast, obrazovka neúspěchu, R | T057–T066 | §19/13–14 | ✅ |
| **F6 US3 (P3)** | prostředí 2 a 3, postup, přechody, závěrečná obrazovka | T067–T076 | §19/15 | ✅ |
| **F7 US4 (P4)** | úvodní obrazovka, pauza, HUD, F11, hudba, 5 SFX | T077–T087 | §19/16–17 | ✅ |
| **F8 US5 (P5)** | PyInstaller spec, lokální build skripty, GitHub Actions, 3 artefakty | T088–T096 | §19/18–19 | ✅ |
| **F9 US6 (P6)** | feedback vrstva v `alzak_devtools/` + `feedbackctl` + minimum testů | T097–T110 | OD-001, A-012 | ✅ |
| **F10 Polish** | ladění hodnot v `config.py`, ruční smoke, `converge` | T111–T116 | §19/20 | ✅ |

> **Značení**: `F1…F10` jsou **implementační fáze**; `P1…P6` jsou **priority
> user stories** ze `spec.md`. Obě značky se nesmí zaměnit — proto se fáze
> neznačí písmenem `P`. Členění i čísla úkolů odpovídají `tasks.md` beze zbytku.

US1–US6 jsou nezávisle testovatelné v pořadí F4 → F9 podle `spec.md`.
F3 je jediný bod, kde plán **vyžaduje** práci Codexu s assety dřív, než jde
pokračovat: bez `manifest.json` a placeholderů nelze F4 vizuálně ověřit a nelze
doložit SC-012 ani SC-017. Herní logika však na assetech nezávisí — testy fází
F2 a F4–F7 běží i s prázdným registrem.

---

## Post-Design Constitution Re-Check

Po dokončení Phase 0 a Phase 1 (research.md, data-model.md, contracts/, quickstart.md):

- **Princip I**: návrh nezavedl žádnou komponentu nad rámec spec. Nejsložitější
  rozhodnutí (vlastní PNG/WAV zapisovač ve `tools/`) je vynuceno FR-082 + SC-017
  + zákazem runtime závislostí, ne vlastní ambicí. Nejde o abstrakci „do budoucna",
  ale o nejjednodušší způsob, jak splnit bajtovou reprodukovatelnost bez `Pillow`.
- **Princip II**: `data-model.md` uvádí úplný výčet konfiguračních klíčů včetně
  všech laserových. Žádná hodnota nezůstala mimo.
- **Princip III**: `contracts/level.schema.json` je jediné schéma pro všechny tři
  soubory; `contracts/level-format.md` popisuje chybové chování.
- **Princip IV**: `contracts/asset-manifest.md` definuje stabilní ID a doložil,
  že výměna souboru nemění herní pravidla.
- **Princip V**: `data-model.md` odděluje simulační stav od prezentačního a
  definuje `InputSnapshot` i `SimEvent` bez pygame typů.
- **Princip VI**: `quickstart.md` uvádí příkaz pro celou sadu i pro jednotlivé
  skupiny; každý SC má přiřazený způsob ověření.
- **Princip VII**: `contracts/input-map.md` a `research.md` R2 uzavírají škálování
  jediným místem v kódu.

**Žádné porušení. Complexity Tracking zůstává prázdný.**

---

## Complexity Tracking

> Vyplňuje se pouze při porušení Constitution Check.

Constitution Check prošla před Phase 0 i po Phase 1 **bez porušení**.
Tabulka je proto záměrně prázdná.

---

## Rizika plánu

| ID | Riziko | Dopad | Zmírnění |
|----|--------|-------|----------|
| RP-01 | Font s českou diakritikou — pygame vestavěný `freesansbold.ttf` nemusí pokrýt `ě š č ř ž ů ď ť ň`. | Nečitelné UI, porušení A-004. | `render/text.py` má jediný bod výběru fontu; ověřovací test vykreslí kontrolní řetězec a porovná, že žádný glyf není `.notdef`. Fallback = přibalený font (assetová práce → **Codex**). Viz research R14. |
| RP-02 | Bajtová shoda výstupu generátoru (SC-017) při použití knihovny třetí strany. | Nesplnitelné SC-017. | Generátor používá **jen stdlib** (`zlib`, `struct`, `wave`) — plná kontrola nad bajty. Viz research R8. |
| RP-03 | macOS Intel artefakt: GitHub `macos-13` runner může být v budoucnu zrušen. | Chybí jeden ze tří artefaktů (FR-064, SC-010). | CI pin na konkrétní runner label + poznámka v `contracts/build-and-ci.md`; alternativa `--target-arch x86_64` na arm64 runneru je zdokumentovaná, ale netestovaná. |
| RP-04 | Rozsah US6 je srovnatelný s celým herním demem (odhad z OD-001). | Posun dokončení. | Přísný výklad OD-001 bodu 1: každá z 9 položek v nejmenším vyhovujícím rozsahu; P6 až po US1–US5; explicitní degradace místo náhradních implementací. |
| RP-05 | Tunelování kolizí při vysoké rychlosti pádu. | Propadnutí plošinou, porušení FR-017. | `SIM_DT = 1/120 s` + omezená `MAX_FALL_SPEED` + validace schématu: minimální tloušťka plošiny > dráha za jeden krok. Viz research R3. |
| RP-06 | Nepodepsané macOS buildy blokuje Gatekeeper. | Testera zastaví varování. | A-009 to přijímá; `quickstart.md` uvádí přesný postup otevření. |

---

## Co plán vědomě neřeší

- Konkrétní vzhled placeholderů — vlastní **Codex** (OD-004).
- Finální hodnoty ladění pohybu — plán dává výchozí sadu v `data-model.md`,
  doladí se v P9 ručním testem.
- Podepisování a notarizace buildů — mimo rozsah (A-009).
- Cokoli z výslovně vyloučeného seznamu v Principu I.
