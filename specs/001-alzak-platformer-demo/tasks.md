# Tasks: Alzák — technologické demo 2D plošinovky

**Input**: Design documents from `/specs/001-alzak-platformer-demo/`
**Prerequisites**: [plan.md](./plan.md) · [spec.md](./spec.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [contracts/](./contracts/)
**Created**: 2026-09-03

**Tests**: **ANO — testy jsou vyžádány.** Princip VI ústavy (NON-NEGOTIABLE) a
FR-061/FR-062 je vyžadují po každé funkci.

**Organization**: Úkoly jsou seskupené podle user stories, aby šla každá
implementovat a otestovat samostatně.

## Format: `[ID] [P?] [Story?] [OWNER?] Description`

- **[P]**: lze zpracovat paralelně (jiné soubory, žádná závislost na nedokončeném úkolu)
- **[Story]**: `[US1]`…`[US5]` — jen ve fázích user stories
- **[OWNER:Codex]**: **assetová práce dle OD-004** — Claude na ni vždy výslovně
  upozorní v handoff bloku a nikdy ji tiše neobejde ani neprovede sám

## Vlastnictví

Celou implementaci provádí **Codex** (`constitution.md` → Governance).
Značka `[OWNER:Codex]` navíc odděluje **assetovou práci**, kterou OD-004 vyhrazuje
Codexu jako samostatné, viditelně označené úkoly:

| Úkol | Předmět |
|------|---------|
| **T029** | deterministický generátor placeholderů |
| **T030** | všechny obrazové placeholdery |
| **T031** | hudební a zvukové placeholdery |
| **T032** | manifest stabilních asset ID |

## Path Conventions

Single project, `src/` layout dle [plan.md](./plan.md) → Project Structure.
Cesty jsou relativní ke kořeni repozitáře.

---

## Fáze F1: Setup (Shared Infrastructure)

**Purpose**: Kostra projektu a testovací prostředí. Nic herního.

- [X] T001 Vytvořit adresářovou strukturu dle plan.md v `src/alzak/`, `tests/`, `tools/`, `packaging/`, `levels/`, `assets/`
- [X] T002 Vytvořit `pyproject.toml` — Python 3.12, runtime závislost výhradně `pygame-ce`, extra `[dev]` s `pytest` a `pyinstaller`, `src/` layout
- [X] T003 [P] Ověřit `.gitignore`; pipeline-specifický `feedback-store/` se dle OD-007 nepřidává
- [X] T004 [P] Vytvořit `tests/conftest.py` nastavující `SDL_VIDEODRIVER=dummy`, `SDL_AUDIODRIVER=dummy` a `PYGAME_HIDE_SUPPORT_PROMPT=1` **před** importem pygame
- [X] T005 [P] Vytvořit kostru `.github/workflows/ci.yml` s jediným jobem `test` na `ubuntu-latest`
- [X] T006 Vytvořit `src/alzak/__init__.py` s `__version__` a `src/alzak/__main__.py` spouštějící `app.main()`

**Checkpoint**: `pytest` proběhne (byť s nulou testů), `python -m alzak` skončí čistě.

---

## Fáze F2: Foundational (Blocking Prerequisites)

**Purpose**: Infrastruktura, bez které nelze začít **žádnou** user story.
Herní logika zde ještě nevzniká.

⚠️ **Tuto fázi musí dokončit před zahájením kterékoli user story.**

### Konfigurace a jádro

- [X] T007 Vytvořit `src/alzak/config.py` s úplným výčtem skupin `DISPLAY`, `SIM`, `PLAYER`, `JUMP`, `ENERGY`, `LASER`, `ENEMY`, `LEVEL`, `HUD`, `AUDIO` dle data-model.md §3; `LASER` obsahuje `muzzle_offset`, `collision_thickness = 16` a všechny `draw_*` klíče. Skupina `FEEDBACK` se dle OD-007 nevytváří (FR-019, FR-034, FR-085…FR-087)
- [X] T008 [P] Vytvořit `src/alzak/paths.py` řešící kořen prostředků pro zdrojový i zabalený (`sys._MEIPASS`) běh
- [X] T009 [P] Vytvořit `src/alzak/core/geometry.py` — AABB obdélník ve `float` a testy překryvu, bez pygame typů
- [X] T010 [P] Vytvořit `src/alzak/core/clock.py` — akumulátor pevného kroku `SIM_DT` s ořezem `max_frame_time`; cílová frekvence vykreslování 60 FPS a časovače konzistentní při výkyvech FPS (FR-004, research R1)
- [X] T011 [P] Vytvořit `src/alzak/core/input.py` — `InputSnapshot` (čisté booly) a převod ze stavu pygame klávesnice dle `contracts/input-map.md`: šipky vlevo/vpravo, mezerník, X, Escape, R, F11 (FR-003, FR-006, FR-007, FR-008, FR-009, FR-010)
- [X] T012 [P] Napsat `tests/unit/test_geometry.py` a `tests/unit/test_clock.py` — překryvy AABB a stabilita akumulátoru při kolísavém `dt`

### Prezentační vrstva

- [X] T013 Vytvořit `src/alzak/render/presentation.py` — logický `Surface` 1920×1080, čistá funkce `compute_viewport()`, škálování oběma směry, letterbox i pillarbox (FR-001, FR-002, Princip VII)
- [X] T014 Napsat `tests/unit/test_presentation.py` ověřující `compute_viewport()` na 1920×1080, 1280×720, 3840×2160, 2560×1080 a 1600×1200 (SC-019)
- [X] T015 [P] Vytvořit `src/alzak/render/text.py` s **jediným** místem výběru fontu (research R14)
- [X] T016 [P] Napsat `tests/unit/test_text_czech_glyphs.py` ověřující, že žádný znak z `ěščřžýáíéúůďťňĚŠČŘŽ` nevykreslí `.notdef` (A-004)

### Assety a data

- [X] T017 Vytvořit `src/alzak/assets/registry.py` — mapování stabilních ID na soubory, líné načítání s cache, chybějící ID = tvrdá chyba, chybějící soubor ve vývoji = viditelný placeholder (FR-050, `contracts/asset-manifest.md`)
- [X] T018 [P] Napsat `tests/unit/test_asset_registry.py` na obě chybová chování a na cache
- [X] T019 Vytvořit `src/alzak/data/schema.py` — deklarativní schéma dle `contracts/level.schema.json` a výjimku `LevelDataError(file, field, reason)`, jen stdlib (research R5)
- [X] T020 Vytvořit `src/alzak/data/loader.py` — **jeden** loader pro všechna prostředí, strukturální i sémantická validace dle `contracts/level-format.md`; validace vynutí, že každé prostředí obsahuje plošiny, propast, jednu instanci protivníka, startovní pozici a východ (FR-043, FR-047)
- [X] T021 Napsat `tests/unit/test_level_loader.py` — chybějící pole, špatný typ, `platform.h < 32`, start nad propastí, trasa protivníka mimo plošinu, neznámé `asset_id`, duplicitní `order` (FR-046, FR-047)

### Aplikace a obrazovky

- [X] T022 Vytvořit `src/alzak/screens/machine.py` — stavový automat `TITLE·PLAY·PAUSE·TRANSITION·GAMEOVER·FINISH·ERROR`; simulace se posouvá **pouze** v `PLAY` (research R13)
- [X] T023 Vytvořit `src/alzak/screens/error_screen.py` — chybová obrazovka uvnitř aplikace (soubor + pole + důvod), ovladatelná klávesnicí (FR-084)
- [X] T024 Vytvořit `src/alzak/app.py` — okno, hlavní smyčka s pevným krokem, dispatch přes `screens/machine.py` (ve fázi F2 jen `TITLE` a `ERROR`; `PLAY` přibude v T054), F11 v každém stavu, zachycení `LevelDataError` na nejvyšší úrovni → chybová obrazovka + `stderr` + `sys.exit(2)` (FR-003, FR-084)
- [X] T025 Napsat `tests/integration/test_error_screen.py` ověřující zprávu na `stderr` a návratový kód 2 při poškozeném JSON (SC-018)
- [X] T026 [P] Vytvořit `src/alzak/audio/mixer.py` — hudební smyčka a SFX, při nedostupném zvukovém zařízení přepnutí do no-op režimu bez pádu
- [X] T027 [P] Napsat `tests/unit/test_audio_fallback.py` ověřující běh bez zvukového zařízení
- [X] T028 Napsat `tests/unit/test_sim_purity.py` — statická (AST) kontrola, že žádný modul v `src/alzak/sim/` neimportuje `pygame.display`, `pygame.mixer` ani `pygame.font`; ve fázi F2 je adresář ještě prázdný, test proto musí **selhat, když `src/alzak/sim/` neexistuje**, aby od fáze F4 skutečně hlídal (Princip V)

- [X] T029 **CHECKPOINT Foundational**: spustit celou sadu `pytest`, ověřit `python -m alzak` (prázdná obrazovka), commitnout, vydat handoff a kontextový marker

---

## Fáze F3: Placeholderové assety — vlastník Codex (OD-004)

**Purpose**: Vyrobit verzované placeholdery a manifest. **Herní logika na nich
nezávisí** — fáze 4–7 lze testovat i s prázdným registrem; assety jsou nutné až
pro vizuální ověření a ruční smoke test.

⚠️ **Assetový stop-point.** Claude na tuto fázi upozorní v handoff bloku (OD-004).

- [X] T030 [OWNER:Codex] Vytvořit `tools/generate_placeholders.py` — deterministický generátor s vlastním PNG zapisovačem (`zlib` + `struct`) a WAV zapisovačem (`wave`), **jen stdlib**, pevné pořadí položek, žádný neseedovaný `random`, žádná časová metadata; režim `--verify` nic nezapisuje (FR-082, SC-017, research R8)
- [X] T031 [OWNER:Codex] Vygenerovat a **commitnout** všechny obrazové placeholdery do `assets/images/` — Alzák (idle/run/air/hurt), protivník (walk/hit), plošiny pobočky/skladu/kanceláře, propast, východ neaktivní i aktivní, tři pozadí, HUD energie plná/prázdná, rám a výplň ukazatele teploty (FR-049, FR-081, `contracts/asset-manifest.md`)
- [X] T032 [OWNER:Codex] Vygenerovat a **commitnout** hudební smyčku do `assets/music/` a **přesně pět** zvukových efektů do `assets/sfx/` — pohyb, skok, spuštění laseru, trvání laseru, ukončení laseru (FR-056, FR-058, A-003)
- [X] T033 [OWNER:Codex] Vytvořit `assets/manifest.json` — stabilní ID → cesta + `sha256` + příznak `generated` pro každou položku dle `contracts/asset-manifest.md` (FR-050)
- [X] T034 Napsat `tests/unit/test_asset_manifest.py` — všechna povinná ID přítomna, každý soubor existuje, `sha256` souhlasí, počet zvukových efektů je právě 5
- [X] T035 Napsat `tests/unit/test_placeholder_determinism.py` — `tools/generate_placeholders.py --verify` nezmění ani jeden bajt (SC-017)

- [X] T036 **CHECKPOINT Assety**: celá sada, vizuální kontrola placeholderů, commit, handoff

---

## Fáze F4: User Story 1 — Průchod jedním prostředím (Priority: P1) 🎯 MVP

**Goal**: Hráč se pohybuje, skáče, laserem porazí protivníka, východ se aktivuje
a vstupem do něj je prostředí dokončeno.

**Independent Test**: Spustit hru přímo v prvním prostředí a projít cyklus
pohyb → skok → laser → poražení → východ. Nevyžaduje menu, další prostředí ani energii.

### Simulace

- [X] T037 [US1] Vytvořit `src/alzak/sim/events.py` — výčet `SimEvent` dle data-model.md §1.7
- [X] T038 [US1] Vytvořit `src/alzak/sim/physics.py` — gravitace s omezenou rychlostí pádu, integrace a kolize AABB **po osách** X→Y s posunem na hranu a vynulováním složky rychlosti (FR-013, FR-017, research R3)
- [X] T039 [US1] Napsat `tests/unit/test_physics.py` — dopad na plošinu, náraz do boku, žádné propadnutí při maximální rychlosti pádu, žádné zaseknutí v rohu
- [X] T040 [US1] Vytvořit `src/alzak/sim/player.py` — zrychlení a tření po zemi, snížená kontrola ve vzduchu, proměnlivá výška skoku, coyote time, jump buffer, `facing`, `on_ground` (FR-011…FR-019)
- [X] T041 [US1] Napsat `tests/unit/test_player_movement.py` — dosažení maximální rychlosti, zastavení po uvolnění, obě šipky současně = žádné zrychlení
- [X] T042 [US1] Napsat `tests/unit/test_player_jump.py` — krátký vs. držený skok, coyote time 90–110 ms, jump buffer 110–130 ms (SC-007)
- [X] T043 [US1] Vytvořit `src/alzak/sim/enemy.py` — hlídkování mezi dvěma datově definovanými body s otočením na kraji, `hp`, `hit_flash_timer` (FR-035, FR-036, FR-038)
- [X] T044 [US1] Napsat `tests/unit/test_enemy_patrol.py` — otočení na obou krajních bodech, setrvání v mezích trasy
- [X] T045 [US1] Vytvořit `src/alzak/sim/laser.py` — muzzle bod z `config.LASER["muzzle_offset"]` zrcadlený podle `facing`, vodorovný pás o `collision_thickness`, `end_x` = nejbližší zásah, stavy `IDLE·FIRING·LOCKED`, ohřev a chlazení (FR-027…FR-034, FR-085…FR-087)
- [X] T046 [US1] Napsat `tests/unit/test_laser_geometry.py` — start v muzzle bodu, výchozí tloušťka 16 px, konec na nejbližší plošině, plošina mezi hráčem a protivníkem blokuje poškození, paprsek končí na hraně obrazovky (SC-021, US1 scénář 7)
- [X] T047 [US1] Napsat `tests/unit/test_laser_heat.py` — přehřátí za 1,4–1,6 s, zablokování, opětovná aktivace až pod prahem i při stále drženém X (SC-005, FR-032)
- [X] T048 [US1] Napsat `tests/unit/test_enemy_defeat.py` — poražení za 0,9–1,1 s souvislého působení **a** za stejný celkový čas při dvou oddělených dávkách (SC-004, SC-020, FR-039)
- [X] T049 [US1] Vytvořit `src/alzak/sim/level.py` — `LevelState` sestavená vždy z `LevelData` + `config`, pořadí vyhodnocení kroku dle data-model.md §1.5, aktivace východu po poražení protivníka, dokončení vstupem do aktivního východu (FR-040, FR-044, FR-045)
- [X] T050 [US1] Napsat `tests/unit/test_level_state.py` — neaktivní východ při překryvu nic nedělá, aktivní dokončí prostředí, aktivace nastane jen po poražení
- [X] T051 [US1] Napsat `tests/unit/test_framerate_independence.py` — shodná výška skoku, dolet a doba přehřátí při simulaci odpovídající 30 a 60 FPS v mezích 5 % (SC-003)

### Data a prezentace

- [X] T052 [US1] Vytvořit `levels/level_01_pobocka.json` dle `contracts/level-format.md` — jedna pevná obrazovka 1920 × 1080 se statickou kamerou obsahující plošiny, propast, trasu protivníka, startovní pozici, východ a odkazy na asset ID (FR-042, FR-043)
- [X] T053 [US1] Vytvořit `src/alzak/render/world.py` — vykreslení pozadí, plošin, propasti, hráče, protivníka, východu (dva vizuálně odlišné stavy) a laseru z `draw_*` klíčů konfigurace (FR-044, FR-087)
- [X] T054 [US1] Vytvořit `src/alzak/screens/play.py` — propojení `InputSnapshot` → simulace → `render/world.py`, R restartuje prostředí (FR-010)
- [X] T055 [US1] Napsat `tests/integration/test_us1_playthrough.py` — headless průchod: pohyb, skok přes propast, laser, poražení, aktivace východu, dokončení

- [X] T056 [US1] **CHECKPOINT MVP**: celá sada + ruční smoke test dle quickstart.md §5 bodů 1–4, commit, handoff

---

## Fáze F5: User Story 2 — Přežití, zranění a neúspěch (Priority: P2)

**Goal**: Energie, zásah s odhozením a nezranitelností, pád do propasti,
obrazovka neúspěchu a úplný restart prostředí.

**Independent Test**: V jednom prostředí opakovaně narazit do protivníka a spadnout
do propasti; ověřit odpočet energie, odhození, nezranitelnost, respawn, obrazovku
neúspěchu a restart.

**Depends on**: US1 (F4)

- [X] T057 [US2] Doplnit do `src/alzak/sim/player.py` energii, `invuln_timer` a odhození dle `config.ENERGY` (FR-020…FR-022)
- [X] T058 [US2] Doplnit do `src/alzak/sim/level.py` vyhodnocení kontaktu hráč × protivník (FR-037) a pádu do propasti se zachováním stavu protivníka i východu (FR-023, A-002)
- [X] T059 [US2] Napsat `tests/unit/test_energy.py` — start se 3 body, ztráta právě 1 bodu, nezranitelnost 0,9–1,1 s, druhý dotyk během ní bez účinku, po vypršení další ztráta (SC-006)
- [X] T060 [US2] Napsat `tests/unit/test_pit_fall.py` — pád odebere 1 bod, vrátí hráče na start, protivník si zachová pozici i utržené poškození, východ si zachová stav
- [X] T061 [US2] Napsat `tests/unit/test_failure_precedence.py` — poražení protivníka a vyčerpání energie v témže kroku ⇒ přednost má neúspěch, prostředí se nepočítá jako dokončené (A-010)
- [X] T062 [US2] Vytvořit `src/alzak/screens/gameover.py` s položkami „Opakovat prostředí" a „Ukončit hru" (FR-024, FR-054)
- [X] T063 [US2] Implementovat úplný restart prostředí v `src/alzak/screens/play.py` a `sim/level.py` — nová `LevelState`: pozice, 3 body energie, vychladlý laser, plně obnovený protivník, neaktivní východ (FR-026)
- [X] T064 [US2] Napsat `tests/integration/test_level_restart.py` — R i „Opakovat prostředí" obnoví **všech pět** složek počátečního stavu
- [X] T065 [US2] Napsat `tests/integration/test_us2_survival.py` — headless: tři zásahy ⇒ obrazovka neúspěchu; odhození nad propastí vede k normálnímu vyhodnocení pádu

- [X] T066 [US2] **CHECKPOINT US2**: celá sada + ruční smoke dle quickstart.md §5 bodu 5, commit, handoff

---

## Fáze F6: User Story 3 — Kompletní průchod třemi prostředími (Priority: P3)

**Goal**: Pevné pořadí pobočka → sklad → kancelář, přechody, doplnění energie,
závěrečná obrazovka a restart dema.

**Independent Test**: Odehrát celý průchod od prvního prostředí po závěrečnou
obrazovku a ověřit pořadí, přechody a obnovení energie.

**Depends on**: US1 (F4)

- [X] T067 [US3] [P] Vytvořit `levels/level_02_sklad.json` dle `contracts/level-format.md` (FR-042, FR-043)
- [X] T068 [US3] [P] Vytvořit `levels/level_03_kancelar.json` dle `contracts/level-format.md` (FR-042, FR-043)
- [X] T069 [US3] Vytvořit `src/alzak/sim/session.py` — index prostředí, pevná posloupnost tří, doplnění energie na 3 při vstupu, příznak dokončení dema (FR-025, FR-041)
- [X] T070 [US3] Napsat `tests/unit/test_session_progression.py` — pořadí prostředí, doplnění energie bez ohledu na předchozí stav, dokončení po třetím
- [X] T071 [US3] Vytvořit `src/alzak/screens/transition.py` — zatmavení a rozsvícení dle `config.LEVEL["transition_fade_time"]`; Escape stisknutý během přechodu se uplatní až po jeho dokončení (FR-048, Edge Case)
- [X] T072 [US3] Napsat `tests/integration/test_transition.py` — přechod doběhne konzistentně, Escape během něj nenechá hru v rozbitém stavu, akumulátor se po návratu nedožene dávkou kroků
- [X] T073 [US3] Vytvořit `src/alzak/screens/finish.py` s položkami „Spustit znovu" a „Ukončit" (FR-055)
- [X] T074 [US3] Napsat `tests/unit/test_all_levels_load.py` — všechny tři JSON se načtou **stejným** loaderem bez výjimky specifické pro prostředí (SC-008)
- [X] T075 [US3] Napsat `tests/integration/test_us3_full_run.py` — headless průchod všemi třemi prostředími až na závěrečnou obrazovku a restart dema

- [X] T076 [US3] **CHECKPOINT US3**: celá sada + ruční průchod celým demem, commit, handoff

---

## Fáze F7: User Story 4 — Ovládání aplikace, HUD a zvuková odezva (Priority: P4)

**Goal**: Úvodní obrazovka, pauza, HUD, F11 a kompletní zvuková vrstva.

**Independent Test**: Projít všechny obrazovky pouze klávesnicí, ověřit každý
prvek HUD a každý zvukový efekt proti odpovídající akci.

**Depends on**: US1, US3 (obrazovky navazují na postup demem)

- [X] T077 [US4] Vytvořit `src/alzak/screens/title.py` — název dema, „Spustit", „Ukončit"; ovládání pouze klávesnicí (FR-051, FR-005)
- [X] T078 [US4] Vytvořit `src/alzak/screens/pause.py` — „Pokračovat", „Restartovat prostředí", „Ukončit hru"; simulace zastavena, hudba ztišena na `AUDIO["music_volume_paused"]` (FR-009, FR-053, FR-057)
- [X] T079 [US4] Implementovat pravidla ukončení aplikace v `src/alzak/screens/pause.py`, `src/alzak/screens/gameover.py`, `src/alzak/screens/title.py`, `src/alzak/screens/finish.py` a `src/alzak/app.py` — „Ukončit hru" v pauze i na obrazovce neúspěchu vrací na úvodní obrazovku; aplikaci ukončí **pouze** „Ukončit" na úvodní a závěrečné obrazovce (FR-083)
- [X] T080 [US4] Napsat `tests/integration/test_exit_rules.py` — FR-083 pro všechny čtyři cesty
- [X] T081 [US4] Vytvořit `src/alzak/render/hud.py` — tři body energie, ukazatel teploty laseru, název prostředí a pořadí „2/3"; všechny rozměry a barvy z `config.HUD` (FR-033, FR-052)
- [X] T082 [US4] Napsat `tests/unit/test_hud.py` — HUD čte hodnoty ze stavu, obsahuje všechny čtyři prvky, neobsahuje číselné konstanty
- [X] T083 [US4] Propojit `src/alzak/audio/mixer.py` se `SimEvent` — hudební smyčka souvislá i přes přechody, zvuk pohybu řízený skutečným pohybem po pevné ploše, zvuky skoku a laseru (FR-056, FR-058, FR-059)
- [X] T084 [US4] Napsat `tests/integration/test_audio_events.py` — zvuk trvání laseru okamžitě končí při uvolnění X, přehřátí, pauze, vstupu do východu i jakékoli změně stavu obrazovky (FR-060)
- [X] T085 [US4] Implementovat F11 v `src/alzak/app.py` a `render/presentation.py` — přepnutí v kterémkoli stavu bez změny rozmístění (FR-003)
- [X] T086 [US4] Napsat `tests/integration/test_us4_screens.py` — headless průchod všemi obrazovkami výhradně klávesnicí

- [X] T087 [US4] **CHECKPOINT US4**: celá sada + ruční smoke dle quickstart.md §5 bodů 6–8, commit, handoff

---

## Fáze F8: User Story 5 — Spuštění a distribuce (Priority: P5)

**Goal**: Spuštění ze zdroje, lokální buildy pro Windows i macOS a tři artefakty
z jednoho běhu GitHub Actions.

**Independent Test**: Čistý klon → instalace závislostí → spuštění → build →
stažený artefakt spustit a dohrát demo.

**Depends on**: US1–US4 (je co balit)

- [X] T088 [US5] Vytvořit `packaging/alzak.spec` — režim onedir, `datas` s `assets/` a `levels/`, vývojové závislosti `pytest` a `PyInstaller` v `excludes`, `console=False` (FR-065)
- [X] T089 [US5] [P] Vytvořit `packaging/build_windows.ps1` — ověření prostředí a volání PyInstalleru
- [X] T090 [US5] [P] Vytvořit `packaging/build_macos.sh` — ověření prostředí a volání PyInstalleru
- [X] T091 [US5] Doplnit `.github/workflows/ci.yml` o joby `build-windows` (`windows-latest`), `build-macos-arm` (`macos-15`) a `build-macos-intel` (`macos-15-intel`), všechny s `needs: test`, každý nahrávající pojmenovaný artefakt (FR-064, SC-010, `contracts/build-and-ci.md`)
- [X] T092 [US5] Doplnit do `.github/workflows/ci.yml` běh `tools/generate_placeholders.py --verify` a testy na Windows i macOS runnerech (SC-009, SC-017)
- [X] T093 [US5] Napsat `tests/unit/test_packaging_spec.py` — `packaging/alzak.spec` zahrnuje `assets/` i `levels/`, vylučuje vývojové závislosti a používá bezkonzolový režim
- [X] T094 [US5] Vytvořit `README.md` s kroky ze `quickstart.md` §2 a §4.6 — spuštění ze zdroje, testy, lokální buildy a postup pro nepodepsaný macOS build (FR-063, A-009)
- [ ] T095 [US5] Ruční ověření staženého artefaktu (`dist/Alzak/` resp. `dist/Alzak.app`) na cílovém systému dle `quickstart.md` §4.6 — dohrát celé demo bez nainstalovaného Pythonu (SC-011); poškozený `levels/level_02_sklad.json` v zabaleném buildu vede k chybové obrazovce a exit kódu 2 (SC-018)

- [ ] T096 [US5] **CHECKPOINT US5**: celá sada, tři artefakty z jednoho běhu CI, commit, handoff

---

## Fáze F9: Polish & Cross-Cutting Concerns

**Purpose**: Doladění, ověření všech kritérií úspěchu a uzavření feature.

- [X] T111 Doladit hodnoty v `src/alzak/config.py` ručním testem — pohyb, skok, laser, protivník; hodnoty musí trvale splňovat SC-003…SC-007 a SC-021 (research R15)
- [X] T112 Napsat `tests/unit/test_no_magic_numbers.py` — statická kontrola, že `sim/laser.py`, `sim/player.py`, `sim/enemy.py`, `render/world.py` a `render/hud.py` neobsahují číselné herní konstanty (Princip II, SC-021)
- [X] T113 Projít `quickstart.md` §4 a doložit každé **aktivní** kritérium úspěchu konkrétním důkazem; SC-014…SC-016 a SC-022 jsou vyřazeny OD-007
- [X] T114 Projít `specs/001-alzak-platformer-demo/checklists/` a vyhodnotit CHK001–CHK128; nálezy zapsat do `analysis-report.md` nebo `open-decisions.md`
- [X] T115 Spustit `/speckit-converge` nad `specs/001-alzak-platformer-demo/` a odstranit případný rozdíl mezi specifikací a implementací (SC-013)
- [ ] T116 **CHECKPOINT Release**: celá sada na všech třech OS, tři artefakty, ruční průchod dema, závěrečný report dle `AGENTS.md` §19, commit, handoff

---

## Fáze F10: Výtvarná a herní revize OD-008

**Purpose**: Zapracovat přímou revizi zadavatele před finálním converge: stylizovaný
high-poly vzhled bez fotorealismu, profilový animovaný Alzák s pistolí, konečný
laser, neblokové plošiny a doložená dosažitelnost.

- [X] T117 [OWNER:Codex] Zapsat OD-008 do `open-decisions.md`, `spec.md`, `plan.md`, `data-model.md` a `contracts/asset-manifest.md` jako FR-089…FR-093 a SC-023…SC-025
- [X] T118 [OWNER:Codex] Vytvořit a verzovat transparentní osmipózový high-poly atlas Alzáka a tři autorská stylizovaná high-poly pozadí pobočky, skladu a kanceláře; zdrojové reference uložit do `assets/source/`
- [X] T119 Rozšířit `assets/manifest.json` a `src/alzak/assets/registry.py` o obdélníky atlasu, `generated: false`, zdroj a checksum; generátor autorské bitmapy nepřepisuje (FR-091, SC-023)
- [X] T120 Implementovat v `src/alzak/render/world.py`, `src/alzak/sim/player.py` a `src/alzak/config.py` profilové zrcadlení, idle/mrknutí, tři fáze běhu, skok, střelbu, zásah a zarovnání pistole s muzzle (FR-089)
- [X] T121 Implementovat a otestovat konfigurovatelný maximální dosah laseru 900 px, omezení hranou obrazu a zachování prvního zásahu (FR-090, SC-025)
- [X] T122 Nahradit plné blokové vykreslení plošin tenkou průhlednou konstrukční lávkou, sesouhlasit výšky ve všech třech JSON úrovních a vizuálně sjednotit protivníka a východ (FR-092, FR-093)
- [X] T123 Doplnit test atlasových obdélníků a automatický vstupový test dosažitelnosti každé zvýšené plošiny ve všech třech úrovních; spustit celou sadu a `tools/generate_placeholders.py --verify` (SC-017, SC-023, SC-024)
- [X] T124 Provést vizuální kontrolu runtime renderu všech tří prostředí, source smoke, znovu vytvořit a spustit lokální macOS build; ručně dohrát demo, pokud ovládací rozhraní prostředí umožní držení kláves
- [X] T125 **CHECKPOINT OD-008**: prohlédnout diff, commitnout výtvarnou revizi a vrátit se k T111–T116; `speckit-converge` se smí uzavřít až nad tímto stavem

---

## Dependencies & Execution Order

```text
F1  Setup
 └─ F2  Foundational            (blokuje vše ostatní)
     ├─ F3  Assety [Codex]      (blokuje vizuální ověření, SC-012 a SC-017;
     │                           NEblokuje testy simulace)
     └─ F4  US1 (P1)  MVP
         ├─ F5  US2 (P2)
         └─ F6  US3 (P3)
             └─ F7  US4 (P4)
                 └─ F8  US5 (P5)
                     └─ F9 Polish
                         └─ F10 Výtvarná revize OD-008
                             └─ návrat k otevřeným gate úkolům T111–T116
```

**Blokující hrany**:

- F2 blokuje **vše** ostatní.
- F3 blokuje ruční smoke testy a SC-012/SC-017, **neblokuje** testy simulace.
- US2 a US3 jsou na sobě nezávislé; obě závisí na US1.
- US4 závisí na US1 a US3 (HUD zobrazuje pořadí prostředí).
- US5 závisí na hotovém herním demu; poté následuje závěrečné ověření.

## Parallel Opportunities

| Skupina | Úkoly | Proč lze paralelně |
|---------|-------|--------------------|
| Setup | T003, T004, T005 | různé soubory |
| Jádro | T008, T009, T010, T011, T012 | různé moduly bez vzájemné závislosti |
| Prezentace | T015, T016 | nezávislé na `presentation.py` |
| Audio | T026, T027 | mimo hlavní řetěz |
| Prostředí | T067, T068 | dva různé JSON soubory |
| Buildy | T089, T090 | dva platformní skripty |

## Independent Test Criteria

| Story | Nezávislý test | Fáze |
|-------|----------------|------|
| US1 | Průchod cyklem pohyb → skok → laser → poražení → východ v prvním prostředí | F4 |
| US2 | Opakované zásahy a pády v jednom prostředí; energie, nezranitelnost, neúspěch, restart | F5 |
| US3 | Celý průchod třemi prostředími až na závěrečnou obrazovku | F6 |
| US4 | Všechny obrazovky pouze klávesnicí; každý prvek HUD a každý zvuk proti akci | F7 |
| US5 | Čistý klon → build → stažený artefakt dohraje demo bez Pythonu | F8 |

## MVP Scope

**MVP = F1 + F2 + F3 + F4 (US1)** → T001–T056.

Po T056 existuje hratelné prostředí, které předvádí pohyb, souboj i cíl.
F3 je součástí MVP pouze proto, že bez placeholderů není demo předvedení
schopné; herní logika na ní nezávisí.

## Testovací checkpointy

| Checkpoint | Úkol | Rozsah validace |
|------------|------|-----------------|
| Foundational | T029 | celá sada + prázdná obrazovka |
| Assety | T036 | celá sada + vizuální kontrola + SC-017 |
| **MVP (US1)** | T056 | celá sada + ruční smoke 1–4 |
| US2 | T066 | celá sada + ruční smoke 5 |
| US3 | T076 | celá sada + ruční průchod demem |
| US4 | T087 | celá sada + ruční smoke 6–8 |
| US5 | T096 | celá sada na 3 OS + 3 artefakty |
| Release | T116 | vše + `converge` + závěrečný report |
| Výtvarná revize | T125 | celá sada + asset verify + 3 rendery + lokální build |

Na každém checkpointu platí `CLAUDE.md` §4: spustit validaci, aktualizovat tasks,
prohlédnout diff, commitnout (OD-003), ohlásit odchylky a **zastavit**, není-li
další checkpoint výslovně autorizován.

## Souhrn

| Ukazatel | Hodnota |
|----------|---------|
| Celkem aktivních úkolů | **111** (T001–T096 a T111–T125; T097–T110 vyřazeny OD-007) |
| Setup | 6 (T001–T006) |
| Foundational | 23 (T007–T029) |
| Fáze assetů | 7 (T030–T036), z toho **4 označené `[OWNER:Codex]`** (T030–T033) |
| US1 (P1, MVP) | 20 (T037–T056) |
| US2 (P2) | 10 (T057–T066) |
| US3 (P3) | 10 (T067–T076) |
| US4 (P4) | 11 (T077–T087) |
| US5 (P5) | 9 (T088–T096) |
| Polish | 6 (T111–T116) |
| Výtvarná revize | 9 (T117–T125) |
| Testovací úkoly | 35 |
| Checkpointy | 8 |
