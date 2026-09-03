# Analýza konzistence: projektové MD soubory ↔ Spec Kit artefakty

**Datum**: 2026-09-03
**Fáze**: po `specify`, před `clarify`
**Branch**: `master` · **HEAD**: `4040592`
**Analyzované zdroje**:

| Zdroj | Typ | Řádků | Autorita (AGENTS.md §1) |
|---|---|---|---|
| Scope zadavatele, sekce 1–20 | explicitní pokyn uživatele pro aktuální úkol | — | **1 (nejvyšší)** |
| `AGENTS.md` | generický agentní řád | 898 | 7 |
| `CLAUDE.md` | Claude-specifický řád | 266 | 4 |
| `feedback_pipeline_standalone.md` | kanonická univerzální politika | 881 | 3 (governing document) |
| `.specify/memory/constitution.md` v1.0.0 | constitution | 128 | 3 |
| `specs/001-alzak-platformer-demo/spec.md` | aktivní specifikace | 306 | 5 |

**Poznámka k autoritě**: constitution v1.0.0 byla napsána **dříve**, než uživatel doplnil MD soubory. Nemohla je tedy reflektovat. Všechna zjištění B* jsou důsledkem tohoto pořadí, ne rozporu v záměru.

---

## Souhrn

| Závažnost | Počet | Blokuje `plan`? |
|---|---|---|
| CRITICAL | 1 | **ano** |
| HIGH | 4 | ano (mechanická náprava) |
| MEDIUM | 5 | ne |
| LOW | 4 | ne |
| Disclosure | 3 | ne |

Jediné skutečně **materiální** rozhodnutí, které nelze bezpečně učinit z dostupného
kontextu, je **A1**. Vše ostatní je náprava, kterou lze provést bez dalšího vstupu.

---

## A. Rozpory v produktovém rozsahu

### A1 — CRITICAL — Vývojářský feedback pipeline je povinný, ale není ve scope ani ve spec

**Rozpor:**

`feedback_pipeline_standalone.md` §21.1:
> „Every project with a user-facing interface **must** provide a developer feedback
> pipeline in development and explicitly designated test builds."
> „Applicable platforms include web, iOS/iPadOS, macOS, Android, Windows, Linux,
> **games**, embedded GUIs, internal tools, and administration panels."

§21.30 (Bootstrap/adoption):
> „Establish **before or alongside first navigable shell** when the project adopts
> this universal standard."

Proti tomu:

- Scope zadavatele (sekce 4 „CÍL MVP", sekce 18 „DEFINICE HOTOVÉHO MVP") feedback
  pipeline **nikde nezmiňuje**.
- `constitution.md` Princip I (Scope-First, NON-NEGOTIABLE): „Implementuje se přesně
  to, co je ve scope — nic víc."
- `spec.md` neobsahuje jediný požadavek FR-001…FR-065 týkající se feedbacku.

**Rozsah dopadu, pokud se přijme** (§21.30 bootstrap minimum):

1. development/test enablement (`DEVELOPER_FEEDBACK_ENABLED`),
2. root-level plovoucí ovládací prvek nad herní smyčkou pygame,
3. jeden platformní adaptér (capture, anotace, mikrofon, transkripce),
4. kanonický balíček (`feedback.md`, `context.json`, screenshoty, audio, checksums),
5. lokální durable fronta se stavy `capturing/queued/transferring/synced/transfer_failed`,
6. konfigurace úložiště,
7. agentní rozhraní `feedbackctl` (12 operací dle §21.13),
8. test vyloučení z produkčního buildu,
9. jeden end-to-end test pipeline (§21.27 má 22 kroků).

Odhad: srovnatelný nebo větší objem práce než celé herní demo. V pygame navíc
neexistuje nativní overlay/accessibility strom ani OS transkripce — §21.5 „semantic
target data" a §21.6 „on-device/OS transcription" by vyžadovaly vlastní implementaci.

**Proč to nelze rozhodnout bez zadavatele** (CLAUDE.md §12): mění to rozsah,
akceptační kritéria, definici hotového MVP i harmonogram. Precedence sama rozpor
neřeší — scope má autoritu 1, ale *mlčí*; feedback politika má autoritu 3 a *mluví*.
Mlčení scope není explicitní zamítnutí.

