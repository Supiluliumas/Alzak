# UNIVERSAL_DEVELOPER_FEEDBACK_PIPELINE.md

## Status

This is the canonical universal policy for the developer feedback pipeline.

Do not duplicate its full normative contents into `AGENTS.md`, `CLAUDE.md`, or per-screen implementation instructions. Those files should reference this policy and contain only integration-specific rules.

---

# 21. Universal developer feedback pipeline

## 21.1 Purpose and mandatory scope

Every project with a user-facing interface must provide a developer feedback pipeline in development and explicitly designated test builds.

The pipeline must allow a developer or tester to:

1. open the tool from any visible application surface;
2. capture current application UI;
3. mark exact affected location/element;
4. record spoken explanation;
5. transcribe to editable text;
6. classify intent;
7. save/transfer canonical feedback package;
8. expose it to coding agents at session start;
9. track work status;
10. preserve implementation/verification evidence.

Applicable platforms include web, iOS/iPadOS, macOS, Android, Windows, Linux, games, embedded GUIs, internal tools, and administration panels.

Non-GUI projects should provide an equivalent development feedback surface when feedback capture is relevant.

The subsystem should be reusable and root-integrated, not independently reimplemented on every screen.

---

## 21.2 Release isolation

The feedback pipeline is development/test tooling.

It must not be included in a production release unless the user explicitly requests a production feedback feature and that feature receives separate security/privacy design.

Preferred isolation is structural/build-time exclusion where the platform/build graph reasonably supports it.

A development flag such as:

```text
DEVELOPER_FEEDBACK_ENABLED
```

may still control development behavior, but a runtime flag alone is not proof that development-only code is absent from production.

Production exclusion must be explicit, testable, and documented.

Hidden gestures or undocumented environment state are not adequate isolation.

---

## 21.3 Universal floating feedback control

Every active user-facing surface should expose a root-level feedback control in eligible development/test builds.

Mount at highest appropriate app shell/window/scene/portal/overlay layer so new screens inherit it automatically.

For multi-window apps, each active app window must have correctly scoped access.

The control should:

- remain above normal content;
- respect safe areas/system bars/keyboards;
- avoid critical controls;
- be draggable/snap safely where appropriate;
- have accessible labels and input equivalents;
- avoid intercepting gestures outside bounds;
- support localization;
- remain visually distinct from production UI.

A deterministic restore path is required if minimized.

### Capture exclusion

The control and editor must not appear in captured application screenshots unless explicitly requested.

Exclusion must be verified against the actual capture artifact, not inferred solely from view/window architecture.

Avoid arbitrary long delays.

---

## 21.4 Capture behavior

Capture the current application surface as the developer sees it, preferring the active application window/rendered surface over the entire desktop.

Do not capture unrelated applications, notifications, password managers, or private desktop content by default.

Preserve when available:

- pixel dimensions;
- display scale;
- orientation;
- viewport/window size;
- color appearance;
- safe-area information;
- route/screen/window/scene identifier.

Preserve both:

1. original unmodified capture;
2. annotated image.

Do not destructively replace original.

If direct capture is unavailable:

- use supported app-surface capture;
- attach render/document/component context where useful;
- allow text/audio-only continuation;
- explicitly mark screenshot unavailable.

Never silently save blank/stale image.

---

## 21.5 Annotation editor

Minimum annotation tool: freehand pencil.

Where practical support:

- eraser;
- undo/redo;
- clear;
- arrow;
- rectangle/ellipse;
- highlight;
- color/stroke width;
- crop/zoom;
- element identification;
- multiple marked regions.

Store structured annotation layer in addition to flattened annotated image.

Normalize coordinates relative to capture.

Where available, supplement with semantic target data:

- accessibility identifier;
- selector/component/view identifier;
- route/hierarchy;
- normalized bounding rectangle;
- privacy-filtered visible text;
- component type.

