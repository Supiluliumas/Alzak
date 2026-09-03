# Otevřená rozhodnutí — feature 001-alzak-platformer-demo

Trvalý záznam nevyřešených vstupů dle `AGENTS.md` §15.1
(„unresolved required input -> tracked blocker/open-input/decision document").

Stav: `open` / `decided` / `superseded`.
Rozhodnutí se po schválení zapíše do nadřazeného artefaktu (constitution nebo spec)
a zde se pouze označí jako `decided` s odkazem. Historie se nemaže.

---

## OD-001 — Adopce vývojářského feedback pipeline

**Stav**: `decided` — 2026-09-03, zadavatel
**Rozhodnutí**: **V2 — přijmout, v nezbytném minimu a s minimem testů.**
**Zapsáno do**: `constitution.md` (sekce Vývojářský feedback pipeline),
`spec.md` (A-012, User Story 6, FR-066…FR-080, SC-014…SC-016)
**Založeno**: 2026-09-03
**Blokovalo**: `plan`, `checklist`, `tasks`, `implement` — odblokováno
**Zdroj rozporu**: `feedback_pipeline_standalone.md` §21.1 a §21.30 vs. scope §4/§18
a `constitution.md` Princip I
**Analýza**: `analysis-report.md` → A1

### Podstata

Kanonická politika označuje feedback pipeline za povinný pro každý projekt
s uživatelským rozhraním a výslovně jmenuje hry. Scope zadavatele jej nezmiňuje.
Politika sama (§21.30) podmiňuje implementaci tím, že „current task includes
adoption" — aktuální úkol ji neobsahuje. Rozhodnutí je proto na zadavateli.

### Varianty

**V1 — Odložit (doporučeno)**
Feedback pipeline se v této feature neimplementuje. Do `spec.md` se doplní
předpoklad A-012, který odchylku výslovně eviduje včetně odkazu na §21.30, a do
`constitution.md` sekce vysvětlující, proč povinnost není v rozporu s Principem I.
Založí se samostatná feature `002-developer-feedback-pipeline` jako budoucí práce.
- MVP dle scope §18 zůstává nedotčené.
- Politika je respektována postupem, který sama předepisuje (report + propose,
  implementace až s úkolem, který adopci obsahuje).
- Riziko: demo buildy nebudou mít vestavěný kanál pro sběr zpětné vazby.

**V2 — Přijmout v minimálním rozsahu**
Implementuje se bootstrap minimum dle §21.30 (9 položek) jako US6 s prioritou P6,
po dokončení herního dema. Adaptér pouze pro pygame/desktop.
- Odhad: srovnatelný objem práce jako celé herní demo.
- Vyžaduje vlastní řešení tam, kde pygame nemá platformní podporu:
  overlay nad herní smyčkou, semantic target (§21.5), on-device transkripce (§21.6).
- Rozšiřuje `spec.md` o ~15 FR, `plan.md` o vrstvu feedbacku,
  `tasks.md` o samostatnou fázi a CI o test produkčního vyloučení (§21.2).
- Posouvá dokončení MVP.

**V3 — Přijmout zjednodušeně, s výslovnou výjimkou**
Implementuje se jen podmnožina: klávesová zkratka pořídí screenshot herního okna,
uloží `context.json` (verze, commit, prostředí, pozice, stav energie/laseru) a
umožní připsat textový popis; balíček jde do lokálního `feedback-store/inbox/<ID>/`
se stabilním ID dle §21.8 a checksumy. **Bez** audia, transkripce, anotačního
editoru, fronty přenosu a `feedbackctl`.
- Zachovává kanonické ID, immutable evidence a strukturu balíčku.
- Vyžaduje písemnou výjimku z §21.5, §21.6, §21.11, §21.13 zapsanou do
  `constitution.md`, protože politika §21.29 zakazuje „claim pipeline operational
  without end-to-end evidence" — pipeline by se tedy **nesměl** označit za funkční,
  jen za částečnou adopci.
- Odhad: malý zlomek V2.

### Přijaté rozhodnutí a jeho výklad

Zvolena **V2**, s výslovným upřesněním zadavatele: *implementuj v nezbytném minimu
a s minimem testů*. Závazný výklad:

1. Implementuje se **všech 9 položek** bootstrap minima dle §21.30, každá v nejmenším
   rozsahu, který politice vyhoví — nikoli v rozsahu hotového produktu.
2. Testy se omezují na **dva testy, které §21.30 sama vyžaduje**: test produkčního
   vyloučení (§21.2) a jeden end-to-end test pipeline (§21.27), plus minimální
   jednotkové testy stabilního ID, checksumů a deduplikace (§21.8, §21.11).
   Širší testovací sada se pro feedback vrstvu nevytváří.
3. Priorita **P6** — až po dokončení herního dema (US1–US5). Herní MVP dle scope §18
   se implementací feedbacku neodkládá.
4. **Omezení platformy se dokumentují, nezastírají.** pygame neposkytuje nativní
   overlay, accessibility strom ani OS transkripci. Kde adaptér schopnost nemá,
   degraduje explicitně (audio unavailable, transcription unavailable) podle
   §21.4 a §21.6, nikdy tiše. Dle §21.29 se pipeline nesmí označit za plně funkční
   v částech, pro které neexistuje end-to-end důkaz.
5. **Závislosti**: feedback vrstva je vývojářský nástroj (§21.2), její případné
   závislosti jsou proto **vývojové**, ne runtime. Constitution Technology
   Constraints tím není porušena. Runtime hry zůstává na samotném `pygame-ce`.

### Historie

- 2026-09-03 — založeno jako `open` na základě nálezu A1 v `analysis-report.md`.
- 2026-09-03 — zadavatel zvolil V2 s upřesněním v nezbytném minimu a s minimem testů.

---

## OD-002 — Přejmenování `AGENTS.md` → `AGENTS.md`

**Stav**: `decided` — 2026-09-03, zadavatel
**Rozhodnutí**: **V1 — přejmenovat.** Provedeno; ověřeno přesným porovnáním názvu
(`AGENTS.md in os.listdir(.)` → True, `AGENTS.md` → False).
**Založeno**: 2026-09-03
**Blokuje**: nic (ale ovlivňuje spolehlivost předání Codexu a CI na Linuxu)
**Analýza**: `analysis-report.md` → D1

### Podstata

`CLAUDE.md` a `AGENTS.md` §1/§16 odkazují na `AGENTS.md`. Skutečný soubor se jmenuje
`AGENTS.md`. Na APFS (case-insensitive) to lokálně funguje; na Linuxu v GitHub
Actions a u nástrojů s přesným porovnáním názvu — včetně Codexu — nikoli.

Přejmenování spadalo pod `AGENTS.md` §4.2 („moving unrelated files"), proto vyžaduje
souhlas.

### Varianty

- **V1 (doporučeno)**: `git mv agents.md AGENTS.md`. Jediný příkaz, odstraní riziko.
- **V2**: ponechat a doplnit do `CLAUDE.md` poznámku o skutečném názvu.
  Riziko zůstává u Codexu a jiných nástrojů.

---

## OD-003 — Autorizace commitů pro tuto feature

**Stav**: `decided` — 2026-09-03, zadavatel
**Rozhodnutí**: **V1 — stálá autorizace commitovat na checkpointech, bez pushe.**
Zapsáno do `constitution.md`, sekce Git policy, jako repozitářová instrukce ve
smyslu `AGENTS.md` §5.3. Push zůstává vždy na samostatné svolení.
**Založeno**: 2026-09-03
**Blokuje**: nic (výchozí chování = necommitovat)
**Analýza**: `analysis-report.md` → B2, E1, E3

### Podstata

`AGENTS.md` §5.3 dovoluje commit jen na výslovný pokyn uživatele nebo když to
repozitářová instrukce výslovně vyžaduje. Žádná taková instrukce neexistuje.
Bez rozhodnutí bude každý commit vyžadovat samostatné svolení, což při
20krokovém plánu implementace (scope §19) znamená mnoho přerušení.

Souvisí: feature 001 běží na `master`, ne na vlastní branchi (E3).

### Varianty

- **V1**: stálá autorizace commitovat na branchi `001-alzak-platformer-demo`
  na každém checkpointu dle `CLAUDE.md` §4, bez pushe. Zapíše se do
  `constitution.md` jako repozitářová instrukce dle §5.3.
- **V2**: commit pouze na výslovné vyžádání (výchozí stav politiky).
- **V3**: jako V1, ale včetně pushe na remote.

### Poznámka

Commit `4040592` vznikl dříve, než byly MD soubory v repozitáři.
Není vracen — `AGENTS.md` §5.2 a §13 zakazují reset/amend bez autorizace.
