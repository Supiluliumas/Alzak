# Kontrakt: buildy a CI

**Vazba**: FR-062…FR-065 · SC-009, SC-010, SC-011, SC-014, SC-017 · A-009, A-014

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
pytest tests/devtools               # feedback vrstva (US6)
```

`tests/conftest.py` nastaví `SDL_VIDEODRIVER=dummy` a `SDL_AUDIODRIVER=dummy`
**před** importem pygame. Sada musí projít na Linuxu, Windows i macOS.

## Lokální buildy (FR-063)

| Platforma | Skript | Výstup |
|-----------|--------|--------|
| Windows | `packaging/build_windows.ps1` | `dist/Alzak/Alzak.exe` |
| macOS | `packaging/build_macos.sh` | `dist/Alzak.app` |

Oba jen ověří prostředí a zavolají `pyinstaller packaging/alzak.spec`.

## `packaging/alzak.spec`

| Položka | Hodnota | Vazba |
|---------|---------|-------|
| režim | **onedir** | research R12 |
| `datas` | `assets/` → `assets/`, `levels/` → `levels/` | FR-065 |
| `excludes` | **`alzak_devtools`**, `pytest`, `PyInstaller`, `_pytest` | **FR-066, SC-014** |
| `console` | `False` | FR-084 — chybová obrazovka musí fungovat bez konzole |
| `name` | `Alzak` | |

Balíček obsahuje Python runtime, herní data, JSON prostředí, assety, hudbu
a zvuky (FR-065). Buildy jsou **nepodepsané a nenotarizované** (A-009).

## GitHub Actions — `.github/workflows/ci.yml` (FR-064, SC-010)

Jeden běh, čtyři joby:

| Job | Runner | Co dělá | Artefakt |
|-----|--------|---------|----------|
| `test` | `ubuntu-latest` | celá sada headless; **brána** pro build joby | — |
| `build-windows` | `windows-latest` | `pytest` + `pyinstaller` | `alzak-windows-x64` |
| `build-macos-arm` | `macos-14` | `pytest` + `pyinstaller` | `alzak-macos-arm64` |
| `build-macos-intel` | `macos-13` | `pytest` + `pyinstaller` | `alzak-macos-x86_64` |

Build joby mají `needs: test` — artefakt nikdy nevznikne z červené sady.

Job `test` navíc spustí:

- `python tools/generate_placeholders.py --verify` — ověření SC-017 **bez zápisu**;
- `pytest tests/devtools/test_production_exclusion.py` — ověření SC-014.

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
feedback-store/
.venv/
__pycache__/
*.pyc
```

Do sdíleného kódu ani konfigurace se **nesmí** zapsat cesta specifická pro stroj
jednoho uživatele (`AGENTS.md` §17).
