# Handoff — feature 001-alzak-platformer-demo

**Aktualizováno**: 2026-09-03 · Codex (`implement` → výtvarná revize OD-008)
**Autorita**: rozcestník a stav; požadavky jsou v `spec.md`, rozhodnutí v
`open-decisions.md` a provedená práce v `tasks.md`.

## Stav

| Položka | Hodnota |
|---------|---------|
| Branch | `001-alzak-platformer-demo` |
| Výchozí HEAD revize OD-008 | `304324a` (`test: prove complete level traversability`) |
| Aktivní feature | `specs/001-alzak-platformer-demo/` |
| Dokončeno | F1–F8; implementace herního MVP; výtvarná revize OD-008 T117–T123 |
| Vyřazeno | vývojářská feedback pipeline, US6 a T097–T110 (OD-007) |
| Zakázáno | push, merge, rebase a změna branche |
| Lokální build | `dist/Alzak.app`, nepodepsaný ARM64 macOS onedir bundle |

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
- PyInstaller konfigurace, lokální skripty pro Windows/macOS a GitHub Actions
  konfigurace pro Windows x64, macOS arm64 a macOS Intel. CI se nespouštělo,
  protože zadavatel zakázal push; feedback pipeline je mimo scope dle OD-007.

## Autoritativní artefakty

- `spec.md`: aktivní FR-001…FR-065, FR-081…FR-087 a FR-089…FR-093;
  SC-001…SC-013, SC-017…SC-021 a SC-023…SC-025.
- `open-decisions.md`: OD-007 vylučuje feedback; OD-008 určuje high-poly revizi.
- `plan.md`, `data-model.md`, `contracts/asset-manifest.md`: runtime atlas,
  vizuální offsety a konečný laser.
- `tasks.md`: T097–T110 neaktivní; výtvarná revize T117–T125.
- `quickstart.md`: přesné příkazy a validační scénáře.

## Důkazy validace před finálním converge

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
```

Diagnostické rendery (gitignored):
`build/diagnostics/highpoly-pobocka.png`, `highpoly-sklad.png`,
`highpoly-kancelar.png`.

## Otevřené validační body

- Plný průchod všemi třemi úrovněmi je automaticky ověřen simulací skutečných
  vstupů bez teleportace, včetně dosažitelnosti každé zvýšené plošiny.
- Ruční dohrání přes CUA nebylo dokončeno: dostupné rozhraní umí jednotlivý
  textový vstup, ale neposkytlo spolehlivé držení směrové klávesy. Tento bod se
  nesmí označit za ručně ověřený, dokud jej člověk nebo vhodný UI driver nedohraje.
- Windows, macOS Intel a GitHub Actions nebyly na tomto stroji spuštěny. Existuje
  jen konfigurace; úspěch těchto platforem se nesmí tvrdit bez běhu.
- macOS build je nepodepsaný a nenotarizovaný (A-009).

## Zbývající pořadí

1. Označit T123/T124 podle uložených důkazů a uzavřít checkpoint T125.
2. Vyhodnotit aktivní checklisty; feedback checklist je historický a vyřazen OD-007.
3. Spustit `speckit-converge`; během converge je jediným povoleným zápisem
   append nových úkolů do `tasks.md`. Pokud je výsledek čistý, soubor zůstane
   byte-identický.
4. Opakovat plnou sadu, asset verify, source smoke a packaged smoke.
5. Commitnout úzce zaměřený checkpoint. Neprovádět push.

## Povinný session handoff

```text
Branch: 001-alzak-platformer-demo
HEAD: ověřit git rev-parse HEAD (před OD-008 byl 304324a)
Active feature: specs/001-alzak-platformer-demo/
Completed checkpoint: implementované MVP + OD-008, finální gate probíhá
Authoritative artifacts changed: spec, decisions, plan, data-model,
  asset-manifest contract, quickstart, tasks, tento handoff
Tasks completed: T001–T094, T112, T117–T123; viz tasks.md pro přesný stav
Validation performed: 67 pytest PASS, asset verify PASS, source smoke PASS,
  macOS ARM64 build/smoke PASS, invalid packaged JSON exit 2 PASS
Open blockers/decisions: ruční dohrání; neběžely Windows/macOS Intel/CI
Uncommitted work: ověřit git status; výtvarná revize čeká na checkpoint commit
Resources intentionally left running: žádné
Next authorized step: checklist → converge → finální validace → lokální commit
Context: KEEP CURRENT SESSION do dokončení converge a checkpoint commitu
```
