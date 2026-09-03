# Feedback Pipeline Requirements Quality Checklist: Alzák tech demo (US6)

**Purpose**: Kontrola **kvality zápisu požadavků** vývojářského feedback pipeline
(FR-066…FR-080, FR-088) vůči kanonické politice `feedback_pipeline_standalone.md`
a vůči rozsahu schválenému v OD-001 (V2, bootstrap minimum).
**Created**: 2026-09-03
**Feature**: [spec.md](../spec.md) · [contracts/feedback-package.md](../contracts/feedback-package.md) · [contracts/feedbackctl.md](../contracts/feedbackctl.md)
**Depth**: release gate | **Audience**: recenzent (Claude) + implementátor (Codex)

**Review Ownership**: Reviewer-owned requirements-quality review artifact.
**Marker Semantics**: `[x]` = kritérium kvality požadavku přezkoumáno a splněno. **Neznamená** hotovou implementaci.

> **Pozor na §21.28**: kanonické prvky politiky se **nepředefinovávají**. Položky
> níže kontrolují, zda projektové artefakty politiku *správně odkazují*, ne zda ji
> kopírují.

## Rozsahová disciplína (OD-001)

- [ ] CHK090 Je pokryto **všech devět** položek bootstrap minima dle §21.30, a je u každé zapsáno, co je „nejmenší vyhovující rozsah"? [Completeness, OD-001 bod 1]
- [ ] CHK091 Je testovací rozsah omezen přesně na to, co §21.30 vyžaduje, a je odchylka od Principu VI výslovně zapsána? [Consistency, Constitution §VI, OD-001 bod 2]
- [ ] CHK092 Je priorita P6 zapsána tak, že z ní plyne pořadí v `tasks.md`, ne jen slovní zmínka? [Clarity, OD-006 bod 6]
- [ ] CHK093 Neobsahují požadavky US6 nic nad rámec bootstrap minima (žádná „hezká" rozšíření)? [Consistency, Constitution §I]

## Produkční vyloučení (§21.2)

- [ ] CHK094 Je požadavek na vyloučení zapsán jako **strukturální**, ne jako runtime příznak? [Clarity, Spec §FR-066]
- [ ] CHK095 Je zapsáno, čím se vyloučení **testuje**, a je test popsán tak, že jeho selhání je jednoznačné? [Measurability, Spec §SC-014]
- [ ] CHK096 Je vyloučení **zdokumentováno** — tedy existuje místo, kde se dočte, proč a jak? [Completeness, §21.2 „documented"]
- [ ] CHK097 Je zapsáno, jak se chová výslovně označený **test build** (na rozdíl od dev a produkčního)? [Coverage, Spec §FR-066]
- [ ] CHK098 Je jednoznačné, že F8 v produkčním buildu nemá **žádný pozorovatelný** efekt, ne jen že nic neotevře? [Clarity, Spec §FR-088, §SC-022]

## Dostupnost a integrace (§21.3, §21.30)

- [ ] CHK099 Je zapsáno, že integrace je **jediná root-level**, a nikoli opakovaná po obrazovkách? [Clarity, Spec §FR-067]
- [ ] CHK100 Je požadavek na viditelný indikátor odlišený od produkčního UI zapsán měřitelně? [Measurability, Spec §FR-068]
- [ ] CHK101 Je pokryto, že nástroj je dostupný **z každé** aktivní herní obrazovky, včetně pauzy, neúspěchu a přechodu? [Coverage, Spec §FR-067]
- [ ] CHK102 Je definováno, co se stane při stisku F8 na **chybové** obrazovce? [Gap]

## Snímek a důkazní materiál (§21.3, §21.4, §21.9)

- [ ] CHK103 Je požadavek „ovládací prvek není ve snímku" doplněn o způsob ověření **proti skutečnému souboru**? [Measurability, Spec §FR-069]
- [ ] CHK104 Je zapsáno, že se uchovávají **oba** obrázky a že se původní nikdy destruktivně nepřepíše? [Completeness, Spec §FR-070]
- [ ] CHK105 Je definováno chování při **selhání** pořízení snímku (výslovná značka, nikdy prázdný obrázek)? [Coverage, Spec §Edge Cases]
- [ ] CHK106 Je zapsán požadavek na **normalizované** souřadnice anotací a je vysvětleno proč? [Clarity, Spec §FR-071]
- [ ] CHK107 Je definován minimální nástroj anotačního editoru (volná tužka) bez otevřeného výčtu „a další"? [Clarity, Spec §FR-071]

## Degradace platformy (§21.4, §21.6)

- [ ] CHK108 Je zapsáno, že `audio` a `transcription` jsou na této platformě **vždy** nedostupné, a je to viditelné i za běhu? [Clarity, Spec §FR-072, §A-013]
- [ ] CHK109 Je zákaz síťového fallbacku zapsán výslovně? [Completeness, Spec §FR-072]
- [ ] CHK110 Je zapsáno, že se pipeline nesmí označit za funkční v části bez end-to-end důkazu? [Consistency, §21.29, Constitution]
- [ ] CHK111 Je SC-015 formulováno tak, že rozlišuje „nedostupné a označené" od „tiše přeskočené"? [Measurability, Spec §SC-015]

## Integrita položky (§21.7, §21.8, §21.9, §21.11)

- [ ] CHK112 Je definováno, co je „dostatečný kontext" pro odmítnutí prázdné zpětné vazby? [Clarity, Spec §FR-073]
- [ ] CHK113 Je formát stabilního ID zapsán přesně dle §21.8, včetně **UTC** data? [Consistency, Spec §FR-074]
- [ ] CHK114 Je vyjmenován **celý** povinný kontext dle §21.8 bez vynechaného pole? [Completeness, Spec §FR-075]
- [ ] CHK115 Je zákaz sběru tajemství, tokenů, hesel, klíčů a obsahu jiných aplikací zapsán a promítnut do popisu kontextu? [Completeness, Spec §FR-076]
- [ ] CHK116 Je „atomická publikace" (FR-077) zapsána konkrétním mechanismem, ne jen slovem? [Clarity, research §R11]
- [ ] CHK117 Je definováno, co se stane s **nedokončeným** balíčkem po pádu aplikace? [Coverage, Spec §Edge Cases, §21.25]
- [ ] CHK118 Je deduplikace zapsána tak, že je jasné, co je primární klíč a co se **nesmí** změnit při opakovaném `pull`? [Measurability, Spec §FR-078, §SC-016]

## Agentní rozhraní (§21.13, §21.14, §21.20)

- [ ] CHK119 Je vyjmenováno **všech jedenáct** operací FR-079 a má každá zapsanou sémantiku a návratový kód? [Completeness, contracts/feedbackctl.md]
- [ ] CHK120 Je „deterministicky" u operací vysvětleno (stejný stav + argumenty ⇒ stejný výstup)? [Clarity, Spec §FR-079]
- [ ] CHK121 Je zapsáno, že `complete` **bez důkazu selže**, ne že se jen nedoporučuje? [Clarity, Spec §FR-080]
- [ ] CHK122 Je zákaz skrytých koncových stavů zapsán a je jasné, co „skrytý koncový stav" znamená? [Clarity, Spec §FR-080]
- [ ] CHK123 Je popsáno, co dělá agent, když pipeline **ještě neexistuje** (fáze P0–P7) — hlásí nedostupnost, netvrdí přezkum? [Coverage, §21.16, Constitution]
- [ ] CHK124 Je zapsán požadavek na neosiřelé `in_progress` claimy při handoffu? [Completeness, `CLAUDE.md` §14]

## Consistency napříč artefakty

- [ ] CHK125 Neduplikuje žádný projektový artefakt kanonickou politiku způsobem, který §21.28 zakazuje? [Consistency]
- [ ] CHK126 Souhlasí rozsah US6 ve `spec.md`, `constitution.md`, `open-decisions.md` (OD-001) a `plan.md` beze zbytku? [Consistency]
- [ ] CHK127 Je klávesa F8 zapsána shodně ve `spec.md` (FR-088), `data-model.md` (`config.FEEDBACK`) a `contracts/input-map.md`? [Consistency, OD-006]
- [ ] CHK128 Je vazba US6 na runtime závislosti zapsána tak, že nemůže dojít k přidání runtime dependency? [Consistency, Spec §A-013]

## Notes

- Politika `feedback_pipeline_standalone.md` má vyšší autoritu než tento checklist
  (Instruction Precedence bod 3). Při rozporu vítězí politika a rozpor se zapíše
  do `open-decisions.md`.
- `$speckit-implement` čte stav zaškrtnutí jako bránu a nesmí jej měnit.
