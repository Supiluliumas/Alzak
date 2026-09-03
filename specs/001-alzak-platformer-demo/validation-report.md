# Validation report — 001-alzak-platformer-demo

**Datum**: 2026-09-03
**Platforma skutečného běhu**: macOS 26.5 arm64, Python 3.12.13,
pygame-ce 2.5.8, pytest 8.4.2, PyInstaller 6.22.2.

Tento dokument rozlišuje automatický důkaz, lokální smoke a neprovedené ruční
nebo cizí-platformní ověření. Konfigurace sama není důkazem úspěšného buildu.

## Kritéria úspěchu

| SC | Stav | Důkaz / omezení |
|----|------|-----------------|
| SC-001 | částečně | Automatický průchod všech tří úrovní skutečnými vstupy bez teleportace prošel; nezaškolený člověk celé demo ručně nedohrál. |
| SC-002 | neověřeno ručně | Cíl 60 FPS je nakonfigurován; celý průchod nebyl vizuálně profilován. |
| SC-003 | PASS | `test_framerate_independence.py`, pevný krok 1/120 s. |
| SC-004 | PASS | `test_enemy_defeat.py` a integrační průchod. |
| SC-005 | PASS | `test_laser_heat.py`. |
| SC-006 | PASS | `test_energy.py`. |
| SC-007 | PASS | `test_player_jump.py`. |
| SC-008 | PASS | `test_all_levels_load.py`, jediný `load_all_levels`. |
| SC-009 | částečně | Celá sada 67 testů prošla na macOS arm64; Linux, Windows a CI neběžely. |
| SC-010 | neověřeno | Workflow má tři build joby, ale bez pushe nebyl spuštěn. |
| SC-011 | částečně | Lokální `dist/Alzak.app` se spustil bez Pythonu; balíček nebyl ručně dohrán ani ověřen na čistém stroji. |
| SC-012 | PASS strukturálně | Stabilní ID a registr oddělují logiku od cest; `test_asset_registry.py`. |
| SC-013 | čeká | Doplní závěrečný běh `speckit-converge`. |
| SC-017 | PASS | `tools/generate_placeholders.py --verify`, 12 deterministických obrázků + zvuky beze změny; autorská aktiva ověřena checksumem. |
| SC-018 | PASS lokálně | Poškozená kopie JSON v macOS buildu: exit 2 a stderr se souborem, polem `platforms[0].h` a důvodem; `test_error_screen.py` ověřuje obrazovku. Data buildu obnovena. |
| SC-019 | PASS automaticky | Šest případů `test_presentation.py`; ruční fullscreen nebyl dokončen. |
| SC-020 | PASS | `test_enemy_defeat.py`, kumulativní poškození. |
| SC-021 | PASS | `test_laser_geometry.py` + `test_no_magic_numbers.py`. |
| SC-023 | PASS | Osm ID se společným transparentním atlasem, manifest test a registry crop test. |
| SC-024 | PASS | `test_every_elevated_platform_is_reachable_by_jumping` pro všechny tři úrovně, pouze vstupy. |
| SC-025 | PASS | `test_beam_range_is_finite_and_clamped_to_screen`, výchozí dosah 900 px. |

## Provedené příkazy

```text
.venv/bin/python tools/generate_placeholders.py --verify
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python -m pytest -q
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy ALZAK_SMOKE_EXIT=1 .venv/bin/python -m alzak
./packaging/build_macos.sh
ALZAK_SMOKE_EXIT=1 dist/Alzak.app/Contents/MacOS/Alzak
ALZAK_NONINTERACTIVE_ERROR=1 dist/Alzak.app/Contents/MacOS/Alzak
file dist/Alzak.app/Contents/MacOS/Alzak
du -sh dist/Alzak.app
git diff --check
```

## Vizuální důkaz

Vykreslení všech tří runtime scén bylo zkontrolováno v logickém rozlišení
1920×1080. Diagnostiky jsou gitignored a zůstávají lokálně v
`build/diagnostics/highpoly-{pobocka,sklad,kancelar}.png`.

## Neprovedeno

- ruční dohrání člověkem/CUA (driver neposkytl spolehlivé držení šipky);
- lokální Windows x64 a macOS Intel build;
- GitHub Actions a tři stažené artefakty;
- podepsání/notarizace macOS aplikace (mimo scope A-009).