Visual marking remains authoritative user evidence.

---

## 21.6 Voice recording and transcription

Provide:

- explicit record start/stop;
- recording indicator;
- elapsed time;
- microphone permission handling;
- cancel;
- playback/re-record when practical;
- text fallback.

### Transcription

Preference order:

1. on-device/OS transcription;
2. approved local engine;
3. explicitly approved external service.

Never send audio/transcript externally without approved policy.

If a project requires on-device-only transcription, unsupported device/locale must degrade to "transcription unavailable", not network fallback.

Transcript remains editable.

### Audio retention

Preserve original audio through successful package write, integrity verification, and canonical transfer.

If no retention policy exists, preserve audio with package because transcript may be imperfect.

---

## 21.7 Feedback type and intent

Canonical types:

```text
bug
change
enhancement
polish
performance
accessibility
security
data
question
other
```

Automatic classification is advisory.

Optional fields:

- severity;
- priority;
- expected behavior;
- observed behavior;
- reproduction steps;
- acceptance criteria;
- platform;
- user role;
- related feedback ID.

Minimum meaningful human content:

- non-empty typed/transcribed description; or
- visual annotation with sufficient context.

Do not accept accidental empty feedback silently.

---

## 21.8 Stable ID and context package

Generate globally stable ID at capture time:

```text
FB-<UTC_DATE>-<RANDOM_OR_UUID>
```

ID must remain unchanged across queue, transfer, normalization, responses, status, resolution, archive, reopen.

Required metadata where available:

- ID;
- UTC timestamp/local timezone;
- type/status;
- app/version/build/configuration;
- branch/commit/dirty indicator;
- platform/OS/device;
- simulator/emulator/physical indicator;
- route/screen/scene;
- viewport/scale/orientation;
- locale/theme;
- relevant accessibility settings;
- feature flags;
- semantic target;
- attachment manifest;
- checksums;
- schema version.

Optional bounded privacy-filtered diagnostics may include recent errors, relevant logs, failed requests, state-machine state, non-sensitive feature state, performance, component hierarchy, console messages, correlation IDs.

Never collect secrets, auth tokens, passwords, private keys, payment data, or unrelated personal data.

Redact secure fields when platform supports it.

---

## 21.9 Canonical package

Logical structure:

```text
feedback-store/
├── inbox/
│   └── <ID>/
│       ├── feedback.md
│       ├── context.json
│       ├── screenshot-original.png
│       ├── screenshot-annotated.png
│       ├── annotations.json
│       ├── audio-original.m4a
│       ├── transcript.txt
│       ├── agent-response.md
│       ├── resolution.json
│       └── checksums.json
├── archive/
└── quarantine/
```

Exact physical layout may differ while preserving logical information.

Immutable capture evidence includes:

- original screenshot;
- original audio;
- original produced transcript;
- original developer-edited description;
- original capture context;
- timestamp;
- stable ID.

Responses/status/resolution/verification are mutable additions.

Never rewrite original evidence to make final implementation appear correct.

---

## 21.10 Storage location

Attachments follow active machine storage policy.

On the configured MacBook, canonical store should resolve under external development storage, for example:

```text
$DEV_STORAGE_ROOT/Feedback/<project-name>-<project-hash>/
```

Do not commit large binary feedback attachments by default.

Do not hardcode one user's volume path into shared source; resolve through local policy/environment.

---

## 21.11 Local-first queue and reliable transfer

Feedback must remain usable offline.

Device-local durable queue must support:

```text
capturing
queued
transferring
synced
transfer_failed
```

Transport state is separate from agent work status.

Required capabilities:

- pending items;
- retry;
- integrity verification;
- duplicate detection;
- partial-transfer recovery;
- bounded-storage warning;
- deletion only after confirmed synchronization.

An item is synchronized only after all required files arrive, checksums match, canonical directory publication succeeds atomically, and stable ID is acknowledged.

