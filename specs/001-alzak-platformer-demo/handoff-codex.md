# Handoff pro Codex — feature 001-alzak-platformer-demo

**Vytvořeno**: 2026-09-03 · Claude (fáze `plan` → `checklist` → `tasks` → `analyze`)
**Určeno pro**: Codex jako implementátora fáze `implement`
**Autorita**: Tento dokument **nenahrazuje** repozitář. Neobsahuje jediný požadavek,
který by neexistoval jinde (`AGENTS.md` §15.9). Je to rozcestník a stav, ne specifikace.

---

## 1. Přesný stav projektu

| Položka | Hodnota |
|---------|---------|
| Branch | `001-alzak-platformer-demo` |
| HEAD | tip branche `001-alzak-platformer-demo`. Poslední **obsahový** commit je `cc155fb` (fáze `analyze`); po něm následují už jen commity tohoto handoffu. Ověř `git log --oneline -5`. |
| Pracovní strom | **čistý**, žádná nezacommitovaná práce |
| Push | **neproveden** — vyžaduje samostatné svolení (OD-003) |
| Dokončené fáze | `constitution` · `specify` · `clarify` · `plan` · `checklist` · `tasks` · `analyze` |
| Další autorizovaný krok | **`/speckit-implement`, fáze F1 Setup** — vyžaduje výslovnou autorizaci zadavatele |
| Zdrojový kód | **žádný zatím neexistuje** — repozitář obsahuje pouze governance a Spec Kit artefakty |

### Co v repozitáři je

```text
AGENTS.md · CLAUDE.md · feedback_pipeline_standalone.md   ← projektové řády, ZÁVAZNÉ
.specify/memory/constitution.md                           ← ústava v1.1.1
specs/001-alzak-platformer-demo/
├── spec.md              88 FR · 22 SC · 14 A · 6 user stories
├── open-decisions.md    OD-001…OD-006, všechna `decided`
├── analysis-report.md   audit MD↔artefakty + výsledek fáze `analyze`
├── plan.md              architektura, Constitution Check, fáze F1…F10, rizika
├── research.md          R1…R15, všechny technické neznámé uzavřené
├── data-model.md        entity, stavové diagramy, ÚPLNÝ výčet konfiguračních klíčů
├── contracts/           7 kontraktů (schéma prostředí, manifest, ovládání, feedback, build)
├── checklists/          CHK001…CHK128 ve třech doménách
├── tasks.md             T001…T116, 9 checkpointů
└── handoff-codex.md     tento soubor
```

### Co v repozitáři NENÍ

`src/`, `tests/`, `tools/`, `packaging/`, `levels/`, `assets/`, `alzak_devtools/`,
`pyproject.toml`, `README.md`, `.github/workflows/` — vše vytváří fáze `implement`.

---

## 2. Než sáhneš na kód

Povinné pořadí dle `CLAUDE.md` §2 a `AGENTS.md` §3.1:

1. přečti `AGENTS.md`;
2. `git status --short`, branch, HEAD;
3. přečti `.specify/memory/constitution.md` — zejména principy I–VII a Git policy;
4. aktivní feature = `001-alzak-platformer-demo`;
5. přečti `tasks.md` a artefakty potřebné **pro aktuální fázi**, ne všechny;
6. zkontroluj stav úkolů a blokery;
7. **feedback pipeline zatím neexistuje** — start-of-session protokol nespouštěj
   a **hlas jej jako nedostupný**; netvrď, že přezkum zpětné vazby proběhl
   (§21.16, `constitution.md`);
8. před buildem, testem se simulátorem nebo generováním dat ověř prerekvizity
   úložiště (`AGENTS.md` §17; pro tento projekt platí generické chování — A-014).

---

## 3. Pořadí úkolů

Autoritativní zdroj je [tasks.md](./tasks.md). Zde jen mapa.

| Fáze | Úkoly | Obsah | Checkpoint |
|------|-------|-------|------------|
| **F1** Setup | T001–T006 | repo skeleton, `pyproject.toml`, `conftest.py`, CI kostra | — |
| **F2** Foundational | T007–T029 | `config.py`, `paths.py`, `core/`, prezentace, text, registr assetů, schéma + loader, stavový automat, chybová obrazovka, `app.py`, audio | **T029** |
| **F3** Assety | T030–T036 | generátor, obrázky, hudba, SFX, manifest | **T036** ⚠️ assetový |
| **F4** US1 (P1) | T037–T056 | fyzika, hráč, protivník, laser, prostředí 1, východ | **T056** 🎯 MVP |
| **F5** US2 (P2) | T057–T066 | energie, zásah, nezranitelnost, propast, neúspěch, restart | **T066** |
| **F6** US3 (P3) | T067–T076 | prostředí 2 a 3, postup, přechody, závěr | **T076** |
| **F7** US4 (P4) | T077–T087 | úvodní obrazovka, pauza, HUD, F11, hudba, 5 SFX | **T087** |
| **F8** US5 (P5) | T088–T096 | PyInstaller, build skripty, CI, 3 artefakty | **T096** |
| **F9** US6 (P6) | T097–T110 | feedback vrstva + `feedbackctl` + minimum testů | **T110** |
| **F10** Polish | T111–T116 | doladění konfigurace, ověření SC, `converge` | **T116** |