**Co politika sama předepisuje pro tento případ** — §21.30, „For existing projects
lacking it":
> „1. report missing universal requirement; 2. inspect UI/build architecture;
> 3. propose smallest root-level integration; 4. avoid scattered one-off buttons;
> 5. **implement adapter when current task includes adoption**; 6. verify coverage."

Bod 5 je podmíněný. Aktuální úkol (scope 1–20) adopci **neobsahuje**. Kroky 1–3 tímto
dokumentem plním; krok 5 čeká na rozhodnutí zadavatele.

**Navržené varianty** — viz `open-decisions.md`, OD-001.

---

## B. Mezery v constitution v1.0.0 vůči AGENTS.md / CLAUDE.md

### B1 — HIGH — Chybí precedenční model instrukcí

`AGENTS.md` §1 definuje osmiúrovňovou precedenci. Constitution v1.0.0 pouze říká,
že „má přednost před zvyklostmi a preferencemi", a neurčuje svůj vztah k `AGENTS.md`,
`CLAUDE.md`, feedback politice ani k pokynům uživatele.

**Náprava**: doplnit do constitution sekci „Instruction precedence" přebírající
`AGENTS.md` §1 doslovně a explicitně zařadit tento projekt do jeho modelu.

### B2 — HIGH — Chybí Git policy; už došlo k odchylce

`AGENTS.md` §5.3:
> „Commit or push only when: the user explicitly requested it; or repository-specific
> instructions explicitly require it."

