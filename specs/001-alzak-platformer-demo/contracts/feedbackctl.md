# Kontrakt: agentní rozhraní `feedbackctl`

**Vazba**: FR-079, FR-080 · `feedback_pipeline_standalone.md` §21.13, §21.14,
§21.16, §21.20, §21.25, §21.27 · SC-015, SC-016

Spouštění: `python -m alzak_devtools.feedbackctl <operace> [argumenty]`
Dostupné **pouze** ve vývojovém stromu — v produkčním balíčku balíček neexistuje.

Všechny operace jsou **deterministické**: stejný stav úložiště + stejné argumenty
⇒ stejný výstup a stejný návratový kód. Výstup je čitelný člověku; `--json`
přepne na strojový tvar.

## Operace

| Operace | Argumenty | Sémantika | Exit |
|---------|-----------|-----------|------|
| `doctor` | — | Ověří úložiště: existenci `inbox/`, `archive/`, `quarantine/`, zbytky ve `.staging/` (přesune do `quarantine/` s výslovnou chybou), platnost `item.json` a checksumů. Hlásí i to, co **nedokáže** ověřit. | 0 = zdravé, 1 = nálezy |
| `pull` | `[--source PATH]` | Načte nové položky do kanonického úložiště. **Idempotentní**: existující ID se nepřepisuje, důkazní materiál se nemění (SC-016). | 0 |
| `list` | `[--state open\|in_progress\|done] [--json]` | Vypíše položky: ID, typ, stav, prostředí, UTC. Pevné řazení podle ID. | 0 |
| `show` | `<ID> [--json]` | Vypíše plný obsah položky včetně kontextu, příloh, odpovědí a historie. | 0, 2 = neznámé ID |
| `respond` | `<ID> --text "…"` | Připojí odpověď agenta do `responses[]`. Nemění `work_state`. | 0 |
| `claim` | `<ID>` | `open` → `in_progress`. Na položce, která už je `in_progress`, selže s výslovnou chybou. | 0, 1 = konflikt |
| `release` | `<ID>` | `in_progress` → `open`. Používá se, když práce nebude pokračovat (`CLAUDE.md` §14). | 0 |
| `complete` | `<ID> --evidence "…"` | `in_progress` → `done`. **Bez `--evidence` selže** (FR-080, §21.20). | 0, 1 = chybí důkaz |
| `reopen` | `<ID> --reason "…"` | `done` → `open`, ID i historie zůstávají. | 0 |
| `sync-status` | `[--json]` | Vypíše `transfer_state` všech položek a počty podle stavu. | 0 |
| `verify` | `[<ID>]` | Přepočítá SHA-256 příloh a porovná s `checksums.json`. Neshoda = tvrdá chyba, položka jde do `quarantine/`. | 0, 1 = neshoda |

## Zásady

1. **Žádný skrytý koncový stav.** Pracovní stav má výhradně hodnoty
   `open`, `in_progress`, `done` (FR-080).
2. **`done` jen s důkazem.** `complete` bez `--evidence` selže, nikdy neuspěje tiše.
3. **Poškozené položky do `quarantine/`**, vždy s výslovnou chybou popisující
   co a proč (§21.25). Nikdy tiše do `inbox/`.
4. **Historie se nemaže.** Každý přechod přidá záznam do `history[]`.
5. **Nedostupnost se hlásí.** Není-li úložiště k dispozici, agent hlásí
   `feedback pipeline unavailable` a **netvrdí**, že přezkum proběhl (§21.16,
   `constitution.md` sekce Vývojářský feedback pipeline).
6. **Neosiřelé claimy** (`CLAUDE.md` §14): před handoffem se `in_progress`
   položky buď dokončí, nebo uvolní přes `release`.

## Start-of-session protokol

```text
python -m alzak_devtools.feedbackctl doctor
python -m alzak_devtools.feedbackctl pull
python -m alzak_devtools.feedbackctl list --state open
```

Dokud vrstva neexistuje (fáze P0–P7), agent tento protokol **nespouští** a hlásí
jej jako **nedostupný** — netvrdí, že přezkum zpětné vazby proběhl.

## Logický tok §21.27 (SC-015)

```text
capture → annotate → save → queue → publish → pull → list → show
        → respond → claim → release → claim → complete → verify
```

Jeden end-to-end test projde tento tok v rozsahu, který pygame adaptér podporuje.
Kroky, které platforma neumožňuje (audio, transkripce), jsou v dokumentaci
i za běhu **výslovně označeny jako nedostupné**, nikoli tiše přeskočeny.