**Blokující hrany**

- **F2 blokuje vše.** Bez konfigurace, prezentační vrstvy a loaderu nezačínej žádnou user story.
- **F3 blokuje** ruční smoke testy, SC-012 a SC-017 — **neblokuje** testy simulace.
  Fáze F4–F7 lze testovat i s prázdným registrem assetů.
- US2 a US3 jsou na sobě nezávislé; obě závisí na US1.
- US4 závisí na US1 i US3 (HUD ukazuje pořadí prostředí „2/3").
- US5 až po hotovém herním demu. **US6 je poslední** (P6, potvrzeno OD-006).

**MVP** = T001–T056.

**Paralelizovatelné**: T003+T004+T005 · T008–T012 · T015+T016 · T026+T027 ·
T067+T068 · T089+T090.

---

## 4. Testovací checkpointy

Na každém checkpointu platí `CLAUDE.md` §4:
**validace → aktualizace tasks → prohlédnutí diffu → commit (OD-003) →
hlášení odchylek → ZASTAVIT**, není-li další checkpoint výslovně autorizován.

| Checkpoint | Úkol | Rozsah validace |
|------------|------|-----------------|
| Foundational | T029 | celá sada `pytest` + `python -m alzak` (prázdná obrazovka) |
| Assety | T036 | celá sada + vizuální kontrola placeholderů + SC-017 |
| **MVP (US1)** | T056 | celá sada + ruční smoke `quickstart.md` §5 body 1–4 |
| US2 | T066 | celá sada + ruční smoke bod 5 |
| US3 | T076 | celá sada + ruční průchod celým demem |
| US4 | T087 | celá sada + ruční smoke body 6–8 |
| US5 | T096 | celá sada na Linuxu/Windows/macOS + 3 artefakty z jednoho běhu CI |
| US6 | T110 | zúžená sada dle OD-001 bodu 2 + důkaz produkčního vyloučení |
| Release | T116 | vše + `/speckit-converge` + závěrečný report dle `AGENTS.md` §19 |

**Princip VI je NON-NEGOTIABLE**: po každé funkci přidej nebo uprav jeden malý test,
spusť **celou** dosavadní sadu, proveď krátký ruční smoke a stručně oznam výsledek.
Commit nesmí zůstat s červenou sadou.

Jediná výjimka: **feedback vrstva (F9)** má zúžený testovací rozsah — test
produkčního vyloučení, jeden end-to-end test a minimální jednotkové testy ID,
checksumů a deduplikace. Výjimka je zapsána v `constitution.md` a v OD-001 bodu 2.

---

## 5. Assetová práce — tvoje výhradní odpovědnost (OD-004)

Čtyři úkoly jsou v `tasks.md` označeny `[OWNER:Codex]`:

| Úkol | Předmět | Klíčové omezení |
|------|---------|-----------------|
| **T030** | `tools/generate_placeholders.py` | **jen standardní knihovna** (`zlib`, `struct`, `wave`, `hashlib`); vlastní PNG a WAV zapisovač; pevné pořadí položek; žádný neseedovaný `random`; žádná časová metadata; režim `--verify` nic nezapisuje |
| **T031** | všechny obrazové placeholdery | 19 ID dle `contracts/asset-manifest.md`, **commitnuté** do `assets/images/` |
| **T032** | hudba + **přesně 5** zvukových efektů | `assets/music/`, `assets/sfx/`; pohyb, skok, laser start, laser loop, laser end (A-003 — žádný zvuk zásahu ani ztráty energie) |
| **T033** | `assets/manifest.json` | stabilní ID → cesta + `sha256` + `generated` |

**Dvě pravidla, která se snadno poruší**

1. **FR-081**: hra assety za běhu **negeneruje**. Generátor není součástí herního
   toku, buildu ani povinného kroku CI. CI ho smí spustit **pouze** s `--verify`.
2. **FR-082 + SC-017**: opakovaný běh nad nezměněným vstupem musí dát **bajtově
   shodné** soubory. Proto stdlib, ne `pygame.image.save` ani Pillow (research R8).

Nikdy assetový krok tiše nepřeskakuj. Na assetovém stop-pointu (F3) to výslovně
oznam v handoff bloku.

---

## 6. Rizika

| ID | Riziko | Kdy udeří | Zmírnění |
|----|--------|-----------|----------|
| **RP-01** | Vestavěný pygame font `freesansbold.ttf` nemusí pokrýt `ě š č ř ž ů ď ť ň`. | T016 ve fázi F2 | `render/text.py` má jediné místo výběru fontu. Selže-li test glyfů, přibal font jako asset s ID `font.ui` a `generated: false`. Je to **assetová práce**. |
| **RP-02** | Bajtová shoda generátoru při použití knihovny třetí strany. | T030 | Jen stdlib. Nepoužívej `pygame.image.save` — bajty závisí na verzi SDL_image a SC-017 by bylo mimo tvou kontrolu. |
| **RP-03** | GitHub runner `macos-13` (x86_64) může být zrušen. | T091 | Pin na konkrétní label; alternativa `--target-arch x86_64` je zdokumentovaná, ale **netestovaná**. Nehlas ji jako funkční bez důkazu. |
| **RP-04** | Rozsah US6 je srovnatelný s celým herním demem. | F9 | Drž se OD-001 bodu 1: každá z 9 položek §21.30 v **nejmenším vyhovujícím** rozsahu. Žádná rozšíření. |
| **RP-05** | Tunelování kolizí při vysoké rychlosti pádu. | T038 | `SIM_DT = 1/120 s` + `max_fall_speed = 1500` + schéma vynucuje `platform.h >= 32`. Nezvyšuj rychlost pádu bez přepočtu. |
| **RP-06** | Gatekeeper blokuje nepodepsaný macOS build. | T095 | A-009 to přijímá. Postup otevření je v `quickstart.md` §4.6. |

---

## 7. Uzavřená rozhodnutí, která NESMÍŠ obejít

| Rozhodnutí | Kde |
|------------|-----|
| Laser začíná v **konfigurovatelném muzzle bodu**, ne v rozměrech sprite | FR-085, OD-006 |
| Výchozí **kolizní tloušťka 16 px**, oddělená od vykreslovací tloušťky | FR-086, OD-006 |
| **Geometrie i vzhled laseru** v `config.py`, žádné magic numbers | FR-087, SC-021, OD-006 |
| Feedback nástroj na klávese **F8** | FR-088, SC-022, OD-006 |
| **US6 zůstává P6** — až po US1–US5 | OD-006, OD-001 bod 3 |
| Placeholdery **verzované** a generátor **deterministický** | FR-081, FR-082, A-005 |
| Assetovou práci dělá **Codex**, výslovně označenou | OD-004 |
| Commit na checkpointech je autorizován, **push není** | OD-003 |
| Škálování **oběma směry** + letterbox i pillarbox | FR-002, OD-005 |
| Runtime závislost **výhradně `pygame-ce`** | Constitution → Technology Constraints |

---

## 8. Pravidla, na kterých projekt stojí

- **Nevymýšlej materiální produktová ani architektonická rozhodnutí, jen abys mohl
  pokračovat** (`CLAUDE.md` §12). Narazíš-li na skutečnou mezeru: zastav **pouze
  dotčenou cestu**, zapiš ji do `open-decisions.md`, vysvětli důsledky a zeptej se.
- **Neupravuj `spec.md` proto, aby ospravedlnil náhodnou implementaci.**
- **Neoslabuj** `AGENTS.md`, `CLAUDE.md`, `feedback_pipeline_standalone.md`
  ani ústavu. Při rozporu rozhoduje Instruction Precedence, konflikt se pojmenuje.
- **Úspěch se netvrdí bez důkazu** (`AGENTS.md` §7). Neproběhlá nebo nedostupná
  validace se hlásí výslovně včetně důvodu.
- **Hygiena kontextu nikdy nezakládá právo commitovat ani pushovat**
  (`CLAUDE.md` §13).
- Na každém checkpointu vydej **handoff blok** a **právě jeden** kontextový marker
  (`CLAUDE.md` §8 a §9).

---

## 9. Otevřené otázky

**Žádné.** OD-001…OD-006 jsou všechna `decided`. Fáze `analyze` proběhla dvakrát;
druhý běh je čistý: 0 nepokrytých FR, 0 nepokrytých SC, 0 kontraktů bez odkazu,
0 modulů bez úkolu, žádné porušení principu ústavy.
