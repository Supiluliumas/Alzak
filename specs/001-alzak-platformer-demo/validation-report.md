# Validation report — 001-alzak-platformer-demo

**Datum**: 2026-09-03
**Platforma skutečného běhu**: macOS 26.5 arm64, Python 3.12.13,
pygame-ce 2.5.8, pytest 8.4.2, PyInstaller 6.22.2.

Tento dokument rozlišuje automatický důkaz, lokální smoke, skutečné ruční
dohrání a neprovedené cizí-platformní ověření. Konfigurace sama není důkazem
úspěšného buildu.

## Kritéria úspěchu

| SC | Stav | Důkaz / omezení |
|----|------|-----------------|
| SC-001 | PASS lokálně | Skutečný zabalený macOS build byl ručně dohrán reálnými vstupy přes pobočku, sklad a kancelář až na závěrečnou obrazovku; automatický průchod bez teleportace také prošel. |
| SC-002 | částečně | Celý ruční průchod byl vizuálně plynulý bez zjevného trhání; 60 FPS nebylo instrumentovaně změřeno. |
| SC-003 | PASS | `test_framerate_independence.py`, pevný krok 1/120 s. |
| SC-004 | PASS | `test_enemy_defeat.py` a integrační průchod. |
| SC-005 | PASS | `test_laser_heat.py`. |
| SC-006 | PASS | `test_energy.py`. |
| SC-007 | PASS | `test_player_jump.py`. |
| SC-008 | PASS | `test_all_levels_load.py`, jediný `load_all_levels`. |
| SC-009 | PASS | GitHub Actions běh 33783162246 úspěšně provedl testovou bránu na Linuxu a celou sadu také na Windows x64, macOS arm64 i macOS Intel. |
| SC-010 | PASS | GitHub Actions běh 33783162246 vytvořil v jednom běhu Windows x64, macOS arm64 a macOS Intel artefakt. |
| SC-011 | částečně | Lokální `dist/Alzak.app` byl přímo spuštěn a celý dohrán přes zabalený runtime; čistý stroj bez instalace Pythonu nebyl k dispozici. |
| SC-012 | PASS strukturálně | Stabilní ID a registr oddělují logiku od cest; `test_asset_registry.py`. |
| SC-013 | PASS | Závěrečný `speckit-converge` nenašel žádnou mezeru a nezměnil `tasks.md` (SHA-256 před/po shodný). |
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
gh run view 33783162246 --json jobs
gh run download 33783162246 -n alzak-windows-x64 -D build/windows-exe
file build/windows-exe/Alzak.exe
```

GitHub Actions [běh 33783162246](https://github.com/Supiluliumas/Alzak/actions/runs/33783162246)
pro commit `af5a5d2` skončil `success`: Linux test gate, Windows x64,
macOS arm64 a macOS Intel. Artefakt `alzak-windows-x64` měl jediný soubor
`Alzak.exe`; po stažení je `PE32+ executable (GUI) x86-64`, 26 MB,
SHA-256 `3c8a3b8fcef8c38c76e8dc0813595e5745e088a957c8a65c30b4480478f284f5`.
Veřejný prerelease [v0.1.0-demo](https://github.com/Supiluliumas/Alzak/releases/tag/v0.1.0-demo)
publikuje stejný jediný asset `Alzak.exe`.

## Vizuální důkaz

Vykreslení všech tří runtime scén bylo zkontrolováno v logickém rozlišení
1920×1080. Diagnostiky jsou gitignored a zůstávají lokálně v
`build/diagnostics/highpoly-{pobocka,sklad,kancelar}.png`.

Skutečný zabalený build byl následně ručně dohrán klávesami šipky, mezerník a
X přes všechny tři úrovně. Závěrečná obrazovka je zachycena v gitignored
`build/diagnostics/manual-finish.png`; průběžné snímky `manual-level1.png`,
`manual-level2.png` a `manual-level3.png` dokládají navazující prostředí.

## Neprovedeno

- ověření balíčku na čistém stroji bez instalace Pythonu;
- ruční spuštění a dohrání Windows `.exe` na skutečném Windows stroji;
- podepsání/notarizace macOS aplikace (mimo scope A-009).
