# Alzák Platformer Tech Demo Constitution

Závazná pravidla projektu.

Vychází z projektového scope (sekce 1–20) dodaného zadavatelem a z projektových
řádů `AGENTS.md`, `CLAUDE.md` a `feedback_pipeline_standalone.md`.

## Instruction Precedence

Přebírá se model z `AGENTS.md` §1 beze změny. Pro tento projekt platí:

1. explicitní pokyn zadavatele pro aktuální úkol — **scope sekce 1–20** a pozdější
   pokyny v konverzaci;
2. omezení operačního systému, bezpečnosti, soukromí a platformy;
3. `feedback_pipeline_standalone.md` a **tato constitution**;
4. `AGENTS.md` a `CLAUDE.md`;
5. `specs/001-alzak-platformer-demo/spec.md` a schválená rozhodnutí
   v `specs/001-alzak-platformer-demo/open-decisions.md`;
6. `plan.md`, `research.md`, `data-model.md`, `contracts/`, `tasks.md`;
7. obecné konvence Spec Kitu a nástrojů.

Při skutečném konfliktu dvou pravidel se pravidlo nevybírá podle pohodlnosti.
Konflikt se pojmenuje, ověří se, zda jej neřeší precedence, a zastaví se **pouze
dotčená cesta**, pokud zbývá nerozhodnutá materiální otázka produktu, architektury,
bezpečnosti, dat nebo kompatibility. Otevřené otázky se evidují v `open-decisions.md`,
nikdy pouze v konverzaci.

Žádné pravidlo nižší autority nesmí tiše oslabit požadavky na bezpečnost, integritu,
soukromí ani na důkazy o provedené validaci.

## Core Principles

### I. Scope-First, Demo-Scale (NON-NEGOTIABLE)

Projekt je **technologické demo**, ne produkční hra. Implementuje se přesně to,
co je ve scope a ve schválených rozhodnutích — nic víc. Každá funkce mimo tento
rámec musí být schválena zadavatelem a zapsána do `spec.md`, jinak se neimplementuje.

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

**Vědomá odchylka od `AGENTS.md` §13.** `AGENTS.md` §13 předepisuje nejužší
testovací rozsah, který změnu prokáže. Scope §16 (autorita 1) vyžaduje po každé
funkci **celou** dosavadní sadu. Rozpor řeší precedence ve prospěch scope. Odchylka
je navíc prakticky bezvýznamná: sada dema běží jednotky sekund, takže „nejužší
smysluplný důkaz" a „celá sada" splývají. `AGENTS.md` §13 uvádí plnou sadu jako
legitimní úroveň 5 svého vlastního pořadí. Tato odchylka je tímto zdokumentována,
aby ji budoucí agent nepovažoval za porušení.

Pro **feedback vrstvu** (viz níže) platí výslovná výjimka: testuje se pouze
minimum vyžadované `feedback_pipeline_standalone.md` §21.30, ne plná sada.

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

**Runtime závislosti mimo `pygame-ce` se nepřidávají.** Standardní knihovna má
přednost. Vývojové závislosti (pytest, PyInstaller a případné závislosti feedback
vrstvy) jsou od runtime odděleny a nesmí se dostat do produkčního buildu.

Cílová snímková frekvence 60 FPS. Pohyb musí zůstat konzistentní při běžných
výkyvech FPS. F11 přepíná okno / fullscreen. Ovládání je pouze klávesnicí,
včetně všech menu a překryvných obrazovek.

Distribuce: nepodepsané buildy pro Windows x64, macOS Apple Silicon a
macOS Intel; každý balíček obsahuje Python runtime, herní data, JSON prostředí,
assety, hudbu a zvuky.

Neexistuje strojově specifická politika úložiště (ověřeno 2026-09-03). Platí proto
generické chování `AGENTS.md` §17: build artefakty jdou do repo-local `build/` a
`dist/`, obojí ignorováno Gitem. Do sdíleného zdrojového kódu ani konfigurace se
**nesmí** zapsat cesta specifická pro stroj jednoho uživatele.

## Vývojářský feedback pipeline

`feedback_pipeline_standalone.md` je kanonická politika a **nesmí být duplikována**
do této ústavy ani do `AGENTS.md` (její §21 preambule a §21.28). Zde jsou pouze
rozhodnutí specifická pro tento projekt.

