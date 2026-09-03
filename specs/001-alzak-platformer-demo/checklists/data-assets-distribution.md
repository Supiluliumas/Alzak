# Data, Assets & Distribution Requirements Quality Checklist: Alzák tech demo

**Purpose**: Kontrola **kvality zápisu požadavků** pro data prostředí, assety
a distribuci (US5 + FR-041…FR-050, FR-061…FR-065, FR-081, FR-082).
**Created**: 2026-09-03
**Feature**: [spec.md](../spec.md) · [contracts/level-format.md](../contracts/level-format.md) · [contracts/asset-manifest.md](../contracts/asset-manifest.md) · [contracts/build-and-ci.md](../contracts/build-and-ci.md)
**Depth**: release gate | **Audience**: recenzent (Claude) + **Codex** jako vlastník assetové práce (OD-004)

**Review Ownership**: Reviewer-owned requirements-quality review artifact.
**Marker Semantics**: `[x]` = kritérium kvality požadavku přezkoumáno a splněno. **Neznamená** hotovou implementaci.

## Requirement Completeness — data prostředí

- [ ] CHK051 Je pro **každé** povinné pole JSON prostředí (FR-046) zapsán typ, rozsah a důvod existence? [Completeness, contracts/level-format.md]
- [ ] CHK052 Jsou zapsány **sémantické** invarianty nad rámec typů (startovní pozice nad plošinou, trasa protivníka nad plošinou, východ mimo propast)? [Completeness]
- [ ] CHK053 Je definován požadavek na minimální tloušťku plošiny a je odůvodněn vazbou na simulační krok? [Clarity, research §R3]
- [ ] CHK054 Je zapsáno, jak se vynucuje pevné pořadí tří prostředí (pole `order` vs. jméno souboru)? [Clarity, Spec §FR-041]
- [ ] CHK055 Je definováno, co se stane při **duplicitním** `order` nebo `id` napříč soubory? [Coverage, Gap]
- [ ] CHK056 Je zapsán požadavek, že data prostředí **neobsahují** laditelné herní hodnoty? [Consistency, Constitution §II]

## Requirement Clarity — chybové chování

- [ ] CHK057 Je formát chybové zprávy (soubor + pole + důvod) zapsán natolik konkrétně, že jde ověřit strojově? [Measurability, Spec §FR-084]
- [ ] CHK058 Je zapsán konkrétní **návratový kód** při selhání validace? [Clarity, Spec §FR-084]
- [ ] CHK059 Je určeno, jak se chybová obrazovka ovládá klávesnicí a čím se zavře? [Completeness, Spec §FR-084]
- [ ] CHK060 Je zapsáno, že chybová obrazovka musí fungovat i v buildu **bez konzole**, a je z toho odvozen požadavek na build (`console=False`)? [Consistency, contracts/build-and-ci.md]
- [ ] CHK061 Je definováno chování při chybějícím souboru prostředí (na rozdíl od poškozeného obsahu)? [Gap]

## Requirement Completeness — assety

- [ ] CHK062 Pokrývá seznam stabilních ID **všech jedenáct** rozlišovaných entit z FR-049 (Alzák, protivník, plošiny, propast, neaktivní východ, aktivní východ, pobočka, sklad, kancelář, energie, teplota laseru)? [Completeness, Spec §FR-049]
- [ ] CHK063 Je počet zvukových efektů přesně pět dle FR-058 a A-003 — bez zvuku zásahu a ztráty energie? [Consistency, Spec §A-003]
- [ ] CHK064 Je zapsán formát a rozměr každého placeholderu tak, aby ho šlo vyrobit bez dalšího dotazu? [Clarity, contracts/asset-manifest.md]
- [ ] CHK065 Je definováno chování registru při **chybějícím ID** vs. **chybějícím souboru**, a liší se? [Coverage]
- [ ] CHK066 Je zapsáno, že výměna placeholderu za finální grafiku nevyžaduje změnu herní logiky, a je to měřitelné? [Measurability, Spec §SC-012]
- [ ] CHK067 Je požadavek na font s českou diakritikou zapsán jako asset s vlastním ID a vlastníkem? [Gap, research §R14, OD-004]

## Requirement Clarity — generátor a verzování

