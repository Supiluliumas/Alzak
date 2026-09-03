# CLAUDE.md

## Purpose

Claude Code-specific operating rules for this repository.

Claude MUST read and obey the applicable `AGENTS.md` first. This file adds Claude-specific session and Spec Kit behavior. It does not weaken constitution, repository governance, security, privacy, Git, storage, feedback, or validation requirements.

---

# 1. Core rule

> The repository is durable project memory. Claude's conversation is temporary working memory.

Do not depend on an ever-growing conversation when relevant state can be reconstructed from repository artifacts.

Do not use old chat history as hidden specification.

---

# 2. Start of every Claude coding session

Before modifying code:

1. read `AGENTS.md` and repository-specific instructions;
2. inspect `git status --short`, branch, and HEAD;
3. read `.specify/memory/constitution.md` when present;
4. identify active feature;
5. read only artifacts required for current phase;
6. inspect task state and blockers;
7. run configured feedback-pipeline start-of-session protocol;
8. verify storage/machine prerequisites before build/test/simulator/dependency/generated-data work.

When continuing from another session or another agent, reconstruct state from repository before asking user to repeat prior decisions.

---

# 3. Spec Kit phase discipline

Treat these as major phase boundaries:

```text
/speckit-specify
/speckit-clarify
/speckit-plan
/speckit-tasks
/speckit-analyze
/speckit-implement
```

After a major phase:

1. validate output;
2. persist durable state;
3. provide checkpoint report;
4. STOP before next major phase unless continuous execution was explicitly authorized.

`/speckit-plan` does not authorize `/speckit-tasks`.

`/speckit-tasks` does not authorize `/speckit-implement`.

Completion of one implementation phase does not authorize all remaining phases by default.

---

# 4. Large implementation runs

Default `/speckit-implement` stop points:

- Setup;
- Foundational;
- each User Story;
- each major phase;
- before consequential refactor/migration;
- before production/release validation.

At checkpoint:

- run relevant validation;
- update tasks;
- inspect diff;
- commit/push only when authorized by repo/user rules;
- report deviations, warnings, debt, blockers;
- stop unless next checkpoint was explicitly authorized.

If user explicitly authorizes continuous whole-feature implementation, continue through mechanical boundaries but still persist logical checkpoints and stop for unresolved material decisions.

---

# 5. Context safety gate

Before recommending `/clear` or fresh thread, verify:

- required product decisions persisted;
- architecture decisions persisted;
- active spec/plan/tasks current;
- blockers/open questions recorded;
- validated work committed when authorized, or uncommitted state explicitly documented/protected;
- branch and HEAD known;
- required diagnostics durable;
- no continuation-critical detail exists only in current conversation;
- feedback status/claims persisted;
- next agent can reconstruct work from repository plus handoff.

If any condition fails, do not recommend `/clear`.

---

# 6. `/compact`

Recommend `/compact` when:

- same task continues;
- current reasoning materially matters;
- unresolved details are not yet persisted;
- context is large but reset risks losing working state.

After compaction, re-anchor on repository artifacts.

---

# 7. `/clear` / fresh thread

Recommend only when:

- major phase safely complete;
- task/feature changes;
- independent review benefits from clean context;
- repository artifacts are sufficient;
- context safety gate passes.

Fresh context is preferred over carrying a >150k-token session into logically new work.

---

# 8. Required context marker

At each major checkpoint output exactly one:

```text
CONTEXT: SAFE TO CLEAR
```

```text
CONTEXT: COMPACT RECOMMENDED
```

```text
CONTEXT: KEEP CURRENT SESSION
```

`SAFE TO CLEAR` is a factual assertion and requires the safety gate.

---

# 9. Mandatory handoff

At major phase boundary include:

```text
Session handoff:
- Branch:
- HEAD:
- Active feature:
- Completed phase/checkpoint:
- Governing/feature artifacts changed:
- Tasks completed:
- Validation performed:
- Known blockers/open decisions:
- Uncommitted work:
- Feedback items/claims relevant to continuation:
- Resources intentionally left running:
- Next authorized step:
- Context: SAFE TO CLEAR / COMPACT RECOMMENDED / KEEP CURRENT SESSION
```

Do not place unique product requirements only in the handoff. Persist them first.

---

# 10. Reading discipline

To reduce context inflation:

- use targeted reads/search;
- read referenced sections before historical documents;
- do not paste large governing docs into chat;
- do not repeatedly summarize accepted decisions;
- do not reopen resolved questions without new evidence;
- do not read every previous feature when only active one is relevant;
- use Git history/diffs for change context.

Correctness has priority over token savings.

---

# 11. Independent review

For `/speckit-analyze`, architecture/security review, or final implementation audit, prefer a fresh context where practical.

Review governing docs, active artifacts, actual diff/code, tests, and validation evidence.

Do not rely primarily on implementer's conversational narrative.

---

# 12. Product and architecture decisions

Claude MUST NOT invent material product/architecture decisions just to continue.

If a genuine gap appears:

1. stop only affected path;
2. identify governing artifact missing the decision;
3. explain concrete consequences;
4. ask user only when choice materially affects product behavior, scope, compatibility, security, data, cost, or acceptance criteria;
5. persist approved decision upstream;
6. reconcile downstream artifacts;
7. resume.

Do not edit upstream spec merely to justify accidental implementation.

---

# 13. Git and context safety

Never use `/clear` as reason for unauthorized commit.

If commits are not authorized and validated work is uncommitted:

- preserve working tree;
- report exact state;
- default to `KEEP CURRENT SESSION` unless user explicitly accepts fresh-session handoff over that worktree;
- never reset/stash/discard merely to make context safe.

---

# 14. Feedback continuity

When feedback pipeline is configured:

- health-check/pull at coding-session start according to canonical policy;
- persist responses/status/evidence before handoff;
- do not orphan `in_progress` claims;
- release or transfer claims when work will not continue;
- include relevant stable IDs in handoff.

Fresh session reconstructs feedback state from canonical store.

---

# 15. Resource cleanup is separate

`/compact`, `/clear`, closing Claude, or switching agents does not authorize cleanup.

Follow `AGENTS.md`, Mac cleanup policy, and storage policy for processes, simulators, caches, temporary data, diagnostics, containers, and external storage.

A session may be `SAFE TO CLEAR` while reusable resources remain intentionally present, if documented and safe.

---

# 16. Final principle

> Once a decision or validated state matters beyond the current conversation, persist it in the repository.

Use Claude context for active reasoning, not as the project's only memory.
