# Tasks: Alzák — technologické demo 2D plošinovky

**Input**: Design documents from `/specs/001-alzak-platformer-demo/`
**Prerequisites**: [plan.md](./plan.md) · [spec.md](./spec.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [contracts/](./contracts/)
**Created**: 2026-09-03

**Tests**: **ANO — testy jsou vyžádány.** Princip VI ústavy (NON-NEGOTIABLE) a
FR-061/FR-062 je vyžadují po každé funkci. Pro feedback vrstvu (US6) platí zúžený
rozsah dle OD-001 bodu 2.

**Organization**: Úkoly jsou seskupené podle user stories, aby šla každá
implementovat a otestovat samostatně.

## Format: `[ID] [P?] [Story?] [OWNER?] Description`

- **[P]**: lze zpracovat paralelně (jiné soubory, žádná závislost na nedokončeném úkolu)
- **[Story]**: `[US1]`…`[US6]` — jen ve fázích user stories
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

- [ ] T007 Vytvořit `src/alzak/config.py` s úplným výčtem skupin `DISPLAY`, `SIM`, `PLAYER`, `JUMP`, `ENERGY`, `LASER`, `ENEMY`, `LEVEL`, `HUD`, `AUDIO`, `FEEDBACK` dle data-model.md §3; `LASER` musí obsahovat `muzzle_offset`, `collision_thickness = 16`, `draw_*` klíče a `FEEDBACK["hotkey"] = F8` (FR-019, FR-034, FR-085…FR-088)
- [ ] T008 [P] Vytvořit `src/alzak/paths.py` řešící kořen prostředků pro zdrojový i zabalený (`sys._MEIPASS`) běh
- [ ] T009 [P] Vytvořit `src/alzak/core/geometry.py` — AABB obdélník ve `float` a testy překryvu, bez pygame typů
- [ ] T010 [P] Vytvořit `src/alzak/core/clock.py` — akumulátor pevného kroku `SIM_DT` s ořezem `max_frame_time`; cílová frekvence vykreslování 60 FPS a časovače konzistentní při výkyvech FPS (FR-004, research R1)
- [ ] T011 [P] Vytvořit `src/alzak/core/input.py` — `InputSnapshot` (čisté booly) a převod ze stavu pygame klávesnice dle `contracts/input-map.md`: šipky vlevo/vpravo, mezerník, X, Escape, R, F11 (FR-003, FR-006, FR-007, FR-008, FR-009, FR-010)
- [ ] T012 [P] Napsat `tests/unit/test_geometry.py` a `tests/unit/test_clock.py` — překryvy AABB a stabilita akumulátoru při kolísavém `dt`

### Prezentační vrstva

- [ ] T013 Vytvořit `src/alzak/render/presentation.py` — logický `Surface` 1920×1080, čistá funkce `compute_viewport()`, škálování oběma směry, letterbox i pillarbox (FR-001, FR-002, Princip VII)
- [ ] T014 Napsat `tests/unit/test_presentation.py` ověřující `compute_viewport()` na 1920×1080, 1280×720, 3840×2160, 2560×1080 a 1600×1200 (SC-019)
- [ ] T015 [P] Vytvořit `src/alzak/render/text.py` s **jediným** místem výběru fontu (research R14)
- [ ] T016 [P] Napsat `tests/unit/test_text_czech_glyphs.py` ověřující, že žádný znak z `ěščřžýáíéúůďťňĚŠČŘŽ` nevykreslí `.notdef` (A-004)

### Assety a data

- [ ] T017 Vytvořit `src/alzak/assets/registry.py` — mapování stabilních ID na soubory, líné načítání s cache, chybějící ID = tvrdá chyba, chybějící soubor ve vývoji = viditelný placeholder (FR-050, `contracts/asset-manifest.md`)
- [ ] T018 [P] Napsat `tests/unit/test_asset_registry.py` na obě chybová chování a na cache
- [ ] T019 Vytvořit `src/alzak/data/schema.py` — deklarativní schéma dle `contracts/level.schema.json` a výjimku `LevelDataError(file, field, reason)`, jen stdlib (research R5)
- [ ] T020 Vytvořit `src/alzak/data/loader.py` — **jeden** loader pro všechna prostředí, strukturální i sémantická validace dle `contracts/level-format.md`; validace vynutí, že každé prostředí obsahuje plošiny, propast, jednu instanci protivníka, startovní pozici a východ (FR-043, FR-047)
- [ ] T021 Napsat `tests/unit/test_level_loader.py` — chybějící pole, špatný typ, `platform.h < 32`, start nad propastí, trasa protivníka mimo plošinu, neznámé `asset_id`, duplicitní `order` (FR-046, FR-047)

### Aplikace a obrazovky

- [ ] T022 Vytvořit `src/alzak/screens/machine.py` — stavový automat `TITLE·PLAY·PAUSE·TRANSITION·GAMEOVER·FINISH·ERROR`; simulace se posouvá **pouze** v `PLAY` (research R13)
- [ ] T023 Vytvořit `src/alzak/screens/error_screen.py` — chybová obrazovka uvnitř aplikace (soubor + pole + důvod), ovladatelná klávesnicí (FR-084)
- [ ] T024 Vytvořit `src/alzak/app.py` — okno, hlavní smyčka s pevným krokem, dispatch přes `screens/machine.py` (ve fázi F2 jen `TITLE` a `ERROR`; `PLAY` přibude v T054), F11 v každém stavu, zachycení `LevelDataError` na nejvyšší úrovni → chybová obrazovka + `stderr` + `sys.exit(2)` (FR-003, FR-084)
- [ ] T025 Napsat `tests/integration/test_error_screen.py` ověřující zprávu na `stderr` a návratový kód 2 při poškozeném JSON (SC-018)
- [ ] T026 [P] Vytvořit `src/alzak/audio/mixer.py` — hudební smyčka a SFX, při nedostupném zvukovém zařízení přepnutí do no-op režimu bez pádu
- [ ] T027 [P] Napsat `tests/unit/test_audio_fallback.py` ověřující běh bez zvukového zařízení
- [ ] T028 Napsat `tests/unit/test_sim_purity.py` — statická (AST) kontrola, že žádný modul v `src/alzak/sim/` neimportuje `pygame.display`, `pygame.mixer` ani `pygame.font`; ve fázi F2 je adresář ještě prázdný, test proto musí **selhat, když `src/alzak/sim/` neexistuje**, aby od fáze F4 skutečně hlídal (Princip V)

- [ ] T029 **CHECKPOINT Foundational**: spustit celou sadu `pytest`, ověřit `python -m alzak` (prázdná obrazovka), commitnout, vydat handoff a kontextový marker

---

## Fáze F3: Placeholderové assety — vlastník Codex (OD-004)

**Purpose**: Vyrobit verzované placeholdery a manifest. **Herní logika na nich
nezávisí** — fáze 4–7 lze testovat i s prázdným registrem; assety jsou nutné až
pro vizuální ověření a ruční smoke test.

⚠️ **Assetový stop-point.** Claude na tuto fázi upozorní v handoff bloku (OD-004).

- [ ] T030 [OWNER:Codex] Vytvořit `tools/generate_placeholders.py` — deterministický generátor s vlastním PNG zapisovačem (`zlib` + `struct`) a WAV zapisovačem (`wave`), **jen stdlib**, pevné pořadí položek, žádný neseedovaný `random`, žádná časová metadata; režim `--verify` nic nezapisuje (FR-082, SC-017, research R8)
- [ ] T031 [OWNER:Codex] Vygenerovat a **commitnout** všechny obrazové placeholdery do `assets/images/` — Alzák (idle/run/air/hurt), protivník (walk/hit), plošiny pobočky/skladu/kanceláře, propast, východ neaktivní i aktivní, tři pozadí, HUD energie plná/prázdná, rám a výplň ukazatele teploty (FR-049, FR-081, `contracts/asset-manifest.md`)
- [ ] T032 [OWNER:Codex] Vygenerovat a **commitnout** hudební smyčku do `assets/music/` a **přesně pět** zvukových efektů do `assets/sfx/` — pohyb, skok, spuštění laseru, trvání laseru, ukončení laseru (FR-056, FR-058, A-003)
- [ ] T033 [OWNER:Codex] Vytvořit `assets/manifest.json` — stabilní ID → cesta + `sha256` + příznak `generated` pro každou položku dle `contracts/asset-manifest.md` (FR-050)
- [ ] T034 Napsat `tests/unit/test_asset_manifest.py` — všechna povinná ID přítomna, každý soubor existuje, `sha256` souhlasí, počet zvukových efektů je právě 5
- [ ] T035 Napsat `tests/unit/test_placeholder_determinism.py` — `tools/generate_placeholders.py --verify` nezmění ani jeden bajt (SC-017)

- [ ] T036 **CHECKPOINT Assety**: celá sada, vizuální kontrola placeholderů, commit, handoff

---

## Fáze F4: User Story 1 — Průchod jedním prostředím (Priority: P1) 🎯 MVP

**Goal**: Hráč se pohybuje, skáče, laserem porazí protivníka, východ se aktivuje
a vstupem do něj je prostředí dokončeno.

**Independent Test**: Spustit hru přímo v prvním prostředí a projít cyklus
pohyb → skok → laser → poražení → východ. Nevyžaduje menu, další prostředí ani energii.

### Simulace

- [ ] T037 [US1] Vytvořit `src/alzak/sim/events.py` — výčet `SimEvent` dle data-model.md §1.7
- [ ] T038 [US1] Vytvořit `src/alzak/sim/physics.py` — gravitace s omezenou rychlostí pádu, integrace a kolize AABB **po osách** X→Y s posunem na hranu a vynulováním složky rychlosti (FR-013, FR-017, research R3)
- [ ] T039 [US1] Napsat `tests/unit/test_physics.py` — dopad na plošinu, náraz do boku, žádné propadnutí při maximální rychlosti pádu, žádné zaseknutí v rohu
- [ ] T040 [US1] Vytvořit `src/alzak/sim/player.py` — zrychlení a tření po zemi, snížená kontrola ve vzduchu, proměnlivá výška skoku, coyote time, jump buffer, `facing`, `on_ground` (FR-011…FR-019)
- [ ] T041 [US1] Napsat `tests/unit/test_player_movement.py` — dosažení maximální rychlosti, zastavení po uvolnění, obě šipky současně = žádné zrychlení
- [ ] T042 [US1] Napsat `tests/unit/test_player_jump.py` — krátký vs. držený skok, coyote time 90–110 ms, jump buffer 110–130 ms (SC-007)
- [ ] T043 [US1] Vytvořit `src/alzak/sim/enemy.py` — hlídkování mezi dvěma datově definovanými body s otočením na kraji, `hp`, `hit_flash_timer` (FR-035, FR-036, FR-038)
- [ ] T044 [US1] Napsat `tests/unit/test_enemy_patrol.py` — otočení na obou krajních bodech, setrvání v mezích trasy
- [ ] T045 [US1] Vytvořit `src/alzak/sim/laser.py` — muzzle bod z `config.LASER["muzzle_offset"]` zrcadlený podle `facing`, vodorovný pás o `collision_thickness`, `end_x` = nejbližší zásah, stavy `IDLE·FIRING·LOCKED`, ohřev a chlazení (FR-027…FR-034, FR-085…FR-087)
- [ ] T046 [US1] Napsat `tests/unit/test_laser_geometry.py` — start v muzzle bodu, výchozí tloušťka 16 px, konec na nejbližší plošině, plošina mezi hráčem a protivníkem blokuje poškození, paprsek končí na hraně obrazovky (SC-021, US1 scénář 7)
- [ ] T047 [US1] Napsat `tests/unit/test_laser_heat.py` — přehřátí za 1,4–1,6 s, zablokování, opětovná aktivace až pod prahem i při stále drženém X (SC-005, FR-032)
- [ ] T048 [US1] Napsat `tests/unit/test_enemy_defeat.py` — poražení za 0,9–1,1 s souvislého působení **a** za stejný celkový čas při dvou oddělených dávkách (SC-004, SC-020, FR-039)
- [ ] T049 [US1] Vytvořit `src/alzak/sim/level.py` — `LevelState` sestavená vždy z `LevelData` + `config`, pořadí vyhodnocení kroku dle data-model.md §1.5, aktivace východu po poražení protivníka, dokončení vstupem do aktivního východu (FR-040, FR-044, FR-045)
- [ ] T050 [US1] Napsat `tests/unit/test_level_state.py` — neaktivní východ při překryvu nic nedělá, aktivní dokončí prostředí, aktivace nastane jen po poražení
- [ ] T051 [US1] Napsat `tests/unit/test_framerate_independence.py` — shodná výška skoku, dolet a doba přehřátí při simulaci odpovídající 30 a 60 FPS v mezích 5 % (SC-003)

### Data a prezentace

- [ ] T052 [US1] Vytvořit `levels/level_01_pobocka.json` dle `contracts/level-format.md` — jedna pevná obrazovka 1920 × 1080 se statickou kamerou obsahující plošiny, propast, trasu protivníka, startovní pozici, východ a odkazy na asset ID (FR-042, FR-043)
- [ ] T053 [US1] Vytvořit `src/alzak/render/world.py` — vykreslení pozadí, plošin, propasti, hráče, protivníka, východu (dva vizuálně odlišné stavy) a laseru z `draw_*` klíčů konfigurace (FR-044, FR-087)
- [ ] T054 [US1] Vytvořit `src/alzak/screens/play.py` — propojení `InputSnapshot` → simulace → `render/world.py`, R restartuje prostředí (FR-010)
- [ ] T055 [US1] Napsat `tests/integration/test_us1_playthrough.py` — headless průchod: pohyb, skok přes propast, laser, poražení, aktivace východu, dokončení

- [ ] T056 [US1] **CHECKPOINT MVP**: celá sada + ruční smoke test dle quickstart.md §5 bodů 1–4, commit, handoff

---

## Fáze F5: User Story 2 — Přežití, zranění a neúspěch (Priority: P2)

**Goal**: Energie, zásah s odhozením a nezranitelností, pád do propasti,
obrazovka neúspěchu a úplný restart prostředí.

**Independent Test**: V jednom prostředí opakovaně narazit do protivníka a spadnout
do propasti; ověřit odpočet energie, odhození, nezranitelnost, respawn, obrazovku
neúspěchu a restart.

**Depends on**: US1 (F4)

- [ ] T057 [US2] Doplnit do `src/alzak/sim/player.py` energii, `invuln_timer` a odhození dle `config.ENERGY` (FR-020…FR-022)
- [ ] T058 [US2] Doplnit do `src/alzak/sim/level.py` vyhodnocení kontaktu hráč × protivník (FR-037) a pádu do propasti se zachováním stavu protivníka i východu (FR-023, A-002)
- [ ] T059 [US2] Napsat `tests/unit/test_energy.py` — start se 3 body, ztráta právě 1 bodu, nezranitelnost 0,9–1,1 s, druhý dotyk během ní bez účinku, po vypršení další ztráta (SC-006)
- [ ] T060 [US2] Napsat `tests/unit/test_pit_fall.py` — pád odebere 1 bod, vrátí hráče na start, protivník si zachová pozici i utržené poškození, východ si zachová stav
- [ ] T061 [US2] Napsat `tests/unit/test_failure_precedence.py` — poražení protivníka a vyčerpání energie v témže kroku ⇒ přednost má neúspěch, prostředí se nepočítá jako dokončené (A-010)
- [ ] T062 [US2] Vytvořit `src/alzak/screens/gameover.py` s položkami „Opakovat prostředí" a „Ukončit hru" (FR-024, FR-054)
- [ ] T063 [US2] Implementovat úplný restart prostředí v `src/alzak/screens/play.py` a `sim/level.py` — nová `LevelState`: pozice, 3 body energie, vychladlý laser, plně obnovený protivník, neaktivní východ (FR-026)
- [ ] T064 [US2] Napsat `tests/integration/test_level_restart.py` — R i „Opakovat prostředí" obnoví **všech pět** složek počátečního stavu
- [ ] T065 [US2] Napsat `tests/integration/test_us2_survival.py` — headless: tři zásahy ⇒ obrazovka neúspěchu; odhození nad propastí vede k normálnímu vyhodnocení pádu

- [ ] T066 [US2] **CHECKPOINT US2**: celá sada + ruční smoke dle quickstart.md §5 bodu 5, commit, handoff

---

## Fáze F6: User Story 3 — Kompletní průchod třemi prostředími (Priority: P3)

**Goal**: Pevné pořadí pobočka → sklad → kancelář, přechody, doplnění energie,
závěrečná obrazovka a restart dema.

**Independent Test**: Odehrát celý průchod od prvního prostředí po závěrečnou
obrazovku a ověřit pořadí, přechody a obnovení energie.

**Depends on**: US1 (F4)

- [ ] T067 [US3] [P] Vytvořit `levels/level_02_sklad.json` dle `contracts/level-format.md` (FR-042, FR-043)
- [ ] T068 [US3] [P] Vytvořit `levels/level_03_kancelar.json` dle `contracts/level-format.md` (FR-042, FR-043)
- [ ] T069 [US3] Vytvořit `src/alzak/sim/session.py` — index prostředí, pevná posloupnost tří, doplnění energie na 3 při vstupu, příznak dokončení dema (FR-025, FR-041)
- [ ] T070 [US3] Napsat `tests/unit/test_session_progression.py` — pořadí prostředí, doplnění energie bez ohledu na předchozí stav, dokončení po třetím
- [ ] T071 [US3] Vytvořit `src/alzak/screens/transition.py` — zatmavení a rozsvícení dle `config.LEVEL["transition_fade_time"]`; Escape stisknutý během přechodu se uplatní až po jeho dokončení (FR-048, Edge Case)
- [ ] T072 [US3] Napsat `tests/integration/test_transition.py` — přechod doběhne konzistentně, Escape během něj nenechá hru v rozbitém stavu, akumulátor se po návratu nedožene dávkou kroků
- [ ] T073 [US3] Vytvořit `src/alzak/screens/finish.py` s položkami „Spustit znovu" a „Ukončit" (FR-055)
- [ ] T074 [US3] Napsat `tests/unit/test_all_levels_load.py` — všechny tři JSON se načtou **stejným** loaderem bez výjimky specifické pro prostředí (SC-008)
- [ ] T075 [US3] Napsat `tests/integration/test_us3_full_run.py` — headless průchod všemi třemi prostředími až na závěrečnou obrazovku a restart dema

- [ ] T076 [US3] **CHECKPOINT US3**: celá sada + ruční průchod celým demem, commit, handoff

---

## Fáze F7: User Story 4 — Ovládání aplikace, HUD a zvuková odezva (Priority: P4)

**Goal**: Úvodní obrazovka, pauza, HUD, F11 a kompletní zvuková vrstva.

**Independent Test**: Projít všechny obrazovky pouze klávesnicí, ověřit každý
prvek HUD a každý zvukový efekt proti odpovídající akci.

**Depends on**: US1, US3 (obrazovky navazují na postup demem)

- [ ] T077 [US4] Vytvořit `src/alzak/screens/title.py` — název dema, „Spustit", „Ukončit"; ovládání pouze klávesnicí (FR-051, FR-005)
- [ ] T078 [US4] Vytvořit `src/alzak/screens/pause.py` — „Pokračovat", „Restartovat prostředí", „Ukončit hru"; simulace zastavena, hudba ztišena na `AUDIO["music_volume_paused"]` (FR-009, FR-053, FR-057)
- [ ] T079 [US4] Implementovat pravidla ukončení aplikace v `src/alzak/screens/pause.py`, `src/alzak/screens/gameover.py`, `src/alzak/screens/title.py`, `src/alzak/screens/finish.py` a `src/alzak/app.py` — „Ukončit hru" v pauze i na obrazovce neúspěchu vrací na úvodní obrazovku; aplikaci ukončí **pouze** „Ukončit" na úvodní a závěrečné obrazovce (FR-083)
- [ ] T080 [US4] Napsat `tests/integration/test_exit_rules.py` — FR-083 pro všechny čtyři cesty
- [ ] T081 [US4] Vytvořit `src/alzak/render/hud.py` — tři body energie, ukazatel teploty laseru, název prostředí a pořadí „2/3"; všechny rozměry a barvy z `config.HUD` (FR-033, FR-052)
- [ ] T082 [US4] Napsat `tests/unit/test_hud.py` — HUD čte hodnoty ze stavu, obsahuje všechny čtyři prvky, neobsahuje číselné konstanty
- [ ] T083 [US4] Propojit `src/alzak/audio/mixer.py` se `SimEvent` — hudební smyčka souvislá i přes přechody, zvuk pohybu řízený skutečným pohybem po pevné ploše, zvuky skoku a laseru (FR-056, FR-058, FR-059)
- [ ] T084 [US4] Napsat `tests/integration/test_audio_events.py` — zvuk trvání laseru okamžitě končí při uvolnění X, přehřátí, pauze, vstupu do východu i jakékoli změně stavu obrazovky (FR-060)
- [ ] T085 [US4] Implementovat F11 v `src/alzak/app.py` a `render/presentation.py` — přepnutí v kterémkoli stavu bez změny rozmístění (FR-003)
- [ ] T086 [US4] Napsat `tests/integration/test_us4_screens.py` — headless průchod všemi obrazovkami výhradně klávesnicí

- [ ] T087 [US4] **CHECKPOINT US4**: celá sada + ruční smoke dle quickstart.md §5 bodů 6–8, commit, handoff

---

## Fáze F8: User Story 5 — Spuštění a distribuce (Priority: P5)

**Goal**: Spuštění ze zdroje, lokální buildy pro Windows i macOS a tři artefakty
z jednoho běhu GitHub Actions.

**Independent Test**: Čistý klon → instalace závislostí → spuštění → build →
stažený artefakt spustit a dohrát demo.

**Depends on**: US1–US4 (je co balit)

- [ ] T088 [US5] Vytvořit `packaging/alzak.spec` — režim onedir, `datas` s `assets/` a `levels/`, `excludes` obsahující **`alzak_devtools`**, `pytest` a `PyInstaller`, `console=False` (FR-065, FR-066)
- [ ] T089 [US5] [P] Vytvořit `packaging/build_windows.ps1` — ověření prostředí a volání PyInstalleru
- [ ] T090 [US5] [P] Vytvořit `packaging/build_macos.sh` — ověření prostředí a volání PyInstalleru
- [ ] T091 [US5] Doplnit `.github/workflows/ci.yml` o joby `build-windows` (`windows-latest`), `build-macos-arm` (`macos-14`) a `build-macos-intel` (`macos-13`), všechny s `needs: test`, každý nahrávající pojmenovaný artefakt (FR-064, SC-010, `contracts/build-and-ci.md`)
- [ ] T092 [US5] Doplnit do `.github/workflows/ci.yml` běh `tools/generate_placeholders.py --verify` a testy na Windows i macOS runnerech (SC-009, SC-017)
- [ ] T093 [US5] Napsat `tests/unit/test_packaging_spec.py` — `packaging/alzak.spec` skutečně vylučuje `alzak_devtools` a zahrnuje `assets/` i `levels/`
- [ ] T094 [US5] Vytvořit `README.md` s kroky ze `quickstart.md` §2 a §4.6 — spuštění ze zdroje, testy, lokální buildy a postup pro nepodepsaný macOS build (FR-063, A-009)
- [ ] T095 [US5] Ruční ověření staženého artefaktu (`dist/Alzak/` resp. `dist/Alzak.app`) na cílovém systému dle `quickstart.md` §4.6 — dohrát celé demo bez nainstalovaného Pythonu (SC-011); poškozený `levels/level_02_sklad.json` v zabaleném buildu vede k chybové obrazovce a exit kódu 2 (SC-018)

- [ ] T096 [US5] **CHECKPOINT US5**: celá sada, tři artefakty z jednoho běhu CI, commit, handoff

---

## Fáze F9: User Story 6 — Vývojářská zpětná vazba z běžící hry (Priority: P6)

**Goal**: Bootstrap minimum feedback pipeline dle §21.30 v rozsahu OD-001.

**Independent Test**: V development buildu projít logický tok §21.27 v rozsahu,
který pygame adaptér podporuje, a samostatně ověřit, že produkční build nástroj
neobsahuje.

**Depends on**: US1–US5 hotové (priorita P6, OD-001 bod 3 a `spec.md` A-012, potvrzeno OD-006)

⚠️ **Zúžený testovací rozsah** dle OD-001 bodu 2 a `spec.md` A-012 — výslovná výjimka
z Principu VI, zapsaná v `constitution.md`. Runtime závislosti se nepřidávají (A-013).

- [ ] T097 [US6] Vytvořit balíček `alzak_devtools/` s `__init__.py` a `feedback/__init__.py` **mimo** `src/alzak/` (FR-066, research R9)
- [ ] T098 [US6] Vytvořit `alzak_devtools/feedback/overlay.py` — jediná root-level integrace, aktivace klávesou **F8**, viditelný indikátor odlišený od produkčního UI, dostupnost z každé aktivní herní obrazovky (FR-067, FR-068, FR-088)
- [ ] T099 [US6] Doplnit do `src/alzak/app.py` **jediný** střežený import `try: from alzak_devtools.feedback import overlay except ImportError: None`, podmíněný `config.FEEDBACK["enabled"]`
- [ ] T100 [US6] Vytvořit `alzak_devtools/feedback/capture.py` — snímek z **kopie logického surface pořízené před kresbou overlay**; při selhání položka s příznakem `screenshot: "unavailable"` (FR-069, FR-070, research R10)
- [ ] T101 [US6] Vytvořit `alzak_devtools/feedback/annotate.py` — volná tužka, uložení původního i anotovaného obrázku a strukturované vrstvy s normalizovanými souřadnicemi (FR-070, FR-071)
- [ ] T102 [US6] Vytvořit `alzak_devtools/feedback/package.py` dle `contracts/feedback-package.md` — stabilní ID `FB-<UTC_DATE>-<hex12>` (FR-074), kontext dle FR-075, `checksums.json`, atomická publikace přes `os.replace` (FR-077), odmítnutí prázdné zpětné vazby (FR-073), zákaz sběru tajemství a dat jiných aplikací (FR-076), výslovné `audio`/`transcription` = `unavailable` (FR-072)
- [ ] T103 [US6] Vytvořit `alzak_devtools/feedback/queue.py` dle `contracts/feedback-package.md` — stavy `capturing·queued·transferring·synced·transfer_failed`, deduplikace podle stabilního ID, odolnost vůči opakovanému načtení (FR-078)
- [ ] T104 [US6] Vytvořit `alzak_devtools/feedbackctl.py` — operace `doctor·pull·list·show·respond·claim·release·complete·reopen·sync-status·verify` se sémantikou a návratovými kódy dle `contracts/feedbackctl.md`; `complete` bez `--evidence` selže; poškozené položky do `quarantine/` s výslovnou chybou (FR-079, FR-080)
- [ ] T105 [US6] Napsat `tests/devtools/test_production_exclusion.py` — `importlib.util.find_spec("alzak_devtools") is None` v produkčním prostředí a `alzak.spec` balíček vylučuje (SC-014)
- [ ] T106 [US6] Napsat `tests/devtools/test_item_integrity.py` — formát stabilního ID, checksumy a deduplikace; dvojí `pull` nezmění ani bajt důkazního materiálu (SC-016)
- [ ] T107 [US6] Napsat `tests/devtools/test_capture_excludes_control.py` — v uloženém PNG **není** marker barvy indikátoru; ověřeno proti skutečnému souboru (FR-069)
- [ ] T108 [US6] Napsat `tests/devtools/test_pipeline_e2e.py` — jeden end-to-end průchod tokem §21.27 v rozsahu adaptéru; nedostupné kroky výslovně označeny, nikoli přeskočeny (SC-015)
- [ ] T109 [US6] Doplnit do `README.md` klávesu F8, rozsah pygame adaptéru, výslovné degradace (`audio`/`transcription` unavailable) a produkční vyloučení (§21.2 „documented")

- [ ] T110 [US6] **CHECKPOINT US6**: zúžená sada + ověření, že `F8` v produkčním buildu nemá efekt, commit, handoff

---

## Fáze F10: Polish & Cross-Cutting Concerns

**Purpose**: Doladění, ověření všech kritérií úspěchu a uzavření feature.

- [ ] T111 Doladit hodnoty v `src/alzak/config.py` ručním testem — pohyb, skok, laser, protivník; hodnoty musí trvale splňovat SC-003…SC-007 a SC-021 (research R15)
- [ ] T112 Napsat `tests/unit/test_no_magic_numbers.py` — statická kontrola, že `sim/laser.py`, `sim/player.py`, `sim/enemy.py`, `render/world.py` a `render/hud.py` neobsahují číselné herní konstanty (Princip II, SC-021)
- [ ] T113 Projít `quickstart.md` §4 a doložit **každé** SC-001…SC-022 konkrétním důkazem
- [ ] T114 Projít `specs/001-alzak-platformer-demo/checklists/` a vyhodnotit CHK001–CHK128; nálezy zapsat do `analysis-report.md` nebo `open-decisions.md`
- [ ] T115 Spustit `/speckit-converge` nad `specs/001-alzak-platformer-demo/` a odstranit případný rozdíl mezi specifikací a implementací (SC-013)
- [ ] T116 **CHECKPOINT Release**: celá sada na všech třech OS, tři artefakty, ruční průchod dema, závěrečný report dle `AGENTS.md` §19, commit, handoff

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
                     └─ F9  US6 (P6)
                         └─ F10 Polish
```

**Blokující hrany**:

- F2 blokuje **vše** ostatní.
- F3 blokuje ruční smoke testy a SC-012/SC-017, **neblokuje** testy simulace.
- US2 a US3 jsou na sobě nezávislé; obě závisí na US1.
- US4 závisí na US1 a US3 (HUD zobrazuje pořadí prostředí).
- US5 závisí na hotovém herním demu; US6 je poslední (P6).

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
| US6 | Tok §21.27 v dev buildu + důkaz nepřítomnosti v produkčním buildu | F9 |

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
| US6 | T110 | zúžená sada + důkaz produkčního vyloučení |
| Release | T116 | vše + `converge` + závěrečný report |

Na každém checkpointu platí `CLAUDE.md` §4: spustit validaci, aktualizovat tasks,
prohlédnout diff, commitnout (OD-003), ohlásit odchylky a **zastavit**, není-li
další checkpoint výslovně autorizován.

## Souhrn

| Ukazatel | Hodnota |
|----------|---------|
| Celkem úkolů | **116** (T001–T116) |
| Setup | 6 (T001–T006) |
| Foundational | 23 (T007–T029) |
| Fáze assetů | 7 (T030–T036), z toho **4 označené `[OWNER:Codex]`** (T030–T033) |
| US1 (P1, MVP) | 20 (T037–T056) |
| US2 (P2) | 10 (T057–T066) |
| US3 (P3) | 10 (T067–T076) |
| US4 (P4) | 11 (T077–T087) |
| US5 (P5) | 9 (T088–T096) |
| US6 (P6) | 14 (T097–T110) |
| Polish | 6 (T111–T116) |
| Testovací úkoly | 39 |
| Checkpointy | 9 |