Deduplicate primarily by stable ID.

Repeated pulls must not create duplicates.

---

## 21.12 Cross-platform adapters

Architecture should separate canonical core from platform adapters.

Conceptual interfaces:

```text
FeedbackOverlayAdapter
FeedbackCaptureAdapter
FeedbackAnnotationAdapter
FeedbackAudioAdapter
FeedbackTranscriptionAdapter
FeedbackContextProvider
FeedbackPrivacyRedactor
FeedbackLocalStore
FeedbackTransportAdapter
FeedbackStatusSyncAdapter
```

Core owns model/status/package validation/checksums/dedup/agent workflow/storage contract/privacy.

Platform adapter owns overlay, capture, microphone, transcription invocation, context extraction, transfer.

Use supported platform mechanisms; do not bypass platform security.

---

## 21.13 Agent-facing CLI

Every integration must expose deterministic equivalent operations, conceptually:

```text
feedbackctl doctor
feedbackctl pull
feedbackctl list
feedbackctl show <ID>
feedbackctl respond <ID>
feedbackctl claim <ID>
feedbackctl release <ID>
feedbackctl complete <ID>
feedbackctl reopen <ID>
feedbackctl sync-status
feedbackctl verify
```

Expectations:

- `doctor`: store, transport, schema, write access, devices, transfer errors;
- `pull`: retrieve/validate/normalize/deduplicate without overwriting immutable evidence;
- `list`: open items first with filters;
- `show`: note, transcript, attachments, context, response, history;
- `respond`: append analysis/proposal/question without automatic status change;
- `claim`: atomic `open -> in_progress` with lease metadata;
- `release`: unresolved `in_progress -> open`, preserve notes;
- `complete`: `done` only with evidence;
- `reopen`: preserve prior resolution history;
- `sync-status`: expose status/response back to developer surface;
- `verify`: package/status/checksum/stale-claim validation.

---

## 21.14 Canonical work status

Use exactly:

```text
open
in_progress
done
```

UI labels may localize.

### open

No active claim. May already contain response/proposal.

### in_progress

Use only for actively addressed item.

Record agent/session/branch/start/lease/current plan/files when known.

It is a temporary lease.

If work stops without immediate continuation, release to `open` unless an explicit documented takeover occurs.

### done

Only after:

- implementation/final answer completed;
- relevant validation passed;
- concrete files/artifacts linked;
- original scenario rechecked where possible;
- visual/device verification completed when relevant.

Code written alone is insufficient.

No hidden terminal states. Duplicate/rejected/obsolete outcomes must be represented explicitly with preserved history.

---

## 21.15 Concurrent-agent claims

Claims must be atomic.

Claim record includes lease expiry and optional heartbeat.

For stale claim:

1. verify original agent/process;
2. preserve work notes;
3. explicitly release/take over;
4. record takeover.

Never overwrite another agent's response/evidence.

---

## 21.16 Mandatory start-of-session protocol

Before modifying code in a configured project:

1. read repository and feedback instructions;
2. verify feedback store and required storage;
3. run health check;
4. pull configured sources/devices;
5. validate/deduplicate;
6. list new/open/stale in-progress;
7. read every newly received item;
8. inspect relevant code before declaring solved;
9. append substantive response to every new item;
10. identify current-task items;
11. claim only items actually being addressed;
12. leave others open.

Do not ask whether feedback should be pulled when pipeline is configured.

If unavailable, report failure before claiming session review complete.

---

## 21.17 Required response to each new note

Response must contain at least one:

- implementation proposal;
- root cause;
- request for specific missing fact;
- documented conflict;
- reasoned disagreement;
- evidence issue already appears resolved;
- grouping under shared root cause.

Do not respond only with:

```text
noted
acknowledged
will check
```

Reference stable ID.

---

## 21.18 Evidence-based review findings

Use findings distinct from canonical work status:

```text
verified_in_code
needs_runtime_confirmation
open
insufficient_information
```

Never write "fixed" without evidence.

---

## 21.19 Claimed-item implementation protocol

For each claimed item:

1. inspect original evidence/context;
2. reproduce where possible;
3. identify source of truth;
4. check documented decisions;
5. inspect related surfaces;
6. define smallest coherent change;
7. write/update tests;
8. implement;
9. run targeted validation;
10. perform visual/device validation when relevant;
11. attach evidence;
12. mark done only when completion criteria pass;
13. sync result back.

Marked screenshot identifies observed location, not necessarily complete fix scope.

---

## 21.20 Completion evidence

Recommended resolution record:

```json
{
  "feedback_id": "FB-20260802-7F3A91C2",
  "status": "done",
  "completed_at": "2026-08-02T14:35:00Z",
  "agent": "<agent-or-session>",
  "branch": "<branch>",
  "commit": "<commit-if-created>",
  "files_changed": ["<path>"],
  "tests": [{"command": "<exact-command>", "result": "passed"}],
  "runtime_verification": "<what-was-verified>",
  "remaining_risks": [],
  "resolution_summary": "<concise-result>"
}
```

For UI feedback include after screenshot, visual comparison, simulator/emulator result, physical-device verification, or explicit user confirmation.

Compilation alone is not sufficient visual evidence.

---

## 21.21 Status synchronization

Where supported, originating device/dashboard should display:

- ID;
- status;
- agent response;
- implementation summary;
- verification;
- completion time;
- reopen action.

Distinguish not reviewed / reviewed-open / active / completed / reopened.

Do not represent response/proposal as implementation progress.

---

## 21.22 Reopening and regression

Reopen when issue persists, is partial, regresses, runtime contradicts code, or acceptance criteria were misunderstood.

Preserve previous resolution and history.

Confirmed recurrence after prior fix should link prior commit and be treated as regression.

---

## 21.23 Privacy and security

Required protections:

- development/test isolation;
- microphone permission;
- visible recording indicator;
- secure-field redaction;
- bounded diagnostics;
- secret/token filtering;
- authenticated encrypted remote transport;
- integrity checks;
- no unrelated-app capture by default;
- no automatic external AI upload;
- configurable retention;
- explicit deletion;
- audit history.

Never weaken app auth/sandbox/transport security.

Never capture production credentials.

---

## 21.24 Performance

Idle subsystem should:

- avoid continuous screen/audio capture;
- avoid aggressive polling;
- avoid unnecessary semantic-tree rebuilds;
- keep memory bounded;
- lazy-load heavy editor/transcription;
- release capture/audio resources;
- stop transfer activity when complete;
- keep floating control lightweight.

Large artifacts follow storage policy.

---

## 21.25 Reliability

Tolerate:

- app interruption;
- device disconnect;
- transfer interruption;
- repeated pulls;
- partial files;
- transcription failure;
- capture restriction;
- multi-window;
- app restart;
- agent interruption;
- concurrent agents;
- schema upgrades.

Use versioned schemas/migrations.

Unknown future fields must not cause wholesale discard.

Corrupted/incomplete items go to quarantine with explicit error.

---

## 21.26 Coverage of all screens

Root-level coverage must be testable.

Possible validation:

- route enumeration;
- window/scene lifecycle tests;
- UI tests across registered screens;
- development runtime assertion;
- health check for surfaces lacking overlay;
- modal/full-screen integration test.

Dedicated feedback integration check must fail when an eligible active surface lacks access.

Do not rely solely on manual inspection.

---

## 21.27 End-to-end acceptance

Integration is not complete until logical flow succeeds:

1. launch eligible development build;
2. navigate representative screen;
3. confirm control;
4. verify modal/secondary-window access where applicable;
5. capture;
6. verify control excluded from actual screenshot artifact;
7. annotate;
8. record voice;
9. transcribe/edit or use documented fallback;
10. submit through local queue/offline path;
11. transfer;
12. pull canonical item;
13. verify checksums/stable ID;
14. pull again and verify no duplicate;
15. agent reads package;
16. append response without status change;
17. claim -> in_progress;
18. release -> open;
19. claim again and attach implementation evidence;
20. complete -> done;
21. sync status to developer surface;
22. reopen and verify preserved history.

Every supported adapter must pass same logical acceptance flow.

---

## 21.28 Repository integration

Each repository documents only project-specific adapter details:

- enablement/build exclusion;
- root integration point;
- CLI path;
- feedback store identifier;
- transfer method;
- source/tests;
- platforms;
- transcription provider/policy;
- retention;
- production exclusion mechanism.

Do not redefine canonical statuses, stable IDs, immutable evidence, or startup workflow.

---

## 21.29 Prohibitions

Never:

- remove control to simplify layout;
- disable pipeline because it complicates testing;
- include development tool in production accidentally;
- mark done without evidence;
- overwrite original transcript/screenshot;
- delete unresolved notes;
- create duplicates during pull;
- ignore new notes;
- claim items not actively addressed;
- leave stale claims after abandoned work;
- externally upload captures/audio/context without approval;
- store large attachments on prohibited storage;
- expose secrets through captures;
- claim pipeline operational without end-to-end evidence.

---

## 21.30 Bootstrap/adoption

The pipeline is standard development foundation for user-facing projects.

Establish before or alongside first navigable shell when the project adopts this universal standard.

Bootstrap includes:

- development/test enablement;
- root control;
- one platform adapter;
- canonical package;
- local durable queue;
- store configuration;
- agent pull/status interface;
- production-exclusion test;
- one end-to-end pipeline test.

For existing projects lacking it:

1. report missing universal requirement;
2. inspect UI/build architecture;
3. propose smallest root-level integration;
4. avoid scattered one-off buttons;
5. implement adapter when current task includes adoption;
6. verify coverage.

Prefer shared versioned core plus thin adapters.

---

## 21.31 Developer dashboard

Canonical store should have local dashboard/equivalent inspection UI supporting:

- filtering;
- original/annotated captures;
- marked-region inspection;
- audio/transcript;
- immutable context;
- responses/history;
- linked files/tests/branch/commit;
- reopen;
- transfer/integrity errors;
- quarantine.

Local-first; cloud not required for basic operation.

Keep transport state, work status, review finding, and verification state distinct.

---

## 21.32 Required feedback summary in final report

When feedback was reviewed/implemented:

```text
Feedback pipeline:
- Pull/health-check command:
- New items received:
- Items reviewed:
- Agent responses added:
- Items claimed:
- Items completed:
- Items returned to open:
- Items still open:
- Status synchronization:
- Pipeline errors/unavailable sources:
```

List stable IDs for claimed/completed items.

---

## 21.33 Session handoff and context continuity

The feedback store is durable development memory across `/compact`, `/clear`, fresh threads, and agent switches.

Chat history must not be required to determine:

- feedback inventory;
- status/claims;
- prior responses;
- verification evidence;
- linked branch/commit;
- remaining open work.

Before context clear/handoff:

1. persist changed responses/status;
2. ensure claims accurately represent continuing work;
3. release abandoned claims or explicitly transfer them;
4. persist obtained implementation evidence;
5. preserve immutable evidence/history;
6. record blockers needed by next session;
7. include relevant feedback IDs in session handoff.

A context reset must not orphan an `in_progress` item.

An active item at session end must be either:

- intentionally continuing and identified in handoff;
- explicitly transferred/taken over;
- released to `open` with notes preserved.

At fresh session, reconstruct from canonical feedback store, not old chat memory.

`CONTEXT: SAFE TO CLEAR` is allowed only when feedback state changes are persisted, claims are intentional/documented, and no required interpretation exists only in chat.
