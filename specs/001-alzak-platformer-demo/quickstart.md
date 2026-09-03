# Quickstart & validační příručka

**Feature**: `001-alzak-platformer-demo` | **Date**: 2026-09-03
**Účel**: spustitelné scénáře, které **prokáží**, že demo funguje. Nikoli návod
k implementaci — ten je v [tasks.md](./tasks.md).

---

## 1. Předpoklady

| Položka | Verze | Ověření |
|---------|-------|---------|
| Python | 3.12 | `python3.12 --version` |
| Git | libovolná | `git --version` |
| Volné místo | ~2 GB (venv + buildy) | `df -h .` |

**Před buildem, testem se simulátorem nebo generováním dat** ověř
prerekvizity úložiště podle `AGENTS.md` §17 a `CLAUDE.md` §2 bodu 8.
Pro tento projekt platí generické chování: `build/` a `dist/` jsou repo-local
a gitignorované.

---

## 2. Spuštění ze zdrojového kódu

```bash
git clone <repo> && cd Alzak
python3.12 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m alzak
```

**Očekávaný výsledek**: okno 1280×720, úvodní obrazovka s názvem dema,
položkami „Spustit" a „Ukončit", ovladatelná pouze klávesnicí.

---

## 3. Testy

```bash
pytest                       # celá sada, headless (Princip VI)
pytest tests/unit -q         # simulace bez pygame displeje
pytest tests/integration -q  # obrazovky, průchod prostředím
```

Sada musí projít **na Linuxu, Windows i macOS** (SC-009). Commit nesmí zůstat
s červenou sadou (Princip VI).

---

## 4. Validační scénáře

Každý scénář je ruční nebo automatické ověření **jednoho kritéria úspěchu**.
Sloupec „Jak" říká, čím se ověřuje.

### 4.1 Herní jádro

| SC | Scénář | Jak |
|----|--------|-----|
| SC-001 | Nezasvěcený hráč projde tři prostředí od úvodní po závěrečnou obrazovku jen klávesnicí, bez instrukcí. | ruční, jeden nezaškolený tester |
| SC-002 | Během celého průchodu 60 FPS bez viditelného trhání. | ruční + volitelný FPS výpis v dev buildu |
| SC-003 | Výška skoku, dolet a doba přehřátí jsou shodné v mezích 5 % při 30 i 60 FPS. | automat: simulace N kroků `SIM_DT` vs. simulace s uměle zdvojeným `dt` snímku |
| SC-004 | Protivník poražen za 0,9–1,1 s souvislého laseru. | automat: `hp / (dps)` a integrační test |
| SC-005 | Laser se přehřeje po 1,4–1,6 s. | automat: krokování `heat` |
| SC-006 | Nezranitelnost 0,9–1,1 s. | automat |
| SC-007 | Coyote time 90–110 ms; jump buffer přijme skok 110–130 ms před dopadem. | automat |
| SC-020 | Protivník zasažený ve dvou dávkách padne po stejném **celkovém** čase jako při jedné. | automat: 0,4 s + pauza + 0,6 s ⇒ poražen |

### 4.2 Laser — geometrie a konfigurace (OD-006)

| SC | Scénář | Jak |
|----|--------|-----|
| SC-021 | Změna `LASER["muzzle_offset"]` nebo `LASER["collision_thickness"]` v `config.py` změní chování i vykreslení laseru **bez jediné změny v logice nebo vykreslování**. | automat: test parametrizuje config a ověří `start`, `end_x` a zásah; plus statická kontrola, že v `sim/laser.py` a `render/world.py` není číselná konstanta laseru |
| — | Výchozí kolizní tloušťka je **16 px**. | automat: `assert config.LASER["collision_thickness"] == 16` |
| — | Laser končí na plošině mezi hráčem a protivníkem; protivník nedostane poškození. | automat (US1 scénář 7) |

### 4.3 Prezentace a rozlišení

| SC | Scénář | Jak |
|----|--------|-----|
| SC-019 | Na 3840×2160 zabírá obraz maximální plochu při 16:9; na 2560×1080 pillarbox; na 1600×1200 letterbox; herní souřadnice se nemění. | automat: `compute_viewport()` na pěti vstupech (viz `contracts/input-map.md`) + ruční kontrola na skutečném displeji |
| — | F11 přepne fullscreen a rozmístění zůstane nezměněné. | ruční |

### 4.4 Data prostředí