**Rozhodnutí OD-001 (2026-09-03, zadavatel): pipeline se přijímá — varianta V2,
v nezbytném minimu a s minimem testů.**

Závazný rozsah pro tento projekt:

1. Implementuje se **všech 9 položek** bootstrap minima dle §21.30, každá
   v nejmenším rozsahu, který politice vyhoví.
2. Testuje se **pouze** minimum, které §21.30 sama vyžaduje: test produkčního
   vyloučení (§21.2) a jeden end-to-end test pipeline (§21.27), plus minimální
   jednotkové testy stabilního ID, checksumů a deduplikace (§21.8, §21.11).
3. Priorita **P6** — implementuje se až po dokončení herního dema (US1–US5).
   Herní MVP dle scope §18 se tím neodkládá.
4. Kanonické prvky se **nepředefinovávají** (§21.28): stavy `open` / `in_progress` /
   `done`, formát stabilního ID `FB-<UTC_DATE>-<RANDOM_OR_UUID>`, immutable evidence
   a startovní workflow zůstávají přesně dle politiky.
5. **Omezení platformy se dokumentují, nezastírají.** pygame nemá nativní overlay,
   accessibility strom ani OS transkripci. Kde adaptér schopnost nemá, degraduje
   **explicitně** dle §21.4 a §21.6 (`audio unavailable`, `transcription unavailable`),
   nikdy tiše a nikdy síťovým fallbackem. Dle §21.29 se pipeline **nesmí** označit
   za funkční v části, pro kterou neexistuje end-to-end důkaz.
6. Pipeline je vývojářský nástroj. Produkční vyloučení musí být **strukturální,
   testovatelné a zdokumentované** (§21.2); samotný runtime příznak nestačí.

Dokud pipeline neexistuje, start-of-session protokol (`CLAUDE.md` §2 bod 7,
`AGENTS.md` §3.1 bod 11) nelze spustit. Agent to **hlásí jako nedostupné** a
netvrdí, že přezkum feedbacku proběhl (§21.16).

## Git policy

Přebírá se `AGENTS.md` §5 a §14. Doplněk specifický pro tento projekt:

