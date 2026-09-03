# AGENTS.md

## Purpose

This repository may be inspected, modified, built, tested, reviewed, and maintained by automated coding agents.

These rules are intentionally project-agnostic. They apply to Codex, Claude Code, GitHub Copilot, Cursor, Windsurf, custom automation, and other coding agents unless a repository-specific instruction explicitly narrows them.

The agent must complete the requested task while protecting:

- source code and repository history;
- uncommitted user work;
- credentials and private data;
- development-environment stability;
- useful build caches and local state;
- system performance;
- unrelated processes, files, devices, and services;
- product and architectural decisions already established by authoritative project artifacts.

Repository-specific instructions may add stricter requirements. They must not silently weaken safety, integrity, privacy, or evidence requirements.

---

# 1. Instruction precedence and policy boundaries

Apply instructions in this order unless the repository explicitly defines a stricter compatible precedence model:

1. explicit instruction from the user for the current task;
2. operating-system, security, privacy, and platform constraints;
3. repository-specific governing documents and constitution;
4. repository-specific `AGENTS.md` / `CLAUDE.md`;
5. active feature specification and approved clarifications;
6. approved plan, research, contracts, data model, and task graph;
7. this generic `AGENTS.md`;
8. tool defaults and conventions.

Machine-specific policies govern their own domain. For example, a machine storage policy may override generic examples in this file about temporary, build, simulator, dependency-cache, archive, or result paths.

Tool-specific files such as `CLAUDE.md` may add stricter behavior for that tool but must not weaken higher-authority requirements.

If two applicable rules genuinely conflict:

- do not silently choose the convenient one;
- identify the conflict;
- determine whether precedence already resolves it;
- stop only the affected path if a material product, architecture, security, data, or compatibility decision remains unresolved.

---

# 2. Core operating principles

1. Understand before changing.
2. Make the smallest coherent change that fully satisfies the request.
3. Prefer reversible actions.
4. Preserve existing behavior unless change is requested.
5. Reuse established project patterns, components, scripts, and dependencies.
6. Do not modify unrelated files.
7. Do not replace working architecture without a clear requirement.
8. Prefer incremental builds and targeted tests.
9. Track every task-owned process, simulator, emulator, container, watcher, server, and temporary directory.
10. Clean up only task-owned resources.
11. Never claim success without evidence.
12. Never hide failed or unavailable validation.
13. Never delete user data, caches, repository state, or diagnostics merely to make an error disappear.
14. Never weaken security controls to make code run.
15. Do not invent product decisions merely to keep execution moving.
16. Persist durable project knowledge in repository artifacts, not only in chat history.
17. If uncertain whether an action is safe, do not perform it.

---

# 3. Required workflow

## 3.1 Before modifying anything

Before implementation:

1. Read this file and repository-specific instructions.
2. Inspect repository structure.
3. Identify applicable governing documents.
4. Read the relevant source files and active feature artifacts.
5. Check Git state.
6. Distinguish pre-existing changes from task-owned changes.
7. Identify existing conventions and reusable code.
8. Identify callers, tests, configuration, migrations, documentation, contracts, and interfaces affected by the change.
9. Determine the smallest useful validation.
10. Record the initial state of shared resources that may be changed.
11. If a developer-feedback pipeline is configured, follow its start-of-session protocol.
12. If a machine-specific storage policy applies, run its required preflight before any storage-producing operation.

