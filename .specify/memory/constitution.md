# Alzák Platformer Tech Demo Constitution

Závazná pravidla projektu. Nadřazena všem ostatním praktikám v repozitáři.
Vychází z projektového scope (sekce 1–20) dodaného zadavatelem, který je
primárním normativním zdrojem požadavků.

## Core Principles

### I. Scope-First, Demo-Scale (NON-NEGOTIABLE)

Projekt je **technologické demo**, ne produkční hra. Implementuje se přesně to,
co je ve scope — nic víc. Každá funkce mimo scope musí být explicitně schválena
zadavatelem a zapsána do `spec.md`, jinak se neimplementuje.

Konkrétně JE mimo rozsah: checkpointy uvnitř prostředí, více typů protivníků,
scrollující kamera, ukládání postupu, nastavení ovládání, lokalizace,
podepisování buildů, procedurální generování prostředí.

Důsledek: preferuj nejjednodušší funkční řešení. Žádné abstrakce „do budoucna".

### II. Centrální konfigurace ladicích hodnot (NON-NEGOTIABLE)

Každá laditelná herní hodnota — rychlost, zrychlení, tření, gravitace, výška a
délka skoku, coyote time, jump buffer, maximální rychlost pádu, body energie,
délka nezranitelnosti, síla odhození, rychlost zahřívání a ochlazování laseru,
práh opětovné aktivace, DPS laseru, HP a rychlost protivníka, hlasitosti —
je definována v jednom modulu `src/alzak/config.py`.

Zakázáno: číselné herní konstanty (magic numbers) rozeseté v logice entit,
stavů nebo vykreslování. Rozměry a pozice specifické pro jedno prostředí patří
do JSON dat prostředí, ne do konfigurace.

### III. Data-Driven prostředí

Všechna tři prostředí jsou popsána JSON soubory se **společným schématem** a
načítána **jedním** loaderem. Přidání nebo změna prostředí nesmí vyžadovat
změnu herní logiky. Loader validuje schéma a při nevalidním souboru selže
s jasnou, konkrétní chybou (soubor + pole + důvod), nikdy tiše.

### IV. Oddělené vrstvy a nahraditelné assety

Kód je rozdělen minimálně na: spouštění aplikace, konfigurace, herní stavy a
obrazovky, hráč, protivník, fyzika a kolize, laser, načítání prostředí,
uživatelské rozhraní, audio, assety.

Herní pravidla nikdy nesahají na soubory assetů přímo. Veškerý přístup vede
přes centrální registr assetů se **stabilními interními identifikátory**.
Nahrazení placeholderu finální grafikou nebo zvukem se provede výměnou souboru
a jednoho řádku v manifestu — bez zásahu do herní logiky.

### V. Deterministická, testovatelná simulace (NON-NEGOTIABLE)

Herní simulace běží na **pevném časovém kroku** s akumulátorem, odděleně od
vykreslování. Simulační funkce jsou volatelné bez okna a bez zvuku.

Důsledek: fyzika, energie, laser, protivník a postup prostředími jsou
jednotkově testovatelné bez pygame displeje. Testy běží headless
(`SDL_VIDEODRIVER=dummy`, `SDL_AUDIODRIVER=dummy`) a musí projít v CI.

### VI. Test po každé funkci (NON-NEGOTIABLE)

Po každé implementované funkci: (1) přidej nebo uprav jeden malý automatický
test, pokud lze funkci rozumně testovat, (2) spusť celou dosavadní sadu,
(3) proveď krátký ruční smoke test hry, (4) stručně oznam výsledek.

Commit nesmí zůstat s červenou testovací sadou.

### VII. Rozlišení 1920×1080 jako jediný souřadnicový systém

Veškerá herní logika, pozice, rozměry a rychlosti jsou vyjádřeny v logickém
prostoru 1920×1080 (16:9). Zmenšení na menší displeje řeší **výhradně**
prezentační vrstva proporcionálním škálováním s letterboxem. Herní kód nikdy
nečte skutečné rozlišení okna.

## Technology Constraints

Povinný stack, odchylka vyžaduje změnu této ústavy:

- Python 3.12
- pygame-ce (herní běhové prostředí)
- pytest (testy)
- PyInstaller (distribuce)
- JSON (data prostředí a manifest assetů)
- GitHub Actions (automatické testy a buildy)

Runtime závislosti mimo `pygame-ce` se nepřidávají. Standardní knihovna má
přednost. Vývojové závislosti (pytest, PyInstaller) jsou odděleny od runtime.

Cílová snímková frekvence 60 FPS. Pohyb musí zůstat konzistentní při běžných
výkyvech FPS. F11 přepíná okno / fullscreen. Ovládání je pouze klávesnicí,
včetně všech menu a překryvných obrazovek.

Distribuce: nepodepsané buildy pro Windows x64, macOS Apple Silicon a
macOS Intel; každý balíček obsahuje Python runtime, herní data, JSON prostředí,
assety, hudbu a zvuky.

## Development Workflow

1. Práce začíná načtením aktuálních Spec Kit artefaktů a projektových MD souborů
   (`AGENTS.md`, `CLAUDE.md`, `README.md`). Toto platí pro Claude i Codex.
2. Změna požadavku jde nejdřív do `spec.md`, pak do `plan.md`, pak do `tasks.md`,
   teprve poté do kódu. Kód nikdy nepředbíhá specifikaci.
3. `tasks.md` je jediný zdroj pravdy o stavu implementace. Stav úkolu se mění
   pouze podle skutečně dokončené a ověřené práce.
4. Před implementací musí projít kontrola konzistence mezi projektovými MD
   soubory, constitution, spec, plan, checklist a tasks (`analyze`).
5. Po dokončení implementace proběhne `converge`; nesmí zůstat nevyřešený
   rozdíl mezi specifikací a implementací.

Rozdělení rolí (oba agenti sdílejí Spec Kit artefakty jako předávací bod):
Claude vlastní specifikaci, architekturu, úplnost akceptačních kritérií a
konzistenci artefaktů. Codex vlastní implementaci schválených tasks,
placeholderové assety, testy, ruční ověření, buildy a aktualizaci stavu tasks.
Je-li dostupný jen jeden agent, provede obě role.

## Governance

Tato ústava má přednost před zvyklostmi a preferencemi. Změna vyžaduje zápis
do tohoto souboru, zvýšení verze a odůvodnění v `plan.md` (sekce Complexity
Tracking).

Verzování: MAJOR při odstranění nebo neslučitelné změně principu, MINOR při
přidání principu nebo podstatném rozšíření, PATCH při upřesnění formulace.

Každá dokončená fáze musí ověřit soulad s principy I–VII. Porušení principu
označeného NON-NEGOTIABLE je blokující vada, ne technický dluh.

**Version**: 1.0.0 | **Ratified**: 2026-09-03 | **Last Amended**: 2026-09-03