**Rozhodnutí OD-003 (2026-09-03, zadavatel):** ve smyslu `AGENTS.md` §5.3
(„repository-specific instructions explicitly require it") je tímto udělena
**stálá autorizace commitovat na checkpointech** definovaných níže, na branchi
`001-alzak-platformer-demo`, **bez pushe**.

- Push na remote vyžaduje vždy samostatné svolení.
- Commit obsahuje jen soudržnou práci k danému checkpointu; žádná tajemství,
  dočasné logy, IDE stav ani strojově specifickou konfiguraci.
- Před commitem: `git status --short`, `git diff --check`, `git diff --stat`
  a prohlédnutí skutečného diffu.
- Zakázáno bez výslovného svolení: `git reset --hard`, `git clean -fd(x)`,
  `git checkout -- .`, `git restore .`, `git push --force*`, `git rebase --onto`,
  `git filter-branch`, `git filter-repo`, amend cizího commitu, přepis publikované
  historie, mazání branchí, změna remotes, změna globální Git konfigurace.
- Hygiena kontextu **nikdy** nezakládá právo commitovat ani pushovat.

Poznámka k historii: commit `4040592` (bootstrap Spec Kitu a constitution v1.0.0)
vznikl dříve, než byly projektové MD soubory v repozitáři. Není vracen —
`AGENTS.md` §5.2 a `CLAUDE.md` §13 zakazují reset nebo amend bez autorizace.

## Spec Kit fáze a checkpointy

Úplný řetězec pro tento projekt má **devět** fází (scope §2):

```text
constitution → specify → clarify → plan → checklist → tasks → analyze → implement → converge
```

`AGENTS.md` §15.3 ani `CLAUDE.md` §3 fáze `checklist` a `converge` neuvádějí. Scope
je jako pokyn autority 1 **přidává**; nejde o rozpor. Nainstalované skilly nesou
prefix `speckit-` (`CLAUDE.md` §3), což je závazné názvosloví.

Všech devět fází jsou **major fáze**. Po každé z nich se dle `CLAUDE.md` §3:

1. validuje výstup;
2. perzistuje trvalý stav;
3. vydá checkpoint report;
4. **ZASTAVÍ** před další fází, není-li průběžný běh výslovně autorizován.

Dokončení `plan` neautorizuje `tasks`. Dokončení `tasks` neautorizuje `implement`.

Výchozí stop-pointy uvnitř `implement` (`CLAUDE.md` §4, `AGENTS.md` §15.4):
Setup · Foundational · každá user story (US1…US6) · před zásadním refaktorem ·
před ověřením release. Dvacetikrokové pořadí ze scope §19 se na tyto stop-pointy
mapuje a je s nimi plně slučitelné.

Pro `analyze`, bezpečnostní přezkum a závěrečný audit implementace se dle
`CLAUDE.md` §11 upřednostňuje čerstvý kontext, je-li to prakticky možné.

## Reporting a handoff

Závěrečný report každého vývojového úkolu má **povinnou strukturu** dle
`AGENTS.md` §19: Result · Files changed · Validation · Resources · Risks ·
Feedback pipeline · Session handoff.

Na každém checkpointu se vydá **handoff blok** dle `CLAUDE.md` §9 a `AGENTS.md`
§15.9 a **právě jeden** kontextový marker dle `CLAUDE.md` §8 a `AGENTS.md` §15.6:

```text
CONTEXT: SAFE TO CLEAR | COMPACT RECOMMENDED | KEEP CURRENT SESSION
```

`SAFE TO CLEAR` je faktické tvrzení a smí zaznít až po splnění celé pre-clear
brány (`AGENTS.md` §15.5, `CLAUDE.md` §5).

Handoff **doplňuje** repozitář, nenahrazuje jej. Nesmí obsahovat jediný požadavek,
který neexistuje nikde jinde (`AGENTS.md` §15.9).

Úspěch se nikdy netvrdí bez důkazu. Neproběhlá nebo nedostupná validace se hlásí
výslovně, včetně důvodu a postupu, jak ji doplnit (`AGENTS.md` §7).

## Governance

Tato ústava má přednost před zvyklostmi a preferencemi v mezích výše uvedené
precedence. Změna vyžaduje zápis do tohoto souboru, zvýšení verze a odůvodnění
v `plan.md` (sekce Complexity Tracking) nebo v `open-decisions.md`.

Verzování: MAJOR při odstranění nebo neslučitelné změně principu, MINOR při
přidání principu nebo podstatném rozšíření, PATCH při upřesnění formulace.

Každá dokončená fáze musí ověřit soulad s principy I–VII. Porušení principu
označeného NON-NEGOTIABLE je blokující vada, ne technický dluh.

Rozdělení rolí (Spec Kit artefakty jsou společný předávací bod obou agentů):
Claude vlastní specifikaci, architekturu, úplnost akceptačních kritérií a
konzistenci artefaktů. Codex vlastní implementaci schválených tasks,
placeholderové assety, testy, ruční ověření, buildy a aktualizaci stavu tasks.
Je-li dostupný jen jeden agent, provede obě role. Oba začínají načtením
`AGENTS.md`, `CLAUDE.md`, této ústavy a aktivních artefaktů feature — nikdy
z paměti staré konverzace (`AGENTS.md` §15.8).

**Version**: 1.1.0 | **Ratified**: 2026-09-03 | **Last Amended**: 2026-09-03

### Historie změn

- **1.1.0** (2026-09-03) — doplněna sekce Instruction Precedence (nález B1),
  Git policy včetně OD-003 (B2), Reporting a handoff (B3, B4), Spec Kit fáze
  a checkpointy (B6, D4), Vývojářský feedback pipeline dle OD-001; k Principu VI
  doplněna zdokumentovaná odchylka od `AGENTS.md` §13 (B5); do Technology
  Constraints doplněn stav strojové politiky úložiště (D3). Podklad:
  `specs/001-alzak-platformer-demo/analysis-report.md`.
- **1.0.0** (2026-09-03) — první verze, sepsána před doplněním projektových MD
  souborů; obsahovala principy I–VII, Technology Constraints a Development Workflow.