Useful initial checks:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git diff --stat
```

Do not begin implementation based only on:

- filenames;
- issue titles;
- generated summaries;
- old chat recollection;
- assumptions;
- conventions from unrelated projects.

---

## 3.2 Planning the change

Before writing code, determine:

- requested outcome;
- current behavior;
- intended behavior;
- authoritative source of truth;
- smallest implementation path;
- compatibility risks;
- security/privacy implications;
- validation required;
- resource cleanup required.

Avoid:

- unrelated refactoring;
- dependency upgrades;
- repository-wide formatting;
- architecture migration;
- file reorganization;
- speculative abstractions;
- future-feature implementation not required by current scope.

Future-ready architecture is justified only when it is explicitly required or materially cheaper now than a later breaking change. It is not permission to implement future product behavior.

---

## 3.3 During implementation

While editing:

- follow existing architecture and style;
- preserve public interfaces unless change is required;
- keep changes localized;
- avoid duplication;
- do not introduce temporary hardcoded production behavior;
- do not leave commented-out implementations;
- do not disable warnings or tests to conceal problems;
- do not silently swallow errors;
- do not present placeholders as completed behavior;
- do not change governing documents merely to legitimize an accidental implementation;
- update tests and documentation when the changed behavior requires it.

If a larger problem is discovered, finish the requested safe scope where possible and report the larger issue separately.

---

## 3.4 After implementation

Before reporting completion:

1. Review the complete diff.
2. Remove task debugging code.
3. Run the narrowest meaningful validation.
4. Expand validation only when justified.
5. Check for accidental unrelated changes.
6. Confirm no secrets or prohibited machine-specific paths were committed.
7. Update task status and durable documentation where required.
8. Stop task-owned processes and perform safe cleanup.
9. Preserve useful diagnostics.
10. Report exactly what was and was not validated.

Useful checks:

```bash
git status --short
git diff --check
git diff --stat
git diff
```

---

# 4. Scope control

## 4.1 Allowed incidental changes

Allowed when directly necessary:

- affected tests;
- minimal compilation fixes;
- necessary type/interface adjustments;
- directly affected documentation;
- migration compatibility changes;
- removal of task-created temporary code;
- formatting within modified lines when required by tooling.

## 4.2 Not allowed without explicit approval or governing authority

- repository-wide formatting;
- unrelated symbol renames;
- moving unrelated files;
- framework replacement;
- package-manager changes;
- unrelated dependency upgrades;
- infrastructure migration;
- broad warning cleanup;
- speculative feature work;
- product behavior not supported by the active specification;
- public API changes unrelated to the task.

When broad change is genuinely unavoidable, explain why and keep it as limited as possible.

---

# 5. Git safety

## 5.1 Required behavior

Before modifications:

```bash
git status --short
```

Distinguish:

- pre-existing user changes;
- task changes;
- generated files;
- ignored files;
- unrelated modifications.

Never overwrite or discard changes not created by the current task.

Before completion:

```bash
git diff --check
git diff --stat
```

Review the actual diff.

## 5.2 Prohibited Git actions without explicit approval

```bash
git reset --hard
git clean -fd
git clean -fdx
git checkout -- .
git restore .
git restore --staged .
git push --force
git push --force-with-lease
git rebase --onto
git filter-branch
git filter-repo
```

Do not:

- discard uncommitted work;
- rewrite published history;
- force-push;
- amend existing commits without authorization;
- resolve conflicts by blindly choosing one side;
- delete branches or change remotes without authorization;
- modify global Git configuration.

## 5.3 Commits and pushes

Commit or push only when:

- the user explicitly requested it; or
- repository-specific instructions explicitly require it.

A commit must contain only coherent task-related work and must exclude secrets, temporary logs, local database dumps, personal IDE state, and machine-only configuration unless intentionally required.

Context hygiene never creates independent permission to commit or push.

---

# 6. Debugging policy

Debugging must be evidence-driven.

When a command or test fails:

1. capture exact command;
2. capture exit code;
3. capture relevant output;
4. reproduce safely if useful;
5. isolate the smallest failing scope;
6. form a concrete hypothesis;
7. choose the least invasive test of that hypothesis;
8. change one meaningful variable at a time;
9. rerun the original failing scenario;
10. preserve useful diagnostics;
11. clean up task-owned resources.

Default maximum retries for an unchanged failing command: one.

Further retries require a meaningful change in code, configuration, destination, environment, dependency state, command arguments, or test scope.

Do not use broad resets as the first debugging response.

Do not:

- delete caches blindly;
- reinstall all dependencies reflexively;
- erase simulators;
- delete lockfiles;
- restart the whole machine;
- kill generic process classes;
- disable security checks;
- alter expected tests to match incorrect output;
- add arbitrary sleeps to conceal races;
- add broad retries without understanding the failure.

---

# 7. Quality gates

A task is not complete merely because code was written.

Validate as applicable:

- parsing;
- compilation;
- type checking;
- affected unit tests;
- affected integration tests;
- UI/end-to-end tests;
- lint/static analysis;
- migrations;
- generated artifacts;
- no disabled unrelated tests;
- no placeholder implementation;
- no new avoidable warnings;
- explicit error handling;
- compatibility;
- affected documentation;
- original scenario re-test.

Use the narrowest validation that provides meaningful evidence.

Expand validation when shared infrastructure, public interfaces, data models, migrations, concurrency, authentication, build configuration, or multiple dependent modules changed.

If validation is unavailable:

- state exactly what was not run;
- state why;
- do not claim full verification;
- provide the command or procedure needed later.

---

# 8. Security and privacy

Never:

- commit or print secrets;
- expose private keys or tokens;
- use real secrets in examples;
- send private data to external services without authorization;
- disable authentication/authorization/TLS/integrity/sandbox/code-signing controls to make development easier;
- copy production data into tests without explicit authorization;
- scan unrelated user files when repository data is sufficient.

Use environment variables, secret managers, keychains, CI secrets, and placeholder values as appropriate.

Do not execute remote scripts blindly, including:

```bash
curl https://example.com/script.sh | sh
wget -qO- https://example.com/install.sh | bash
```

Inspect external code and prefer official sources.

---

# 9. Dependency policy

Use the repository's existing dependency manager and lockfile.

Before adding a dependency, confirm that:

- existing project/platform functionality is insufficient;
- maintenance status is acceptable;
- license is compatible;
- transitive footprint is reasonable;
- security exposure is justified.

Do not:

- upgrade unrelated dependencies;
- replace package managers;
- delete lockfiles to fix ordinary errors;
- clear global caches automatically;
- mix package managers;
- globally install packages when project-local installation is available.

---

# 10. Tool and shell policy

Prefer:

- read-only inspection before mutation;
- project-local tools;
- explicit paths and targets;
- explicit PIDs;
- bounded output;
- timeouts where commands may hang;
- deterministic commands;
- task-specific temporary directories according to the active storage policy.

Avoid:

- whole-filesystem scans;
- broad wildcard deletion;
- ambiguous working directories;
- unbounded log streams;
- global configuration changes;
- elevated privileges.

Do not use `sudo` unless system-level modification is genuinely required and the user explicitly approved it.

Before recursive deletion:

```bash
test -n "$TARGET_DIR"
test "$TARGET_DIR" != "/"
test "$TARGET_DIR" != "$HOME"
test -d "$TARGET_DIR"
```

Deletion must target a verified task-owned/project-owned path.

---

# 11. Process and resource management

Every long-running process started by the agent must be tracked.

Examples:

- builds;
- test runners;
- dev servers;
- watchers;
- bundlers;
- simulators;
- emulators;
- preview processes;
- Docker containers;
- log streams.

Terminate only known task-owned resources.

Avoid broad commands such as:

```bash
killall node
killall Simulator
pkill -f xcodebuild
pkill -f swift
pkill -f java
pkill -f python
```

unless every matching process has been verified as task-owned.

High CPU or memory usage alone is not permission to terminate a process.

Machine-specific process, simulator, and storage behavior may be governed by a dedicated machine policy.

---

# 12. Build policy

Prefer incremental builds.

Do not routinely run clean builds.

Build only the smallest necessary target, scheme, configuration, destination, package, or module.

Use isolated task/project build paths when required by repository or machine policy.

Do not erase useful global caches merely to diagnose one build.

---

# 13. Test policy

Run the narrowest test scope that proves the change.

Preferred order:

1. affected test method;
2. affected test file/class;
3. affected target/package;
4. affected module;
5. full suite;
6. broader integration/UI validation when required.

Do not enable parallel test workers by default on constrained systems.

Do not weaken assertions, skip failures, or mark flaky tests as passing merely to satisfy a gate.

---

# 14. Prohibited destructive actions

Never use the following as routine cleanup:

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/*
rm -rf ~/Library/Developer/CoreSimulator
rm -rf /Library/Developer/CoreSimulator
xcrun simctl erase all
xcrun simctl delete all
xcodebuild clean
git reset --hard
git clean -fd
git clean -fdx
rm -rf node_modules
rm -rf .git
rm -rf ~/Library/Caches/*
docker system prune -a
docker volume prune
sudo rm -rf
```