- [ ] CHK068 Je „deterministický" (FR-082) definován jako **bajtová** shoda, ne jen vizuální? [Clarity, Spec §FR-082]
- [ ] CHK069 Je zapsáno, čím se determinismus zajišťuje (jen stdlib, pevné pořadí, žádný čas v metadatech, seedovaný náhodný generátor)? [Completeness, research §R8]
- [ ] CHK070 Je zákaz generování za běhu (FR-081) formulován tak, že pokrývá i **build a CI**, ne jen herní smyčku? [Coverage, Spec §FR-081]
- [ ] CHK071 Je zapsán ověřovací postup pro SC-017 (checksumy před a po), včetně režimu, který nic nepřepisuje? [Measurability, quickstart §4.5]
- [ ] CHK072 Je určeno, kdo je vlastníkem generátoru a assetů, a je to viditelné i v `tasks.md`? [Completeness, OD-004]

## Requirement Completeness — distribuce a CI

- [ ] CHK073 Jsou vyjmenovány **všechny tři** cílové artefakty se svými runnery a názvy? [Completeness, Spec §FR-064, contracts/build-and-ci.md]
- [ ] CHK074 Je zapsáno, co přesně musí balíček obsahovat (Python runtime, herní data, JSON, assety, hudba, zvuky)? [Completeness, Spec §FR-065]
- [ ] CHK075 Je zapsán požadavek, že build joby závisí na zelené testovací sadě? [Gap → řešeno v contracts/build-and-ci.md; ověř, že to spec nebo kontrakt skutečně říká]
- [ ] CHK076 Je definován rozsah testů, které musí běžet headless, a čím se headless režim zapíná? [Clarity, Spec §FR-062, research §R7]
- [ ] CHK077 Je zapsáno, že buildy jsou nepodepsané, a je popsán dopad na uživatele (Gatekeeper)? [Completeness, Spec §A-009]
- [ ] CHK078 Je pokryta situace, kdy runner pro macOS Intel přestane být dostupný? [Coverage, plan §RP-03]

## Acceptance Criteria Quality

- [ ] CHK079 Je SC-008 formulováno tak, že jeho selhání je jednoznačné (existuje výjimka specifická pro jedno prostředí ⇒ selhalo)? [Measurability]
- [ ] CHK080 Je SC-011 ověřitelné bez přístupu k vývojářskému stroji (čistý systém bez Pythonu)? [Measurability]
- [ ] CHK081 Je SC-010 formulováno tak, že vyžaduje **jeden** běh CI, ne tři samostatné? [Clarity, Spec §SC-010]
- [ ] CHK082 Má každý požadavek FR-061…FR-065 alespoň jedno odpovídající SC? [Coverage]

## Dependencies & Assumptions

- [ ] CHK083 Je zapsáno, že runtime závislostí je **výhradně** `pygame-ce`, a je to promítnuto i do požadavků na validaci JSON a generátor? [Consistency, Constitution §Technology Constraints]
- [ ] CHK084 Je zdokumentováno, kam jdou build artefakty a feedback úložiště, a že jsou gitignorované? [Completeness, Spec §A-014]
- [ ] CHK085 Je zapsáno, že do sdíleného kódu nesmí jít strojově specifická cesta? [Completeness, `AGENTS.md` §17]
- [ ] CHK086 Je popsáno, jak se prostředky nacházejí v zabaleném buildu (odlišná kořenová cesta)? [Gap, research §R6]

## Ambiguities & Conflicts

- [ ] CHK087 Není v rozporu požadavek „assety verzovat" (FR-081) s běžnou praxí gitignorovat generované soubory? Je výjimka výslovně odůvodněná? [Ambiguity, Spec §A-005]
- [ ] CHK088 Je jednoznačné, zda `assets/manifest.json` generuje generátor, nebo se udržuje ručně? [Ambiguity, contracts/asset-manifest.md]
- [ ] CHK089 Je jednoznačné, zda `contracts/level.schema.json` hra za běhu používá, nebo je jen dokumentační? [Clarity, research §R5]

## Notes

- Položky CHK062–CHK072 se dotýkají práce, jejímž vlastníkem je **Codex** (OD-004).
  Claude na ně upozorní v handoff bloku, nikdy je tiše neobejde.
- `$speckit-implement` čte stav zaškrtnutí jako bránu a nesmí jej měnit.