| SC | Scénář | Jak |
|----|--------|-----|
| SC-008 | Všechny tři JSON se načtou **stejným** loaderem bez výjimky specifické pro prostředí. | automat: parametrizovaný test přes `levels/*.json` |
| SC-018 | Záměrně poškozený JSON v **zabaleném buildu bez konzole** vede k viditelné chybové obrazovce (soubor + pole + důvod); aplikace nikdy neskončí tiše. | poloautomat: unit test na `LevelDataError` + **ruční ověření na zabaleném buildu** |

Ruční postup pro SC-018:

```bash
# v rozbaleném dist/ balíčku
python - <<'PY'
import json, pathlib
p = pathlib.Path("levels/level_02_sklad.json")
d = json.loads(p.read_text()); d["platforms"][0]["h"] = 12
p.write_text(json.dumps(d))
PY
./Alzak            # očekáváno: chybová obrazovka + stderr + exit code 2
echo $?            # očekáváno: 2
```

### 4.5 Assety

| SC | Scénář | Jak |
|----|--------|-----|
| SC-012 | Nahrazení libovolného obrázku souborem téhož ID se projeví ve hře bez změny logiky. | ruční: přepsat `assets/images/*.png`, spustit, ověřit |
| SC-017 | Opakované spuštění generátoru nezmění ani jeden bajt. | automat: `python tools/generate_placeholders.py --verify` |

```bash
# ruční varianta SC-017
find assets -type f -exec shasum -a 256 {} \; | sort > /tmp/before.txt
python tools/generate_placeholders.py
find assets -type f -exec shasum -a 256 {} \; | sort > /tmp/after.txt
diff /tmp/before.txt /tmp/after.txt && echo "SC-017 OK"
```

### 4.6 Distribuce

| SC | Scénář | Jak |
|----|--------|-----|
| SC-009 | Celá sada projde headless na Linuxu, Windows i macOS. | CI job `test` + build joby |
| SC-010 | Jeden běh GitHub Actions vytvoří tři stažitelné artefakty. | CI |
| SC-011 | Stažený artefakt se spustí a umožní dokončit demo **bez nainstalovaného Pythonu**. | ruční na čistém stroji |

macOS (nepodepsaný build, A-009): Ctrl+klik na `Alzak.app` → **Otevřít** →
potvrdit dialog Gatekeeperu.

### 4.7 Konzistence artefaktů

| SC | Scénář | Jak |
|----|--------|-----|
| SC-013 | `converge` nenajde nevyřešený rozdíl mezi specifikací a implementací. | `/speckit-converge` ve fázi P9 |

---

## 5. Ruční smoke test (Princip VI, bod 3)

Po každé funkční skupině, do dvou minut:

1. `python -m alzak` → úvodní obrazovka → Spustit.
2. Rozeběhnout se, přeskočit propast, sjet z hrany (coyote), skočit těsně před
   dopadem (buffer).
3. Držet X — laser vyjde z muzzle bodu, končí na první překážce; ukazatel
   teploty roste; po ~1,5 s se zablokuje; pustit, ochladit, znovu vystřelit.
4. Porazit protivníka → východ se rozsvítí → vstoupit → přechod.
5. Narazit do protivníka (energie −1, odhození, blikání), spadnout do propasti
   (energie −1, respawn, protivník si drží poškození).
6. Escape → pauza (hudba ztišena) → Pokračovat. R → úplný restart prostředí.
7. F11 → fullscreen a zpět.
8. Dohrát tři prostředí → závěrečná obrazovka → Spustit znovu → Ukončit.

---

## 6. Nejčastější problémy

| Příznak | Příčina | Řešení |
|---------|---------|--------|
| `pygame.error: No available video device` | chybí displej | `SDL_VIDEODRIVER=dummy` (testy to dělají samy) |
| Hra běží beze zvuku | není zvukové zařízení | očekávané chování, hra nesmí spadnout |
| Otazníky místo diakritiky | font bez českých glyfů | research R14 — přibalit `font.ui` (assetová práce → **Codex**) |
| Chybová obrazovka při startu | nevalidní `levels/*.json` | text uvádí soubor, pole i důvod |
| macOS: „aplikaci nelze otevřít" | nepodepsaný build (A-009) | Ctrl+klik → Otevřít |
| `assets/` prázdné | placeholdery ještě nevygenerovány | `python tools/generate_placeholders.py` (vývojářský krok, **ne** součást běhu hry) |
