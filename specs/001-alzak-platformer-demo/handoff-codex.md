# Handoff — feature 001-alzak-platformer-demo

**Aktualizováno**: 2026-09-03 · Codex (`implement` → OD-008 → `converge` → OD-009)
**Autorita**: rozcestník a stav; požadavky jsou v `spec.md`, rozhodnutí v
`open-decisions.md` a provedená práce v `tasks.md`.

## Stav

| Položka | Hodnota |
|---------|---------|
| Branch | `001-alzak-platformer-demo` |
| Validovaný CI HEAD | `af5a5d2` (`ci: trigger Windows executable build`) |
| Aktivní feature | `specs/001-alzak-platformer-demo/` |
| Dokončeno | F1–F8; hratelné MVP; OD-008 T117–T125; T111–T115; T096; OD-009 T126; čistý `converge`; ruční dohrání macOS balíčku; CI na třech OS |
| Vyřazeno | vývojářská feedback pipeline, US6 a T097–T110 (OD-007) |
| Zakázáno | merge, rebase a změna branche; push byl jednorázově výslovně autorizován pro OD-009 |
| Artefakty | lokální `dist/Alzak.app`; stažený `build/windows-exe/Alzak.exe` (Windows x64) |

Aktuální HEAD a pracovní strom je nutné při převzetí ověřit přes
`git log -1 --oneline` a `git status --short`; tento dokument se aktualizuje
před finálním commitem a nemá nahrazovat Git.

## Implementovaný výsledek

- Python 3.12 + pygame-ce, logický obraz 1920 × 1080, pevný simulační krok 1/120 s.
- Tři datově načítaná prostředí: pobočka → sklad → kancelář; kompletní menu,
  pauza, neúspěch, přechody, závěr, HUD, hudba a pět SFX.
- Profilový Alzák ze společného transparentního ImageGen atlasu: idle, mrknutí,
  tři fáze běhu, skok, střelba a zásah; zrcadlení podle směru.
- Viditelná laserová pistole, muzzle v centrální konfiguraci, 16px kolizní pás,
  konečný dosah 900 px, první překážka/protivník a přehřívání.
- Tři odlišná stylizovaná high-poly ImageGen pozadí. Plošiny jsou kresleny jako
  tenké průhledné konstrukční lávky; vysoká datová kolize se nevykresluje jako blok.
- PyInstaller konfigurace: Windows one-file `Alzak.exe`, macOS onedir bundle;
  GitHub Actions úspěšně ověřilo Windows x64, macOS arm64 a macOS Intel.
  Feedback pipeline je mimo scope dle OD-007.

## Autoritativní artefakty

- `spec.md`: aktivní FR-001…FR-065, FR-081…FR-087 a FR-089…FR-093;
  SC-001…SC-013, SC-017…SC-021 a SC-023…SC-025.
- `open-decisions.md`: OD-007 vylučuje feedback; OD-008 určuje high-poly revizi.
- `open-decisions.md`: OD-009 určuje jediný Windows `Alzak.exe`.
- `plan.md`, `data-model.md`, `contracts/asset-manifest.md`: runtime atlas,
  vizuální offsety a konečný laser.
- `tasks.md`: T097–T110 neaktivní; výtvarná revize T117–T125.
- `quickstart.md`: přesné příkazy a validační scénáře.

## Důkazy závěrečné validace

```text
.venv/bin/python tools/generate_placeholders.py --verify
  PASS — 12 deterministických obrázků, 3 autorská pozadí,
  8 atlasových snímků, 1 hudební smyčka, 5 SFX

SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python -m pytest -q
  PASS — 67 testů

SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy ALZAK_SMOKE_EXIT=1 \
  .venv/bin/python -m alzak
  PASS — exit 0

./packaging/build_macos.sh
  PASS — PyInstaller 6.22.2, macOS ARM64

ALZAK_SMOKE_EXIT=1 dist/Alzak.app/Contents/MacOS/Alzak
  PASS — exit 0, Mach-O arm64, bundle 47 MB

ALZAK_NONINTERACTIVE_ERROR=1 dist/Alzak.app/Contents/MacOS/Alzak
  PASS s poškozenou kopií level_02 — exit 2, stderr obsahuje
  soubor + platforms[0].h + „minimum je 32“; data buildu poté obnovena

ruční průchod dist/Alzak.app
  PASS — reálné vstupy šipky/mezerník/X, pobočka → sklad → kancelář →
  „DEMO DOKONČENO!“; důkaz build/diagnostics/manual-finish.png

speckit-converge
  PASS — 77 aktivních FR a 21 aktivních SC pokryto, bez nových úkolů;
  tasks.md měl před/po shodný SHA-256

GitHub Actions run 33783162246
  PASS — Linux test gate + Windows x64 + macOS arm64 + macOS Intel; tři artefakty
  z jednoho běhu. Windows artefakt byl stažen a obsahuje jen PE32+ GUI x64
  Alzak.exe (26 MB, SHA-256 3c8a3b8fcef8c38c76e8dc0813595e5745e088a957c8a65c30b4480478f284f5)
```

Diagnostické rendery (gitignored):
`build/diagnostics/highpoly-pobocka.png`, `highpoly-sklad.png`,
`highpoly-kancelar.png`.

## Otevřené externí validační body

- Plný průchod všemi třemi úrovněmi je automaticky ověřen simulací skutečných
  vstupů bez teleportace a ručně ověřen v zabaleném macOS buildu, včetně boje,
  přechodů prostředí, pádu, restartu a závěrečné obrazovky.
- Balíček nebyl spuštěn na čistém stroji bez nainstalovaného Pythonu, proto T095
  a úplný důkaz SC-011 zůstávají otevřené.
- Windows x64, macOS arm64 a macOS Intel CI buildy a testy úspěšně proběhly;
  Windows `.exe` zatím nebyl ručně spuštěn na skutečném Windows stroji.
- macOS build je nepodepsaný a nenotarizovaný (A-009).

## Zbývající pořadí

Implementace, CI a Windows one-file dodávka jsou uzavřené. Případné pokračování
vyžaduje pouze čistý Windows stroj bez Pythonu pro ruční dohrání (T095). Další
push se bez nového výslovného pokynu neprovádí.

## Povinný session handoff

```text
Branch: 001-alzak-platformer-demo
HEAD: af5a5d2 je CI-validovaný commit; aktuální dokumentační HEAD ověřit
  git rev-parse HEAD
Active feature: specs/001-alzak-platformer-demo/
Completed checkpoint: hratelné MVP + OD-008 + čistý converge + OD-009 Windows exe
Authoritative artifacts changed: spec, decisions, plan, data-model,
  asset-manifest contract, quickstart, tasks, tento handoff
Tasks completed: T001–T094, T096, T111–T115, T117–T126; viz tasks.md pro přesný stav
Validation performed: 67 pytest PASS, asset verify PASS, source smoke PASS,
  macOS ARM64 build/smoke/manual full play PASS, invalid packaged JSON exit 2 PASS,
  converge bez mezer PASS, CI Linux/Windows/macOS ARM+Intel PASS, Windows PE x64 PASS
Open blockers/decisions: čistý Windows stroj bez Pythonu pro T095 / úplný SC-011
Uncommitted work: dokumentační záznam CI čeká na commit
Resources intentionally left running: žádné
Next authorized step: předat Alzak.exe; volitelně ručně spustit na čistém Windows
Context: KEEP CURRENT SESSION do commitu dokumentačního záznamu
```
