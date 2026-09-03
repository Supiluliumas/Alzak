# Alzák: Mise splněna!

Hratelné technologické demo 2D plošinovky v Pythonu 3.12 a pygame-ce. Projděte
obchodní pobočku, logistický sklad a kancelář, v každém prostředí porazte robota
laserem a vstupte do rozsvíceného východu.

## Ovládání

| Klávesa | Akce |
|---|---|
| šipky vlevo/vpravo | pohyb |
| mezerník | skok; držením vyšší |
| X | laser |
| Escape | pauza / pokračovat |
| R | restart prostředí |
| F11 | okno / fullscreen |
| šipky nahoru/dolů + Enter | menu |

## Spuštění ze zdrojového kódu

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/python -m alzak
```

Bez `uv` lze použít standardní `python3.12 -m venv .venv` a
`.venv/bin/pip install -e ".[dev]"`.

## Testy

```bash
.venv/bin/pytest
.venv/bin/python tools/generate_placeholders.py --verify
```

Testy nastavují dummy video i audio ovladač před importem pygame.

## Lokální build

macOS:

```bash
./packaging/build_macos.sh
open dist/Alzak.app
```

Windows PowerShell:

```powershell
.\packaging\build_windows.ps1
.\dist\Alzak.exe
```

Buildy jsou záměrně nepodepsané. Na macOS použijte při prvním spuštění
Ctrl+klik na `Alzak.app`, zvolte **Otevřít** a potvrďte Gatekeeper. PyInstaller
Windows build je jeden soubor `Alzak.exe`; při startu si dočasně rozbalí Python
runtime, tři JSON prostředí, grafiku, hudbu i SFX. macOS zůstává onedir bundle.

GitHub Actions spouští headless testy a vytváří tři artefakty:
`alzak-windows-x64`, `alzak-macos-arm64` a `alzak-macos-x86_64`.

## Placeholdery

Verzované runtime assety generuje čistě standardní knihovnou deterministický
skript `tools/generate_placeholders.py`. Hra jej za běhu ani při buildu nespouští.
ImageGen koncept hrdiny v `assets/source/` je pouze výtvarná reference; hra
používá malé reprodukovatelné sprity z `assets/images/`.
