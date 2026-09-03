# Feature Specification: Alzák — technologické demo 2D plošinovky

**Feature Branch**: `001-alzak-platformer-demo`

**Created**: 2026-09-03

**Status**: Ready for Planning

**Revize**: 2026-09-03 — sesouhlaseno s projektovými řády doplněnými zadavatelem; podklad `analysis-report.md`, rozhodnutí `open-decisions.md`. 2026-09-03 — fáze `clarify`: pět upřesnění zaznamenaných v sekci Clarifications. 2026-09-03 — vstup do fáze `plan`: tři uzavřená rozhodnutí zadavatele ke geometrii laseru (OD-006), zapsaná jako FR-085…FR-087 a SC-021. 2026-09-03 — zadavatel výslovně vyřadil vývojářskou feedback pipeline z rozsahu (OD-007); US6, FR-066…FR-080, FR-088 a SC-014…SC-016/SC-022 jsou neaktivní historické identifikátory. 2026-09-03 — výtvarná a herní revize OD-008 doplňuje FR-089…FR-093 a SC-023…SC-025.

**Input**: Projektový scope zadavatele, sekce 1–20 (pokyn autority 1 dle `AGENTS.md` §1), doplněný projektovými řády `AGENTS.md` a `CLAUDE.md`. Vzájemná precedence je definována v `.specify/memory/constitution.md`, sekce Instruction Precedence. Rozhodnutí OD-007 výslovně vylučuje feedback pipeline z této feature.

## Přehled

Samostatně předveditelné technologické demo 2D plošinové hry s firemním maskotem
Alzákem. Hráč projde třemi pevnými prostředími (obchodní pobočka → logistický
sklad → kancelář). V každém porazí jednoho hlídkujícího protivníka souvislým
laserem s přehříváním a vstoupí do aktivovaného východu. Demo předvádí kvalitu
pohybu, souboj, prezentaci a kompletní distribuční řetězec pro Windows a macOS.

## Clarifications

### Session 2026-09-03