A repository- or machine-specific policy may define a safer exact project-owned path, but no policy should be interpreted as blanket permission for destructive cleanup.

---

# 15. Context hygiene and session continuity

## 15.1 Governing principle

> Persist durable knowledge in versioned project artifacts; use chat/session context as temporary working memory.

A future agent must not require access to an old conversation to reconstruct a product decision, architecture decision, active feature state, validated implementation state, or unresolved blocker needed for safe continuation.

Persist durable information in the appropriate artifact:

```text
product/game-design decision
  -> governing canon, product specification, approved clarification, decision record

project-wide engineering rule
  -> constitution, AGENTS.md, CLAUDE.md, ADR, repository policy

feature behavior
  -> spec.md

technical decision
  -> plan.md, research.md, data-model.md, contracts, ADR

executable work state
  -> tasks.md

implementation evidence
  -> tests, commits, validation artifacts, retained diagnostics

unresolved required input
  -> tracked blocker/open-input/decision document
```

Do not use chat history as hidden specification.

## 15.2 Context-cost discipline

Use the smallest useful context.

Prefer:

- targeted file reads;
- repository search;
- diffs;
- section-level references;
- fresh contexts for distinct work;
- independent review from actual artifacts.

Avoid:

- repeatedly loading every governing document;
- pasting entire accepted specifications into chat;
- restating resolved decisions;
- carrying an unrelated task into an extremely large session;
- relying on conversational memory when authoritative artifacts exist.