Constitution v1.0.0 o commitech mlčí. Commit `4040592` („chore: bootstrap Spec Kit…")
byl proveden **bez explicitního pokynu uživatele** a **přímo na `master`**. Viz E1.

**Náprava**: doplnit do constitution sekci „Git policy" s odkazem na `AGENTS.md`
§5.1–§5.3 a §14, včetně seznamu zakázaných akcí.

### B3 — HIGH — Chybí povinný formát závěrečného reportu a handoffu

`AGENTS.md` §19 předepisuje strukturu: Result / Files changed / Validation /
Resources / Risks / Feedback pipeline / Session handoff.
`CLAUDE.md` §9 předepisuje 13položkový blok „Session handoff".
`AGENTS.md` §15.9 předepisuje cross-agent handoff blok.

Constitution ani spec je nezmiňují. Přitom scope sekce 3 staví Spec Kit artefakty
jako předávací bod mezi Claude a Codex — handoff je tedy pro projekt zásadní.

**Náprava**: doplnit do constitution sekci „Reporting a handoff" odkazující na
`AGENTS.md` §19 a `CLAUDE.md` §9 jako závazný formát.

### B4 — HIGH — Chybí povinný CONTEXT marker; nebyl vydán v předchozím checkpointu

`CLAUDE.md` §8 a `AGENTS.md` §15.6:
> „At every major checkpoint report **exactly one**: `CONTEXT: SAFE TO CLEAR` /
> `CONTEXT: COMPACT RECOMMENDED` / `CONTEXT: KEEP CURRENT SESSION`"

Checkpoint po dokončení `specify` (předchozí odpověď) tento marker **neobsahoval**,
protože soubory v té chvíli v repozitáři nebyly. Od této chvíle povinné.

**Náprava**: doplnit do constitution; marker vydávat na každém checkpointu.

### B5 — MEDIUM — Napětí: „celá testovací sada" vs. „nejužší rozsah testů"

| Zdroj | Požadavek |
|---|---|
| Scope §16 (autorita 1) | „spusť **celou** dosavadní testovací sadu" po každé funkci |
| Constitution VI (autorita 3) | totéž, převzato ze scope |
| `AGENTS.md` §13 (autorita 7) | „Run the **narrowest** test scope that proves the change" |

**Vyhodnocení**: **není to rozpor vyžadující zásah zadavatele.** Precedence jej řeší —
scope má autoritu 1. Navíc `AGENTS.md` §13 uvádí plnou sadu jako legitimní úroveň 5
a u dema této velikosti trvá plný běh jednotky sekund, takže „nejužší rozsah, který
poskytuje smysluplný důkaz" a „celá sada" prakticky splývají.

**Náprava**: zapsat do constitution jako **vědomou, odůvodněnou odchylku**, aby ji
budoucí agent nepovažoval za porušení `AGENTS.md`.

### B6 — MEDIUM — Chybí implementační checkpointy a zákaz automatického přechodu mezi fázemi

`CLAUDE.md` §3: „`/speckit-plan` does not authorize `/speckit-tasks`."
`CLAUDE.md` §4 a `AGENTS.md` §15.4: výchozí stop-pointy pro `implement` = Setup,
Foundational, každá user story, každá major fáze.

Constitution v1.0.0 popisuje workflow, ale neurčuje, že se mezi fázemi **zastavuje**.
Scope §19 dává 20krokové pořadí, které je s checkpointy plně slučitelné
(mapuje se na Setup → Foundational → US1…US5).

**Náprava**: doplnit do constitution; zmapovat scope §19 na user stories US1–US5.

---

## C. Faktická neaktuálnost specifikace

### C1 — HIGH — `spec.md` tvrdí, že repozitář je prázdný

Dvě místa jsou nyní nepravdivá:

- Hlavička **Input**: „…repozitář byl při zahájení prázdný a neobsahoval žádné
  konkurenční projektové MD soubory."
- **A-001**: „…jediným zdrojem projektových pravidel je scope zadavatele.
  `AGENTS.md` a `CLAUDE.md` **budou v rámci této feature vytvořeny**…"

Obě tvrzení platila v okamžiku zápisu a přestala platit doplněním MD souborů.
Ponechat je znamená, že by budoucí agent mohl `AGENTS.md`/`CLAUDE.md` přepsat
vlastní verzí — přímé porušení `AGENTS.md` §2.6 a §4.2.

**Náprava**: přepsat Input a A-001; doplnit A-011 o precedenci MD souborů;
podle rozhodnutí OD-001 doplnit A-012 o feedback pipeline.

### C2 — MEDIUM — A-005 nerozhoduje commit vs. generování assetů

A-005 říká, že placeholdery jsou generovány programově, ale neurčuje, zda se
**verzují**. Rozhodnutí ovlivňuje FR-065 (buildy obsahují assety), CI a `.gitignore`.

**Doporučení do `plan.md`**: generované soubory **verzovat** (jsou deliverable dle
FR-049, deterministické, jednotky až desítky kB) **a zároveň** ponechat generátor
`tools/gen_placeholder_assets.py` kvůli reprodukovatelnosti a snadné výměně za
finální grafiku dle FR-050. Odpadá tím krok navíc v CI i při běhu ze zdroje.

---

## D. Praktická a technická zjištění

### D1 — VYŘEŠENO (bylo MEDIUM) — Soubor se jmenoval `agents.md`, nikoli `AGENTS.md`

`CLAUDE.md` úvod: „Claude MUST read and obey the applicable **`AGENTS.md`** first."
`AGENTS.md` §1 bod 4 a §16 rovněž odkazují na `AGENTS.md`.

Ověřeno: svazek je APFS **case-insensitive**, takže `test -f AGENTS.md` lokálně
projde. Na Linuxu (GitHub Actions dle scope §17) a u nástrojů s přesným porovnáním
názvu — včetně Codexu, který hledá `AGENTS.md` — se soubor **nenajde**.

**Provedeno** 2026-09-03 se souhlasem zadavatele (OD-002 → V1). Ověřeno přesným
porovnáním názvu. Původní náprava vyžadovala souhlas dle (`AGENTS.md` §4.2
„moving unrelated files"). Viz OD-002.

### D2 — LOW — Feedback pipeline není nakonfigurován, start-of-session protokol nelze spustit

`CLAUDE.md` §2 bod 7 a `AGENTS.md` §3.1 bod 11 vyžadují spuštění start-of-session
protokolu feedback pipeline. Ověřeno: neexistuje `feedback-store/`, `feedbackctl`
ani jiná konfigurace.

Dle §21.16 poslední odstavec: „If unavailable, **report failure** before claiming
session review complete." Tímto hlásím: **pipeline není nakonfigurován, health-check
ani pull nebyl proveden, žádné položky nebyly načteny.** Netvrdím, že přezkum
feedbacku proběhl.

### D3 — LOW — Neexistuje machine-specific storage policy; `$DEV_STORAGE_ROOT` není nastaven

`AGENTS.md` §17 a feedback §21.10 předpokládají možnou existenci strojové politiky
úložiště. Ověřeno: v repozitáři ani v `~/.claude/` žádná není, proměnná je prázdná.

**Důsledek**: platí generické chování `AGENTS.md`. Build artefakty PyInstalleru
půjdou do repo-local `dist/` a `build/` (obojí už v `.gitignore`). Žádný krok
nesmí zapisovat na cizí svazek ani hardcodovat uživatelskou cestu (`AGENTS.md` §17).

### D4 — LOW — Nekonzistentní názvosloví Spec Kit příkazů; `checklist` a `converge` chybí v obou MD

| Zdroj | Uvedené fáze |
|---|---|
| `AGENTS.md` §15.3 | `/specify /clarify /plan /tasks /analyze /implement` |
| `CLAUDE.md` §3 | `/speckit-specify … /speckit-implement` |
| Nainstalované skilly | `speckit-*` (10 ks) |
| Scope §2 (autorita 1) | constitution, specify, clarify, plan, **checklist**, tasks, analyze, implement, **converge** |

Ani `AGENTS.md`, ani `CLAUDE.md` nezná `checklist` a `converge`. Nejde o rozpor —
scope má vyšší autoritu a fáze pouze **přidává**; oba skilly jsou nainstalované.
Pravidlo „po major fázi zastav" (`CLAUDE.md` §3) se na ně vztahuje analogicky.

**Náprava**: zapsat do constitution úplný devítifázový řetězec včetně `checklist`
a `converge` a označit je za major fáze.

---

## E. Disclosure — provedené akce vůči nyní platné politice

### E1 — Commit `4040592` bez explicitního pokynu, na `master`

Provedeno dříve, než byly MD soubory v repozitáři. Nyní by šlo o porušení
`AGENTS.md` §5.3.

**Neopravuji.** `AGENTS.md` §5.2 zakazuje `git reset --hard` i amend bez autorizace
a §13 („Git and context safety") zakazuje mazat práci kvůli hygieně. Commit
ponechávám a hlásím. Pokud jej chceš vrátit, řekni to výslovně.

Obsah commitu: scaffold Spec Kitu, `.gitignore`, constitution v1.0.0. Žádné
tajemství, žádná strojově specifická cesta, žádná cizí práce.

**Aktuálně necommitnuté**: `specs/`, `CLAUDE.md`, `AGENTS.md`,
`feedback_pipeline_standalone.md`. Ponechávám v pracovním stromu.

### E2 — Úprava generovaných souborů Spec Kitu

Změněno: `.specify/integration.json` (registrace **obou** integrací, default `claude`)
a `.specify/init-options.json` (`"ai": "codex"` → `"claude"`). Důvod: `specify init`
při druhém spuštění pro Codex přepsal registraci a smazal Claude. Bez opravy by
nástroj považoval projekt za výhradně Codexový, ačkoli scope §3 vyžaduje oba agenty.

### E3 — Feature 001 běží na `master`, ne na vlastní branchi

`create-new-feature.sh` samostatnou branch nevytvořil (repozitář měl v tu chvíli
jediný commit). Doporučení: před `implement` přesunout na `001-alzak-platformer-demo`.
Vyžaduje souhlas.

---

## Co je naopak v pořádku

Bez nálezu prošly:

- **Constitution I–VII vs. scope 1–20**: úplná shoda, žádné pravidlo scope není
  vynecháno ani oslabeno.
- **Constitution vs. `AGENTS.md` §2 (Core operating principles)**: Princip I
  odpovídá bodům 2/7/15, Princip IV bodu 5, Princip VI bodům 11/12.
- **`spec.md` FR-001…FR-065 vs. scope 1–20**: každá normativní věta scope má
  odpovídající FR; zpětná kontrola nenašla FR bez opory ve scope.
- **`spec.md` SC-001…SC-013 vs. scope §18**: všech 15 bodů „definice hotového MVP"
  je pokryto měřitelným kritériem.
- **Constitution „Technology Constraints" vs. scope §5**: shoda včetně 1920×1080,
  60 FPS, F11 a nepodepsaných buildů.
- **`CLAUDE.md` §10 (reading discipline)**: dodrženo — cílené čtení, žádné
  vkládání celých governing dokumentů do chatu.
- **`AGENTS.md` §8 (security/privacy)**: žádné tajemství, žádné externí volání
  s privátními daty, žádné oslabení kontrol.
- **`AGENTS.md` §11 (process management)**: nespuštěn žádný dlouhoběžící proces.

---

## Navržené pořadí nápravy

| # | Akce | Artefakt | Blokováno |
|---|---|---|---|
| 1 | Rozhodnout OD-001 (feedback pipeline) | — | **zadavatel** |
| 2 | Rozhodnout OD-002 (`AGENTS.md` → `AGENTS.md`) | — | **zadavatel** |
| 3 | Constitution → v1.1.0: precedence (B1), Git policy (B2), reporting/handoff (B3), CONTEXT marker (B4), odchylka u testů (B5), checkpointy a 9 fází (B6, D4) | `constitution.md` | ne |
| 4 | Oprava Input + A-001, doplnění A-011 (a A-012 dle OD-001) | `spec.md` | částečně OD-001 |
| 5 | Doplnění FR pro feedback pipeline **jen** při volbě „přijmout" | `spec.md` | OD-001 |
| 6 | Teprve poté `clarify` | — | 3, 4 |

**`plan` nelze zahájit, dokud není OD-001 rozhodnuto** — určuje architekturu,
strukturu projektu, testovací strategii i distribuci (produkční vyloučení dle §21.2).

---

## Stav nápravy — aktualizace 2026-09-03

| # | Nález | Stav | Kde |
|---|---|---|---|
| A1 | Feedback pipeline povinný, chyběl ve spec | **vyřešeno** | OD-001 → V2; constitution sekce „Vývojářský feedback pipeline"; spec US6, FR-066…FR-080, SC-014…SC-016, A-012, A-013 |
| B1 | Chybí precedenční model | **vyřešeno** | constitution → „Instruction Precedence"; spec A-011 |
| B2 | Chybí Git policy | **vyřešeno** | constitution → „Git policy" včetně OD-003 |
| B3 | Chybí formát reportu a handoffu | **vyřešeno** | constitution → „Reporting a handoff" |
| B4 | Chybí CONTEXT marker | **vyřešeno** | constitution → „Reporting a handoff"; marker vydáván od tohoto checkpointu |
| B5 | Napětí „celá sada" vs. „nejužší rozsah" | **vyřešeno** | constitution Princip VI → zdokumentovaná odchylka od `AGENTS.md` §13 |
| B6 | Chybí fázové a implementační checkpointy | **vyřešeno** | constitution → „Spec Kit fáze a checkpointy" |
| C1 | spec tvrdil prázdný repozitář | **vyřešeno** | spec hlavička **Input** + A-001 přepsány |
| C2 | A-005 nerozhoduje commit vs. generování assetů | **odloženo do `plan.md`** | doporučení: verzovat generované assety a ponechat generátor |
| D1 | `agents.md` vs. `AGENTS.md` | **vyřešeno** | přejmenováno, ověřeno přesným porovnáním názvu (OD-002) |
| D2 | Feedback pipeline nekonfigurován | **trvá, hlášeno** | vyřeší implementace US6; do té doby se protokol hlásí jako nedostupný |
| D3 | Chybí strojová politika úložiště | **vyřešeno** | constitution → Technology Constraints; spec A-014 |
| D4 | Názvosloví fází; chybí `checklist` a `converge` | **vyřešeno** | constitution → „Spec Kit fáze a checkpointy" (9 fází, prefix `speckit-`) |
| E1 | Commit `4040592` bez pokynu | **hlášeno, nevraceno** | OD-003; constitution „Git policy", poznámka k historii |
| E2 | Úprava generovaných souborů Spec Kitu | **hlášeno** | tento report, sekce E2 |
| E3 | Feature na `master` | **vyřešeno** | práce přesunuta na branch `001-alzak-platformer-demo` (OD-003 → V1) |

**Zbývá otevřené**: pouze C2, které je rozhodnutím pro `plan.md`, nikoli rozporem
mezi podklady. Žádný nález neblokuje fázi `clarify`.

**Ověření po nápravě**:

- `spec.md`: FR-001…FR-080 bez mezer, SC-001…SC-016 bez mezer, A-001…A-014 bez mezer.
- V `specs/` nezůstal jediný odkaz na `agents.md` malými písmeny.
- Constitution v1.1.0 s historií změn.