- Q: Mají se programově generované placeholderové assety verzovat v repozitáři, nebo se mají generovat při buildu či za běhu? (A-005, FR-049, FR-050) → A: Verzovat v repozitáři a **zároveň** ponechat deterministický generátor. Stejný vstup generátoru musí vytvořit shodné placeholdery. Hra při běžném spuštění používá již vygenerované soubory; generování za běhu aplikace není součástí běžného herního toku.
- Q: Co má udělat položka „Ukončit hru" na obrazovce pauzy a na obrazovce neúspěchu — ukončit aplikaci, nebo se vrátit na úvodní obrazovku? (FR-051, FR-053, FR-054) → A: Vrátit na úvodní obrazovku. Aplikaci ukončí pouze „Ukončit" na úvodní a na závěrečné obrazovce.
- Q: Jak se hráči zobrazí chyba načtení poškozeného JSON prostředí v zabaleném buildu, který nemá konzoli? (FR-046, FR-047) → A: Vlastní chybovou obrazovkou uvnitř aplikace (soubor + pole + důvod), současně zápisem na standardní chybový výstup a ukončením s nenulovým návratovým kódem.
- Q: Kumuluje se poškození protivníka i přes přerušení střelby, nebo se mu životy mezi dávkami obnovují? (FR-039, SC-004) → A: Kumuluje se trvale a protivník životy neregeneruje. Plné životy vrací výhradně restart prostředí (R / „Opakovat prostředí") nebo nový vstup do prostředí.
- Q: Jak se má hra chovat na displeji větším než 1920 × 1080 a na displeji s jiným poměrem stran než 16:9? (FR-001, FR-002) → A: Proporcionálně škálovat oběma směry na maximální plochu při zachovaném poměru 16:9, zbytek vyplnit černým letterboxem nebo pillarboxem.

### Session 2026-09-03 — vstup do fáze `plan`

Rozhodnutí uzavřel zadavatel přímo, bez dotazu. Evidováno jako OD-006.

- Q: Kde přesně laser vzniká a jak široký je jeho kolizní paprsek? (FR-027, FR-028, FR-034) → A: Laser začíná v **konfigurovatelném výstupním bodu (muzzle)** definovaném jako offset vůči pozici Alzáka a jeho směru pohledu, vede **vodorovně** k první pevné překážce nebo k protivníkovi a jeho výchozí **kolizní tloušťka je 16 px** v logickém prostoru 1920 × 1080. Viz FR-085, FR-086.
- Q: Kam patří geometrie a vzhled laseru? (Princip II) → A: Do **centrální konfigurace** `src/alzak/config.py` — offset muzzle, kolizní tloušťka, tloušťka a barvy vykreslení. V logice ani ve vykreslování laseru nesmí zůstat magic numbers. Viz FR-087, SC-021.

### Session 2026-09-03 — změna rozsahu

- Q: Má být součástí feature vývojářská feedback pipeline? → A: **Ne. Zadavatel ji výslovně vyřadil úplně.** OD-007 nahrazuje dřívější OD-001 a příslušnou část OD-006; US6 ani její kód, data, klávesa a testy se neimplementují.

### Session 2026-09-03 — výtvarná a herní revize

- Q: Jaký má být finální vizuální směr a chování Alzáka? → A: Realitou inspirovaný, ale **stylizovaný high-poly 3D vzhled, nikoli fotorealismus**. Alzák je z profilu, používá vícestavovou animaci, viditelně drží laserovou pistoli a laser má konečný dosah. Pozadí pobočky, skladu a kanceláře jsou odlišná autorská high-poly prostředí; herní plošiny jsou tenké konstrukční lávky, nikoli vyplněné obdélníkové bloky. Všechny zvýšené plošiny musí zůstat dosažitelné běžným skokem. Viz OD-008, FR-089…FR-093.

**Poznámka k číslování**: požadavky přidané v této fázi dostávají další volné ID
(FR-081 a výše) a jsou umístěny do věcně příslušné sekce. Stávající FR se
**nepřečíslovávají**, aby zůstaly platné odkazy v `analysis-report.md`,
`open-decisions.md` a `.specify/memory/constitution.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 – Průchod jedním prostředím (Priority: P1) 🎯 MVP

Hráč se objeví na startovní pozici prostředí. Vidí plošiny, propast, hlídkujícího
protivníka a **neaktivní** východ. Rozeběhne se, přeskočí propast, drží X a
souvislým laserem zlikviduje protivníka. Východ se rozsvítí jako aktivní. Hráč do
něj vstoupí a prostředí je dokončeno.

**Why this priority**: Toto je celá jádrová smyčka dema. Bez ní neexistuje nic
předveditelného. Když je hotová jen tato story, demo už má hodnotu — jedno
hratelné prostředí, které ukazuje pohyb, souboj i cíl.

**Independent Test**: Spustit hru přímo v prvním prostředí, projít cyklus
pohyb → skok → laser → poražení → východ. Nevyžaduje menu, další prostředí ani
systém energie.

**Acceptance Scenarios**:

1. **Given** načtené prostředí, **When** hra začne, **Then** je Alzák na startovní pozici definované v JSON, stojí na pevné ploše a nepropadá.
2. **Given** Alzák stojí na plošině, **When** hráč drží šipku vpravo, **Then** Alzák plynule zrychluje doprava až na maximální rychlost a po uvolnění klávesy přirozeně zastaví.
3. **Given** Alzák stojí na plošině, **When** hráč krátce klepne na mezerník, **Then** Alzák vyskočí nízko; **When** hráč mezerník podrží, **Then** Alzák vyskočí výrazně výš.
4. **Given** Alzák se pohybuje směrem k plošině, **When** dojde ke kolizi, **Then** je zastaven na její hraně a nikdy neprojde skrz ani se do ní nezasekne.
5. **Given** protivník hlídkuje na své plošině, **When** dorazí ke krajnímu bodu trasy, **Then** se otočí a pokračuje opačným směrem.
6. **Given** hráč se dívá doprava a protivník je vpravo v přímé linii, **When** hráč drží X, **Then** se vykreslí souvislý vodorovný laser od výstupního bodu (muzzle) Alzáka po protivníka, ne dál, a protivník průběžně ztrácí životy s viditelnou odezvou zásahu.
7. **Given** mezi Alzákem a protivníkem je plošina, **When** hráč drží X, **Then** laser končí na plošině a protivník nedostává poškození.
8. **Given** laser působí na protivníka, **When** celková doba působení dosáhne přibližně 1 sekundy, **Then** je protivník poražen a zmizí.
9. **Given** protivník je poražen, **When** se stav prostředí vyhodnotí, **Then** se východ přepne z neaktivního na aktivní s jasně odlišnou vizuální podobou.
10. **Given** východ je aktivní, **When** se s ním Alzák překryje, **Then** je prostředí dokončeno.
11. **Given** východ je **ne**aktivní, **When** se s ním Alzák překryje, **Then** se nic nestane a hra pokračuje.

---

### User Story 2 – Přežití, zranění a neúspěch (Priority: P2)

Alzák má tři body energie. Dotyk protivníka ho zraní a odhodí, načež je krátce
nezranitelný. Pád do propasti ho stojí energii a vrací na start. Po vyčerpání
energie se objeví obrazovka neúspěchu, ze které lze prostředí zopakovat.

**Why this priority**: Dodává riziko a smysl vyhýbání se protivníkovi. Bez ní je
US1 bez napětí, ale stále hratelná — proto P2.

**Independent Test**: V jednom prostředí opakovaně narazit do protivníka a spadnout
do propasti; ověřit odpočet energie, odhození, nezranitelnost, respawn, obrazovku
neúspěchu a restart.

**Acceptance Scenarios**:

1. **Given** hráč vstoupí do prostředí, **When** se prostředí načte, **Then** má Alzák přesně 3 body energie zobrazené v HUD.
2. **Given** Alzák je zranitelný, **When** se dotkne protivníka, **Then** ztratí právě 1 bod energie, je krátce odhozen směrem od protivníka a získá přibližně 1 sekundu nezranitelnosti s jasnou vizuální odezvou.
3. **Given** Alzák je v nezranitelnosti, **When** se protivníka dotkne znovu, **Then** neztratí žádnou energii.
4. **Given** nezranitelnost vypršela, **When** se Alzák dotkne protivníka, **Then** ztratí další bod energie.
5. **Given** Alzák spadne pod hranici propasti, **When** se pád vyhodnotí, **Then** ztratí 1 bod energie a objeví se na startovní pozici **téhož** prostředí; protivník si zachová svůj stav (pozici i poškození).
6. **Given** Alzákovi zbývá 1 bod energie, **When** utrpí další zásah nebo spadne do propasti, **Then** energie klesne na 0 a zobrazí se obrazovka neúspěchu.
7. **Given** obrazovka neúspěchu, **When** hráč zvolí „Opakovat prostředí", **Then** se prostředí obnoví do plně počátečního stavu — pozice Alzáka, 3 body energie, vychladlý laser, plně obnovený a neporažený protivník na výchozí pozici, neaktivní východ.
8. **Given** hráč hraje libovolné prostředí, **When** stiskne R, **Then** proběhne stejné úplné obnovení počátečního stavu prostředí.

---

### User Story 3 – Kompletní průchod třemi prostředími (Priority: P3)

Hráč postupně dokončí pobočku, sklad a kancelář v pevném pořadí, mezi nimi vidí
krátký přechod, a po třetím prostředí se dostane na závěrečnou obrazovku.

**Why this priority**: Mění jedno prostředí v ucelené demo s obloukem. Vyžaduje
hotovou US1.

**Independent Test**: Odehrát celý průchod od prvního prostředí po závěrečnou
obrazovku a ověřit pořadí, přechody a obnovení energie.

**Acceptance Scenarios**:

1. **Given** hráč spustí demo, **When** začne hrát, **Then** je prvním prostředím obchodní pobočka, druhým logistický sklad a třetím kancelář, vždy v tomto pevném pořadí.
2. **Given** hráč dokončí prostředí, **When** se spustí přechod, **Then** obraz krátce ztmavne a znovu se rozsvítí v následujícím prostředí.
3. **Given** hráč vstoupí do nového prostředí, **When** se prostředí načte, **Then** je energie doplněna na 3 body bez ohledu na její předchozí stav.
4. **Given** hráč dokončí třetí prostředí, **When** přechod skončí, **Then** se zobrazí závěrečná obrazovka s informací o dokončení dema.
5. **Given** závěrečná obrazovka, **When** hráč zvolí „Spustit znovu", **Then** demo začíná znovu od prvního prostředí s plnou energií a čistým stavem.
6. **Given** kterékoli ze tří prostředí, **When** se načte, **Then** zabírá jednu pevnou obrazovku 1920×1080 se statickou kamerou a obsahuje plošiny, propast, jednu instanci téhož typu protivníka, startovní pozici a východ.

---

### User Story 4 – Ovládání aplikace, HUD a zvuková odezva (Priority: P4)

Hráč ovládá celé demo klávesnicí: spustí ho z úvodní obrazovky, kdykoli
pozastaví, přepne fullscreen a průběžně vidí v HUD energii, teplotu laseru a
kde v demu je. Hudba hraje souvisle, zvuky reagují na jeho akce.

**Why this priority**: Rám kolem hry. Demo je bez něj hratelné, ale nepředvedené.

**Independent Test**: Projít všechny obrazovky pouze klávesnicí, ověřit každý
prvek HUD a každý zvukový efekt proti odpovídající akci.

**Acceptance Scenarios**:

1. **Given** spuštěná aplikace, **When** se objeví úvodní obrazovka, **Then** obsahuje název dema, položku „Spustit" a položku „Ukončit", ovladatelné pouze klávesnicí.
2. **Given** probíhající hra, **When** hráč stiskne Escape, **Then** se hra pozastaví (simulace se zastaví), zobrazí se pauza s „Pokračovat", „Restartovat prostředí", „Ukončit hru" a hudba se ztiší.
3. **Given** pauza, **When** hráč zvolí „Pokračovat", **Then** hra pokračuje z místa zastavení a hlasitost hudby se vrátí na běžnou úroveň.
4. **Given** libovolný stav hry, **When** hráč stiskne F11, **Then** se přepne mezi okenním a fullscreen režimem a herní rozmístění zůstane nezměněné.
5. **Given** hra běží na displeji menším než 1920×1080, **When** se vykresluje, **Then** se celý obraz proporcionálně zmenší se zachováním poměru 16:9 a herní souřadnice zůstanou v prostoru 1920×1080.
6. **Given** probíhající hra, **When** hráč sleduje HUD, **Then** vidí tři body energie, ukazatel teploty laseru, název prostředí a jeho pořadí ve tvaru „2/3".
7. **Given** spuštěná hra, **When** hudba dohraje, **Then** plynule pokračuje ve smyčce a nepřerušuje se při přechodu mezi prostředími.
8. **Given** Alzák se pohybuje po pevné ploše, **When** se pohybuje, **Then** zní zvuk pohybu; **When** stojí nebo je ve vzduchu, **Then** zvuk pohybu nezní.
9. **Given** hráč spustí laser, **When** stiskne X, **Then** zazní zvuk spuštění a naváže na něj zvuk trvání laseru; **When** X uvolní, laser se přehřeje, hra se pozastaví nebo se změní herní stav, **Then** zvuk trvání okamžitě skončí a zazní zvuk ukončení.
10. **Given** obrazovka pauzy nebo obrazovka neúspěchu, **When** hráč zvolí „Ukončit hru", **Then** se rozehraná hra zahodí a zobrazí se úvodní obrazovka, přičemž aplikace zůstane spuštěná.
11. **Given** displej s rozlišením vyšším než 1920 × 1080 nebo s jiným poměrem stran než 16:9, **When** se vykresluje, **Then** herní obraz zabírá největší možnou plochu při zachovaném poměru 16:9 a zbývající okraje jsou černé.

---

### User Story 5 – Spuštění a distribuce (Priority: P5)

Vývojář spustí demo ze zdrojového kódu, lokálně vyrobí aplikaci pro Windows i
macOS a nechá GitHub Actions automaticky sestavit artefakty pro všechny tři cíle.

**Why this priority**: Nutná podmínka „samostatně předveditelného" dema, ale až po
tom, co je co předvádět.

**Independent Test**: Čistý klon → instalace závislostí → spuštění → build →
stažený artefakt spustit a dohrát demo.

**Acceptance Scenarios**:

1. **Given** čistý klon repozitáře, **When** vývojář provede zdokumentované kroky, **Then** se hra spustí ze zdrojového kódu na Windows i macOS.
2. **Given** vývojář na Windows, **When** spustí lokální build skript, **Then** vznikne spustitelná 64bitová Windows aplikace obsahující Python runtime, herní data, JSON prostředí, assety, hudbu a zvuky.
3. **Given** vývojář na macOS, **When** spustí lokální build skript, **Then** vznikne spustitelná macOS aplikace se stejným obsahem.
4. **Given** push do repozitáře, **When** proběhne GitHub Actions, **Then** se spustí celá testovací sada headless a vzniknou artefakty: Windows x64, macOS Apple Silicon a macOS Intel.
5. **Given** stažený artefakt na cílovém systému, **When** ho uživatel spustí, **Then** lze dokončit celé demo od úvodní po závěrečnou obrazovku bez instalace Pythonu.

---

### Edge Cases

- Hráč drží X déle než dovolí přehřívání → laser se zablokuje, je to viditelné v HUD a zvuk trvání skončí; po ochlazení pod práh opětovné aktivace laser znovu funguje i při stále drženém X.
- Hráč pustí X těsně před přehřátím → laser se začne ochlazovat, nikdy se nezablokuje.
- Hráč přeruší střelbu a po chvíli ji obnoví → protivník si zachová dosud utržené poškození a žádné životy neregeneruje; rozhoduje součet doby působení, ne délka jedné dávky.
- Hráč porazí protivníka a vzápětí spadne do propasti → východ zůstává aktivní, protivník zůstává poražený, hráč ztrácí energii a vrací se na start.
- Hráč vyčerpá poslední energii v témže okamžiku, kdy porazí protivníka → přednost má obrazovka neúspěchu; prostředí se nepočítá jako dokončené.
- Hráč stiskne Escape během přechodu mezi prostředími → přechod doběhne konzistentně, pauza nesmí zanechat hru v rozbitém stavu.
- Hráč drží X při vstupu do východu nebo při pauze → laser okamžitě končí včetně zvuku.
- Hráč sjede z hrany plošiny bez skoku → po dobu coyote time smí ještě skočit.
- Hráč stiskne mezerník těsně před dopadem → jump buffer skok provede v okamžiku dopadu.
- Hráč drží obě šipky současně → Alzák nezrychluje ani na jednu stranu.
- Alzák je odhozen zásahem přímo nad propast → pád do propasti se vyhodnotí normálně a odečte další bod energie.
- JSON prostředí je poškozený nebo nemá povinné pole → aplikace zobrazí chybovou obrazovku uvnitř aplikace s názvem souboru, chybným polem a důvodem, tutéž zprávu zapíše na standardní chybový výstup a skončí nenulovým návratovým kódem; prostředí nikdy nespustí v nedefinovaném stavu (FR-084).
- Zvukové zařízení není k dispozici (CI, headless) → hra běží dál bez zvuku a nespadne.
- Snímková frekvence krátkodobě klesne → herní pohyb a časovače (coyote, buffer, nezranitelnost, přehřívání) zůstanou konzistentní v reálném čase.

## Requirements *(mandatory)*

### Funkční požadavky — aplikace a prezentace

- **FR-001**: Hra MUSÍ používat logické rozlišení 1920 × 1080 s poměrem stran 16:9 jako jediný souřadnicový systém pro veškerou herní logiku.
- **FR-002**: Prezentační vrstva MUSÍ celý obraz proporcionálně škálovat na skutečné rozlišení okna nebo obrazovky — **zmenšovat i zvětšovat** — vždy se zachováním poměru stran 16:9. Nevyužitý prostor MUSÍ být vyplněn černým letterboxem (vodorovné pruhy) nebo pillarboxem (svislé pruhy). Rozmístění objektů i veškerá herní logika zůstávají v prostoru 1920 × 1080 a herní kód skutečné rozlišení okna nečte.
- **FR-003**: Klávesa F11 MUSÍ přepínat mezi okenním a fullscreen režimem v kterémkoli stavu hry.
- **FR-004**: Cílová obnovovací frekvence MUSÍ být 60 FPS a herní pohyb i všechny časovače MUSÍ zůstat konzistentní při běžných výkyvech FPS.
- **FR-005**: Aplikace MUSÍ být ovladatelná výhradně klávesnicí, včetně menu a všech překryvných obrazovek.

### Funkční požadavky — ovládání

- **FR-006**: Šipka vlevo MUSÍ pohybovat Alzákem doleva, šipka vpravo doprava.
- **FR-007**: Mezerník MUSÍ vyvolat skok.
- **FR-008**: Klávesa X MUSÍ po dobu držení vysílat souvislý laser.
- **FR-009**: Escape MUSÍ pozastavit hru.
- **FR-010**: Klávesa R MUSÍ restartovat aktuální prostředí.

### Funkční požadavky — pohyb Alzáka

- **FR-011**: Pohyb po zemi MUSÍ mít plynulé zrychlení, přirozené zastavení a maximální rychlost.
- **FR-012**: Ve vzduchu MUSÍ mít hráč menší, ale stále použitelnou kontrolu nad vodorovným pohybem.
- **FR-013**: Na Alzáka MUSÍ působit gravitace s omezenou maximální rychlostí pádu.
- **FR-014**: Výška skoku MUSÍ být proměnlivá podle délky držení mezerníku.
- **FR-015**: Hra MUSÍ poskytovat přibližně 100 ms coyote time po opuštění pevné plochy.
- **FR-016**: Hra MUSÍ poskytovat přibližně 120 ms jump buffer pro skok stisknutý před dopadem.
- **FR-017**: Kolize s plošinami MUSÍ být stabilní — bez propadání, zasekávání a chvění.
- **FR-018**: Hra MUSÍ jednoznačně rozlišovat stav na zemi a ve vzduchu a tento stav MUSÍ řídit skok, coyote time i zvuk pohybu.
- **FR-019**: Všechny hodnoty pohybu MUSÍ být uloženy v centrální konfiguraci.

### Funkční požadavky — energie, zásah a pád

- **FR-020**: Alzák MUSÍ začínat každé prostředí se třemi body energie.
- **FR-021**: Kontakt s protivníkem MUSÍ odebrat právě jeden bod energie, krátce Alzáka odhodit, aktivovat přibližně jednu sekundu nezranitelnosti a poskytnout jasnou vizuální odezvu.
- **FR-022**: Během nezranitelnosti MUSÍ být další kontakt s protivníkem bez účinku na energii.
- **FR-023**: Pád do propasti MUSÍ odebrat jeden bod energie a vrátit Alzáka na startovní pozici aktuálního prostředí, aniž by měnil stav protivníka nebo východu.
- **FR-024**: Po vyčerpání energie MUSÍ hra zobrazit obrazovku neúspěchu s volbami zopakovat aktuální prostředí nebo ukončit hru.
- **FR-025**: Vstup do nového prostředí MUSÍ doplnit energii na tři body.
- **FR-026**: Restart prostředí MUSÍ obnovit jeho úplný počáteční stav včetně protivníka, energie, laseru a neaktivního východu.

### Funkční požadavky — laser

- **FR-027**: Při držení klávesy X MUSÍ Alzák vysílat souvislý vodorovný laser ve směru, kterým se dívá.
- **FR-028**: Laser MUSÍ začínat u Alzáka a končit na první pevné překážce nebo protivníkovi v jeho dráze.
- **FR-029**: Laser MUSÍ po dobu kontaktu poškozovat protivníka a poskytovat viditelnou odezvu zásahu.
- **FR-030**: Laser MUSÍ používat systém přehřívání: přibližně 1,5 sekundy nepřerušené střelby vede k úplnému přehřátí.
- **FR-031**: Po uvolnění klávesy X se laser MUSÍ začít ochlazovat.
- **FR-032**: Úplné přehřátí MUSÍ laser dočasně zablokovat; po ochlazení pod definovaný práh se MUSÍ znovu aktivovat.
- **FR-033**: Teplota laseru MUSÍ být viditelná v HUD.
- **FR-034**: Rychlost zahřívání, rychlost ochlazování a práh opětovné aktivace MUSÍ být v centrální konfiguraci.
- **FR-085**: Laser MUSÍ vycházet z **konfigurovatelného výstupního bodu (muzzle)** určeného offsetem vůči pozici Alzáka a zrcadleného podle jeho směru pohledu. Offset je součástí centrální konfigurace; v kódu laseru ani hráče nesmí být zapsán číselně.
- **FR-086**: Kolizní paprsek laseru MUSÍ mít definovanou tloušťku s **výchozí hodnotou 16 px** v logickém prostoru 1920 × 1080. Tloušťka určuje, co paprsek zasáhne, a je součástí centrální konfigurace.
- **FR-087**: Veškerá **geometrie a vzhled laseru** — offset muzzle, kolizní tloušťka, tloušťka a barvy vykreslení a případné další vizuální parametry — MUSÍ být definovány v centrální konfiguraci. V logice laseru ani ve vykreslovací vrstvě NESMÍ zůstat žádná číselná konstanta popisující laser.
- **FR-090**: Laser MUSÍ mít konečný, centrálně konfigurovatelný maximální dosah; výchozí dosah je **900 px** v logickém prostoru a paprsek stále končí dříve na první pevné překážce nebo protivníkovi.

### Funkční požadavky — protivník

- **FR-035**: Ve všech třech prostředích MUSÍ být použit stejný typ protivníka, jedna instance na prostředí.
- **FR-036**: Protivník MUSÍ hlídkovat po určené plošině mezi dvěma datově definovanými body a na konci trasy se otočit.
- **FR-037**: Kontakt s protivníkem MUSÍ zranit Alzáka podle FR-021.
- **FR-038**: Protivník MUSÍ reagovat na zásah laserem viditelnou odezvou.
- **FR-039**: Protivník MUSÍ být poražen přibližně po jedné sekundě **celkového** působení laseru. Poškození se kumuluje průběžně napříč přerušeními střelby i napříč pádem Alzáka do propasti a protivník je NESMÍ regenerovat. Plné životy se obnoví výhradně restartem prostředí (klávesa R nebo „Opakovat prostředí") anebo novým vstupem do prostředí.
- **FR-040**: Poražení protivníka MUSÍ aktivovat východ.

### Funkční požadavky — prostředí a data

- **FR-041**: Hra MUSÍ obsahovat tři prostředí: obchodní pobočka, logistický sklad, kancelářské prostředí, hraná v pevném lineárním pořadí.
- **FR-042**: Každé prostředí MUSÍ zabírat jednu pevnou obrazovku 1920 × 1080 se statickou kamerou.
- **FR-043**: Každé prostředí MUSÍ obsahovat plošiny, propast, jednu instanci protivníka, startovní pozici Alzáka a východ.
- **FR-044**: Východ MUSÍ být viditelný od začátku prostředí, aktivovat se až po poražení protivníka a vizuálně odlišit neaktivní a aktivní stav.
- **FR-045**: Prostředí je dokončeno tím, že hráč nejprve porazí protivníka a poté vstoupí do aktivního východu.
- **FR-046**: Každé prostředí MUSÍ být popsáno samostatným JSON souborem obsahujícím minimálně identifikátor, zobrazovaný název, startovní pozici Alzáka, pozice a rozměry plošin, prostor propasti, trasu protivníka, pozici východu a odkazy na assety.
- **FR-047**: Všechny tři JSON soubory MUSÍ používat společné schéma a být načítány společným načítacím systémem.
- **FR-048**: Mezi prostředími MUSÍ proběhnout krátký jednoduchý přechod (zatmavení a opětovné zobrazení).
- **FR-084**: Selže-li načtení nebo validace JSON prostředí, aplikace MUSÍ chybu zobrazit **uvnitř aplikace** na vlastní chybové obrazovce uvádějící název souboru, konkrétní pole a důvod, a současně tutéž zprávu zapsat na standardní chybový výstup. Chybová obrazovka MUSÍ fungovat i v zabaleném buildu bez konzole a MUSÍ být ukončitelná klávesnicí; aplikace poté skončí nenulovým návratovým kódem. Tiché ukončení ani neošetřená výjimka bez viditelné zprávy nejsou přípustné.
- **FR-092**: Každé ze tří prostředí MUSÍ mít odlišné autorské pozadí ve stylizovaném high-poly 3D směru inspirovaném reálnou pobočkou, skladem a kanceláří; prostředí NESMÍ být složeno pouze z jednobarevných geometrických bloků.
- **FR-093**: Viditelné plošiny MUSÍ být kresleny jako tenké konstrukční lávky s průhledným okolím, nikoli jako plná výplň celé kolizní výšky. Každá zvýšená plošina MUSÍ být dosažitelná standardním pohybem a skokem bez teleportace nebo diagnostického vstupu.

### Funkční požadavky — assety

- **FR-049**: Demo MUSÍ obsahovat placeholderové assety, které jednoznačně odliší Alzáka, protivníka, plošiny, propast, neaktivní východ, aktivní východ, pobočku, sklad, kancelář, energii a teplotu laseru.
- **FR-050**: Assety MUSÍ být zpřístupněny přes centrální registr se stabilními interními identifikátory tak, aby bylo možné nahradit placeholder finální grafikou bez změny herních pravidel.
- **FR-081**: Vygenerované placeholderové assety (obrázky, hudba, zvuky) MUSÍ být verzovány v repozitáři jako běžné soubory. Hra je při běžném spuštění — ze zdrojového kódu i z distribuovaného buildu — MUSÍ načítat z těchto uložených souborů. Generování assetů za běhu aplikace ani jako povinný krok buildu nebo CI je ZAKÁZÁNO.
- **FR-082**: Generátor placeholderů MUSÍ zůstat v repozitáři jako vývojářský nástroj a MUSÍ být deterministický: pro nezměněný vstup produkuje bajtově shodné výstupní soubory. Jeho spuštění je vědomý vývojářský krok mimo běžný herní tok.
- **FR-089**: Alzák MUSÍ být vykreslen z profilu jako transparentní stylizovaný high-poly sprite s viditelnou laserovou pistolí. Animace MUSÍ rozlišit nejméně idle, mrknutí, tři fáze běhu, skok, střelbu a zásah a MUSÍ se zrcadlit podle směru pohledu.
- **FR-091**: Autorské ImageGen bitmapy (atlas Alzáka a tři pozadí) MUSÍ být verzované, označené v manifestu `generated: false` a ověřené checksumem. Deterministický generátor je nesmí přepisovat; smí je pouze indexovat a kopírovat do ověřovacího výstupu.

### Funkční požadavky — menu a HUD

- **FR-051**: Úvodní obrazovka MUSÍ obsahovat název dema, položku „Spustit" a položku „Ukončit". Položka „Ukončit" ukončí aplikaci.
- **FR-052**: HUD MUSÍ zobrazovat tři body energie, ukazatel teploty laseru, název prostředí a pořadí prostředí ve tvaru „2/3".
- **FR-053**: Obrazovka pauzy MUSÍ obsahovat „Pokračovat", „Restartovat prostředí" a „Ukončit hru". Položka „Ukončit hru" MUSÍ zahodit rozehranou hru a vrátit hráče na úvodní obrazovku, NIKOLI ukončit aplikaci.
- **FR-054**: Obrazovka neúspěchu MUSÍ obsahovat „Opakovat prostředí" a „Ukončit hru". Položka „Ukončit hru" MUSÍ zahodit rozehranou hru a vrátit hráče na úvodní obrazovku, NIKOLI ukončit aplikaci.
- **FR-055**: Závěrečná obrazovka MUSÍ obsahovat informaci o dokončení dema, „Spustit znovu" a „Ukončit". Položka „Ukončit" ukončí aplikaci.
- **FR-083**: Aplikaci MUSÍ být možné ukončit z herního rozhraní výhradně položkou „Ukončit" na úvodní nebo na závěrečné obrazovce (vedle systémového zavření okna). Z obrazovky pauzy ani z obrazovky neúspěchu NESMÍ jít aplikaci ukončit přímo.

### Funkční požadavky — hudba a zvuky

- **FR-056**: Hra MUSÍ používat jednu jednoduchou hudební smyčku, která začne při spuštění hry a plynule pokračuje mezi třemi prostředími.
- **FR-057**: Při pauze se hudba MUSÍ ztišit a po pokračování vrátit na běžnou hlasitost.
- **FR-058**: Zvukové efekty MUSÍ pokrývat pohyb po zemi, skok, spuštění laseru, trvání laseru a ukončení laseru.
- **FR-059**: Zvuk pohybu MUSÍ být řízen skutečným pohybem Alzáka po pevné ploše.
- **FR-060**: Zvuk laseru MUSÍ správně reagovat na uvolnění klávesy, přehřátí, pauzu a změnu herního stavu.

### Funkční požadavky — testování a distribuce

- **FR-061**: Automatické testy MUSÍ pokrýt tři body energie, ztrátu energie, dočasnou nezranitelnost, přehřívání a ochlazování laseru, poškozování protivníka, poražení protivníka, aktivaci východu, načtení všech tří JSON prostředí a přechod mezi prostředími.
- **FR-062**: Relevantní testy MUSÍ být spustitelné headless pro CI.
- **FR-063**: Projekt MUSÍ podporovat spuštění ze zdrojového kódu, lokální build Windows aplikace, lokální build macOS aplikace a automatické sestavení přes GitHub Actions.
- **FR-064**: Automatické sestavení MUSÍ produkovat Windows 64bitový artefakt, macOS artefakt pro Apple Silicon a macOS artefakt pro Intel.
- **FR-065**: Buildy MUSÍ obsahovat Python runtime, herní data, JSON prostředí, assety, hudbu a zvuky. Výsledné balíčky jsou nepodepsané technologické buildy.

### Key Entities

- **Alzák (hráč)**: pozice, rozměry, rychlost, směr pohledu, stav na zemi/ve vzduchu, energie (0–3), stav nezranitelnosti, časovače coyote a jump bufferu.
- **Protivník**: pozice, rozměry, směr hlídkování, dva krajní body trasy, aktuální životy, stav poražen/živý, časovač vizuální odezvy zásahu.
- **Laser**: stav aktivní/neaktivní/zablokovaný, teplota (0–1), počáteční bod odvozený z konfigurovatelného offsetu muzzle a směru pohledu, koncový bod, kolizní tloušťka (výchozí 16 px), zasažený cíl.
- **Plošina**: obdélník pevné plochy definovaný pozicí a rozměry, identifikátor assetu.
- **Propast**: svislá hranice pádu a vodorovný rozsah, po jehož překročení dolů dojde ke ztrátě energie.
- **Východ**: pozice, rozměry, stav aktivní/neaktivní.
- **Prostředí**: identifikátor, zobrazovaný název, pořadí, startovní pozice, seznam plošin, propast, definice protivníka, východ, odkazy na assety.
- **Postup demem**: index aktuálního prostředí, pevná posloupnost tří prostředí, stav dokončení.
- **Registr assetů**: mapování stabilních interních identifikátorů na soubory obrázků a zvuků.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Hráč, který demo nikdy neviděl, dokončí celé tři prostředí od úvodní po závěrečnou obrazovku pouze klávesnicí, bez jakýchkoli dalších instrukcí.
- **SC-002**: Demo běží po celou dobu průchodu na cílové obnovovací frekvenci 60 FPS bez viditelného trhání.
- **SC-003**: Při umělém kolísání snímkové frekvence mezi 30 a 60 FPS zůstane výška skoku, dolet skoku i doba přehřátí laseru shodná v mezích 5 %.
- **SC-004**: Protivník je poražen souvislým laserem v rozmezí 0,9–1,1 sekundy celkového působení.
- **SC-005**: Laser se přehřeje po 1,4–1,6 sekundy nepřerušené střelby.
- **SC-006**: Nezranitelnost po zásahu trvá 0,9–1,1 sekundy.
- **SC-007**: Coyote time je použitelný 90–110 ms po opuštění plochy; jump buffer přijme skok stisknutý 110–130 ms před dopadem.
- **SC-008**: Všechny tři JSON soubory prostředí se načtou stejným loaderem bez jediné výjimky specifické pro konkrétní prostředí.
- **SC-009**: Celá automatická testovací sada projde headless na Linuxu, Windows i macOS.
- **SC-010**: GitHub Actions vytvoří tři stažitelné artefakty (Windows x64, macOS Apple Silicon, macOS Intel) v rámci jednoho běhu.
- **SC-011**: Stažený artefakt se na cílovém systému spustí a umožní dokončit celé demo bez nainstalovaného Pythonu.
- **SC-012**: Nahrazení libovolného placeholderového obrázku souborem stejného identifikátoru se projeví ve hře bez jediné změny v herní logice.
- **SC-013**: Spec Kit `converge` nenajde nevyřešený rozdíl mezi specifikací a implementací.
- **SC-017**: Opakované spuštění generátoru placeholderů nad nezměněným vstupem nezmění ani jeden bajt verzovaných assetů; shoda je ověřitelná porovnáním checksumů před a po spuštění.
- **SC-018**: V zabaleném buildu bez konzole vede záměrně poškozený JSON prostředí k viditelné chybové obrazovce uvádějící název souboru i chybné pole; aplikace nikdy neskončí tiše ani bez zprávy.
- **SC-019**: Na displeji s vyšším rozlišením než 1920 × 1080 i na displeji s jiným poměrem stran než 16:9 zabírá herní obraz maximální možnou plochu při zachovaném poměru 16:9, zbytek je černý a herní souřadnice zůstávají shodné se souřadnicemi na 1920 × 1080.
- **SC-020**: Protivník zasažený laserem ve dvou nebo více oddělených dávkách je poražen po stejném celkovém čase působení jako při jedné souvislé dávce (0,9–1,1 s).
- **SC-021**: Změna offsetu výstupního bodu laseru nebo jeho kolizní tloušťky v centrální konfiguraci se projeví v chování i ve vykreslení laseru bez jediné změny v logice entit nebo ve vykreslovacím kódu; výchozí kolizní tloušťka je 16 px.
- **SC-023**: Manifest obsahuje osm samostatně adresovatelných póz Alzáka ze společného transparentního atlasu; runtime render vybírá idle/mrknutí, tři běhové fáze, skok, střelbu a zásah podle stavu simulace.
- **SC-024**: Automatický test projde každou zvýšenou plošinu ve všech třech prostředích pouze sekvencí pohybu a skoku; test neupravuje souřadnice hráče přímo.
- **SC-025**: Laser bez zásahu končí přesně po nakonfigurovaném dosahu 900 px nebo na hraně logické obrazovky, podle toho, co nastane dříve.

## Assumptions

Následující rozhodnutí byla přijata tam, kde scope nechával prostor. Jsou závazná,
dokud je zadavatel nezmění.

- **A-001**: Repozitář byl při založení této feature prázdný a spec vznikl výhradně ze scope. Dne 2026-09-03 zadavatel doplnil `AGENTS.md` a `CLAUDE.md`. Tyto soubory jsou závazné a slouží spolu se Spec Kit artefakty jako trvalý předávací bod mezi agenty.
- **A-002**: Pád do propasti (FR-023) a restart prostředí (FR-026) jsou dva odlišné mechanismy. Pád vrací pouze Alzáka a odečítá energii; nevrací protivníka ani východ. Restart obnovuje vše.
- **A-003**: Scope nevyžaduje zvukový efekt zásahu ani ztráty energie; odezva na zásah je čistě vizuální. Zvuková sada zůstává přesně na pěti efektech z FR-058.
- **A-004**: Uživatelské rozhraní a texty jsou v češtině, protože takto je scope formuluje. Lokalizace není v rozsahu.
- **A-005**: Placeholderová hudba, zvuky a zbývající pomocné obrázky jsou generovány programově skriptem v repozitáři, aby byly reprodukovatelné a bez licenčních závazků. Autorské bitmapy výslovně požadované výtvarnou revizí (atlas Alzáka a tři pozadí) jsou verzované ImageGen výstupy s checksumem a generátor je nepřepisuje. **Upřesněno 2026-09-03 (rozhodnutí C2 a OD-008):** vygenerované soubory se **verzují** v repozitáři a generátor v něm **zůstává**. Hra při běžném spuštění používá výhradně uložené assety; generování za běhu není součástí herního toku. Viz FR-081, FR-082, FR-091, SC-017.
- **A-006**: Escape na úvodní, závěrečné obrazovce a obrazovce neúspěchu neaktivuje pauzu; slouží jako návrat nebo nemá efekt. Pauza existuje pouze během hraní.
- **A-007**: Demo nemá ukládání postupu. Ukončení aplikace zahodí veškerý stav.
- **A-008**: Cílem není podpora herních ovladačů, myši ani dotykového ovládání.
- **A-009**: macOS buildy jsou nepodepsané a nenotarizované; uživatel je spouští s vědomím varování Gatekeeperu. Windows build je nepodepsaný.
- **A-010**: Při souběhu poražení protivníka a vyčerpání energie ve stejném snímku má přednost neúspěch (viz Edge Cases).
- **A-011**: Precedence pokynů se řídí `AGENTS.md` §1 v podobě zapsané v `.specify/memory/constitution.md`, sekce Instruction Precedence. Scope zadavatele má autoritu 1; tato specifikace autoritu 5. Nálezy a rozhodnutí jsou trvale evidovány v `analysis-report.md` a `open-decisions.md`, nikdy pouze v konverzaci.
- **A-012**: Rozhodnutím OD-007 zadavatel výslovně vyřadil vývojářskou feedback pipeline z feature. Dřívější A-012…A-014 jsou nahrazeny; nevzniká feedback kód, úložiště, ovládací klávesa ani testovací výjimka.
