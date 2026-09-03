# Kontrakt: balíček zpětné vazby (US6)

> **VYŘAZENO OD-007 (2026-09-03).** Tento soubor je pouze historický návrh,
> není součástí aktivní specifikace a nesmí být implementován.

**Vazba**: FR-066…FR-080, FR-088 · SC-014…SC-016, SC-022 ·
`feedback_pipeline_standalone.md` §21.2, §21.4, §21.8, §21.9, §21.11, §21.25, §21.28
**Rozsah**: OD-001 varianta V2 — bootstrap minimum, každá položka v nejmenším
vyhovujícím rozsahu.

> **§21.28**: kanonické prvky se zde **nepředefinovávají**. Tento kontrakt je
> pouze projektovým zápisem toho, co politika už určuje.

## Umístění

```text
feedback-store/            # repo-local, gitignored (A-014)
├── .staging/<ID>/         # rozepsaná položka; nikdy se nečte jako platná
├── inbox/<ID>/            # publikované položky
├── archive/<ID>/          # uzavřené (done) položky
└── quarantine/<ID>/       # poškozené nebo neúplné, VŽDY s výslovnou chybou
```

## Stabilní ID (FR-074, §21.8)

```text
FB-<YYYYMMDD>-<12 hex>        např. FB-20260903-9f2c41ab77de
      ▲ UTC datum vzniku       ▲ uuid4().hex[:12]
```

Vzniká **jednou** ve stavu `capturing` a nemění se napříč frontou, přenosem,
normalizací, odpověďmi, stavem, uzavřením ani znovuotevřením.

## Obsah `inbox/<ID>/`

| Soubor | Povinný | Popis |
|--------|---------|-------|
| `item.json` | ano | stav, popis, kontext, odpovědi, historie |
| `manifest.json` | ano | seznam příloh + `schema_version` |
| `checksums.json` | ano | SHA-256 každé přílohy (FR-075) |
| `screenshot_original.png` | ne¹ | **neupravený** snímek (FR-070) |
| `screenshot_annotated.png` | ne¹ | zploštělý snímek s anotací (FR-070) |
| `annotations.json` | ne¹ | strukturovaná vrstva, normalizované souřadnice (FR-071) |

¹ Chybí-li, `item.json` to musí **výslovně** označit (`"screenshot": "unavailable"`),
nikdy prázdným souborem ani tichým vynecháním.

### `item.json`

```json
{
  "schema_version": 1,
  "id": "FB-20260903-9f2c41ab77de",
  "type": "bug",
  "work_state": "open",
  "transfer_state": "synced",
  "description": "Laser prochází skrz levý sloup ve skladu.",
  "audio": "unavailable",
  "transcription": "unavailable",
  "screenshot": "captured",
  "context": {
    "utc": "2026-09-03T14:22:07Z",
    "game_version": "0.4.0",
    "build_kind": "source",
    "git_branch": "001-alzak-platformer-demo",
    "git_commit": "70f19a5",
    "platform": "Darwin",
    "os_version": "25.5.0",
    "level_id": "sklad",
    "level_order": 2,
    "logical_resolution": [1920, 1080],
    "window_size": [1280, 720],
    "scale": 0.6666666666666666,
    "attachments": ["screenshot_original.png", "screenshot_annotated.png", "annotations.json"],
    "schema_version": 1
  },
  "responses": [],
  "resolution": null,
  "history": [
    { "utc": "2026-09-03T14:22:07Z", "from": null, "to": "open", "by": "capture" }
  ]
}
```

### `annotations.json` (FR-071)

```json
{
  "schema_version": 1,
  "strokes": [
    { "tool": "pencil", "points": [[0.412, 0.633], [0.418, 0.640], [0.430, 0.651]] }
  ]
}
```

Souřadnice jsou **normalizované na 0–1** vůči logickému prostoru 1920 × 1080,
takže anotace přežije jakoukoli změnu měřítka okna.

## Snímek bez ovládacího prvku (FR-069, research R10)

Snímek vzniká z **kopie logického surface pořízené před kresbou overlay**.
Ověření je **proti skutečnému souboru**, ne architektonickou úvahou: E2E test
umístí do známé pozice marker barvy indikátoru, pořídí snímek a ověří, že
v uloženém PNG marker není.

## Platformní degradace (FR-072, §21.4, §21.6, A-013)

pygame nemá nahrávání zvuku ani OS transkripci. Pole `audio` a `transcription`
jsou proto **vždy** `"unavailable"` — výslovně, viditelně v nástroji, nikdy tiše.
**Síťový fallback je zakázán.** Žádná data neopouštějí zařízení.

## Prázdná zpětná vazba (FR-073)

Odeslání je odmítnuto, není-li splněno alespoň jedno: neprázdný popis, nebo
alespoň jeden tah v `annotations.json`. Nástroj řekne **proč**; tiché přijetí je
zakázáno.

## Atomická publikace (FR-077, §21.9, §21.11)

```text
1. zapiš vše do feedback-store/.staging/<ID>/
2. spočítej a zapiš checksums.json
3. os.replace(".staging/<ID>", "inbox/<ID>")     # atomické na témže svazku
```

Přerušení procesu uprostřed zanechá adresář ve `.staging/`. `feedbackctl doctor`
jej přesune do `quarantine/` s výslovnou chybou — **nikdy** tiše do `inbox/`.

## Fronta a deduplikace (FR-078, SC-016)

Stavy přenosu: `capturing` → `queued` → `transferring` → `synced`,
při selhání `transfer_failed` (odtud zpět na `queued`).

`pull` je **idempotentní**: existující `inbox/<ID>` se nepřepisuje a
`screenshot_original.png` ani `annotations.json` se po publikaci nikdy nemění.
Dvojí `pull` téže položky nesmí změnit **jediný bajt** důkazního materiálu.

## Pracovní stav (FR-080, §21.14, §21.20, §21.25)

```text
open ──claim──> in_progress ──complete(+evidence)──> done
     <─release──            <──────reopen────────────
```

Povoleny jsou **výhradně** hodnoty `open`, `in_progress`, `done`.
`done` jen s doloženým důkazem v `resolution.evidence`. `history[]` je
append-only a nikdy se nepřepisuje. **Skryté koncové stavy jsou zakázány.**

## Zakázaný obsah (FR-076, §21.8, §21.23)

Tajemství, tokeny, hesla, klíče, nesouvisející osobní data a obsah jiných
aplikací se **nesbírají**. Snímkuje se pouze herní plocha, nikdy obrazovka OS.

## Produkční vyloučení (FR-066, SC-014, research R9)

Kód žije v top-level balíčku `alzak_devtools/` mimo `src/alzak/`.
`packaging/alzak.spec` jej uvádí v `excludes`. Napojení na hru je jediný
`try: from alzak_devtools… except ImportError: None`.
Test ověří, že v produkčním prostředí je `importlib.util.find_spec("alzak_devtools")`
`None` a že `alzak.spec` balíček skutečně vylučuje.
