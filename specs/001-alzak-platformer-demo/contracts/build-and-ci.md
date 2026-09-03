# Kontrakt: buildy a CI

**Vazba**: FR-062…FR-065 · SC-009, SC-010, SC-011, SC-017 · A-009

## Spuštění ze zdrojového kódu (FR-063)

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m alzak
```

## Testy (FR-062, SC-009)

```bash
pytest                              # celá sada, headless
pytest tests/unit                   # bez pygame displeje
```

`tests/conftest.py` nastaví `SDL_VIDEODRIVER=dummy` a `SDL_AUDIODRIVER=dummy`
**před** importem pygame. Sada musí projít na Linuxu, Windows i macOS.

## Lokální buildy (FR-063)

| Platforma | Skript | Výstup |
|-----------|--------|--------|
| Windows | `packaging/build_windows.ps1` | `dist/Alzak.exe` |
| macOS | `packaging/build_macos.sh` | `dist/Alzak.app` |

Oba jen ověří prostředí a zavolají `pyinstaller packaging/alzak.spec`.

## `packaging/alzak.spec`

| Položka | Hodnota | Vazba |
|---------|---------|-------|
| režim | Windows **onefile**; macOS **onedir** | OD-009, research R12 |
| `datas` | `assets/` → `assets/`, `levels/` → `levels/` | FR-065 |
| `excludes` | `pytest`, `PyInstaller`, `_pytest` | vývojové nástroje nejsou v runtime |
| `console` | `False` | FR-084 — chybová obrazovka musí fungovat bez konzole |
| `name` | `Alzak` | |

Balíček obsahuje Python runtime, herní data, JSON prostředí, assety, hudbu
a zvuky (FR-065). Windows onefile je při startu rozbalí do PyInstaller
`_MEIPASS`; macOS je ponechává ve svém onedir bundle. Buildy jsou **nepodepsané
a nenotarizované** (A-009).

## GitHub Actions — `.github/workflows/ci.yml` (FR-064, SC-010)

Jeden běh, čtyři joby:

| Job | Runner | Co dělá | Artefakt |
|-----|--------|---------|----------|
| `test` | `ubuntu-latest` | celá sada headless; **brána** pro build joby | — |
| `build-windows` | `windows-latest` | `pytest` + one-file `pyinstaller` | `alzak-windows-x64` (obsahuje pouze `Alzak.exe`) |
| `build-macos-arm` | `macos-15` | `pytest` + `pyinstaller` | `alzak-macos-arm64` |
| `build-macos-intel` | `macos-15-intel` | `pytest` + `pyinstaller` | `alzak-macos-x86_64` |

Build joby mají `needs: test` — artefakt nikdy nevznikne z červené sady.
Manuální dispatch s `target=windows` spustí jen bránu `test` a Windows job,
jakmile je workflow dostupný na výchozí větvi repozitáře. Pro tento feature běh
se workflow vyvolal push eventem, protože GitHub ruční dispatch workflow mimo
výchozí větev nenabízí.

Job `test` navíc spustí:

- `python tools/generate_placeholders.py --verify` — ověření SC-017 **bez zápisu**;

Generátor placeholderů se v CI **nikdy** nespouští v režimu, který přepisuje
soubory (FR-081).

## Ověření staženého artefaktu (SC-011)

1. Stáhnout artefakt na cílovém systému.
2. Windows: spustit `Alzak.exe`. macOS: Ctrl+klik → Otevřít (Gatekeeper, A-009).
3. Projít celé demo od úvodní po závěrečnou obrazovku **bez nainstalovaného Pythonu**.

## Gitignore (A-014)

```text
build/
dist/
.venv/
__pycache__/
*.pyc
```

Do sdíleného kódu ani konfigurace se **nesmí** zapsat cesta specifická pro stroj
jednoho uživatele (`AGENTS.md` §17).

## Revize runnerů 2026-09-03

Původně plánovaný `macos-13` byl GitHubem vyřazen 4. prosince 2025. Konfigurace
proto používá standardní aktuální labely `macos-15` (arm64) a
`macos-15-intel` (x86_64). Feedback-specifické požadavky odstranilo OD-007.