Correctness and traceability take priority over token savings.

## 15.3 Spec Kit phase boundaries

Major Spec Kit phases are natural checkpoints:

```text
/specify
/clarify
/plan
/tasks
/analyze
/implement
```

Default behavior after completing a major phase:

1. validate output;
2. persist durable artifacts;
3. report checkpoint;
4. STOP before automatically entering the next phase unless continuous execution was explicitly authorized.

Completion of `/plan` is not permission to run `/tasks`.
Completion of `/tasks` is not permission to run `/implement`.

## 15.4 Implementation checkpoints

For a large `/implement` run, default checkpoints are:

- Setup complete;
- Foundational complete;
- each user story complete;
- each major implementation phase complete;
- before consequential refactor/migration;
- before production/release verification.

At each checkpoint:

1. validate completed scope;
2. update task state;
3. inspect diff;
4. persist work according to Git policy;
5. report deviations, warnings, technical debt, and blockers;
6. STOP unless continuation beyond that checkpoint was explicitly authorized.

If commits are not authorized, do not commit merely for context hygiene. Report the uncommitted state and treat context clearing conservatively.

## 15.5 Pre-clear safety gate

The agent may report `CONTEXT: SAFE TO CLEAR` only after verifying, where applicable:

- all product decisions needed by future work are persisted;
- all architecture decisions needed by future work are persisted;
- active feature scope and acceptance criteria are persisted;
- task completion state is current;
- unresolved questions/blockers are durable;
- validated implementation work is committed when authorized, or explicitly documented/protected if not;
- required generated artifacts are persisted;
- useful continuation diagnostics have durable paths;
- current branch and HEAD are known;
- no implementation detail required for continuation exists only in chat;
- no task-owned process must remain alive solely because its state would otherwise be forgotten.

If any applicable condition fails, do not report `SAFE TO CLEAR`.

## 15.6 Required context status

At every major checkpoint report exactly one:

```text
CONTEXT: SAFE TO CLEAR
```

Use only when a fresh agent can safely reconstruct continuation from repository artifacts plus the handoff.

```text
CONTEXT: COMPACT RECOMMENDED
```

Use when the same task is still active and current-session reasoning remains materially useful, but context is unnecessarily large.

```text
CONTEXT: KEEP CURRENT SESSION
```

Use when unresolved work still depends on information not safely persisted.

## 15.7 `/compact` versus `/clear`

Recommend `/compact` when:

- same task continues;
- blocker investigation is active;
- unresolved reasoning remains session-local;
- context is large but reset would lose useful working state.

Recommend `/clear` or a fresh thread when:

- a major phase is safely complete;
- next task is logically distinct;
- independent review is desirable;
- repository artifacts are sufficient;
- the pre-clear gate passes.

A context reset is not a substitute for persisting project state.

## 15.8 Fresh-context bootstrap

A fresh agent continuing work must:

1. read applicable agent/tool instructions;
2. inspect branch, HEAD, and working tree;
3. read constitution when present;
4. identify active feature;
5. read only active artifacts needed for the current phase;
6. inspect task state and blockers;
7. run configured feedback-pipeline startup;
8. verify storage/machine prerequisites before generated-data operations.

Do not ask the user to repeat decisions already persisted in the repository.

## 15.9 Cross-agent handoff

Claude, Codex, Copilot, Cursor, Windsurf, or another agent must be able to continue without shared chat history.

At major handoff include:

```text
Branch:
HEAD:
Active feature:
Completed phase/checkpoint:
Authoritative artifacts:
Tasks completed:
Validation performed:
Known blockers/open decisions:
Uncommitted work:
Resources intentionally left running:
Next authorized step:
Context status:
```

The handoff supplements the repository. It must not contain unique requirements that exist nowhere else.

For architecture review, `/analyze`, security review, and final implementation audit, prefer fresh context where practical.

## 15.10 Context reset is not cleanup authorization

`/compact`, `/clear`, closing an agent, or switching agents does not authorize:

- killing unrelated processes;
- deleting temporary evidence still needed;
- deleting build/cache state;
- resetting Git;
- discarding a worktree;
- shutting down pre-existing simulators;
- deleting diagnostics.

Resource cleanup remains governed independently by repository and machine policies.

---

# 16. Developer feedback pipeline integration

The detailed developer-feedback standard must live in a single canonical standalone policy rather than being duplicated into this file.

Preferred canonical filenames include:

```text
UNIVERSAL_FEEDBACK_PIPELINE.md
feedback_pipeline_standalone.md
```

If a canonical feedback policy exists and the project has a user-facing interface:

- read it during bootstrap/adoption;
- follow its configured start-of-session protocol once the pipeline exists;
- preserve its canonical statuses, stable IDs, immutable evidence, privacy requirements, and completion evidence;
- do not reimplement divergent per-screen feedback systems;
- do not include development feedback tooling in production unless explicitly approved.

If the pipeline is not yet implemented, follow the standalone policy's adoption rules. Do not duplicate its full normative text into `AGENTS.md`.

---

# 17. Machine-specific policy integration

Machine-specific files may define stricter rules for:

- storage placement;
- simulators/emulators;
- build products;
- temporary data;
- dependency caches;
- archives/results;
- CPU/memory use.

When a machine-specific storage policy is active, its path-selection rules override generic path examples in this file.

Do not hardcode a user's machine-specific storage path into shared project source/configuration unless the governing policy explicitly requires a local-only file.

---

# 18. End-of-task cleanup

At task end:

1. terminate task-owned background processes;
2. stop task-owned servers/watchers;
3. shut down task-owned simulators/emulators when policy requires;
4. stop task-owned containers;
5. remove disposable task-owned temporary files;
6. preserve useful diagnostics;
7. leave shared caches intact;
8. leave unrelated processes untouched;
9. report anything intentionally left running.

Do not delete evidence required for a subsequent session.

---

# 19. Required final report

At the end of every development task report:

## Result

- what was implemented;
- what behavior changed;
- what remains unresolved.

## Files changed

- exact file list;
- generated files separately.

## Validation

- exact commands/checks;
- result;
- anything not run and why.

## Resources

- simulators/emulators;
- background processes started/stopped;
- containers;
- temporary files removed;
- diagnostics retained;
- resources intentionally left running.

## Risks

- compatibility risks;
- unverified paths;
- known limitations;
- follow-up work.

## Feedback pipeline

When configured and relevant:

- health/pull command;
- new/reviewed/claimed/completed/open item IDs;
- sync result;
- pipeline errors.

## Session handoff

At major Spec Kit phases or authorized implementation checkpoints:

```text
Branch:
HEAD:
Active feature:
Completed checkpoint:
Authoritative artifacts changed:
Tasks completed:
Validation performed:
Open blockers/decisions:
Uncommitted work:
Resources intentionally left running:
Next authorized step:
Context: SAFE TO CLEAR / COMPACT RECOMMENDED / KEEP CURRENT SESSION
```

---

# 20. Default decision rule

When uncertain whether an action is safe:

**Do not perform it.**

Report:

- evidence;
- affected resource;
- proposed action;
- risk;
- safer alternative.
