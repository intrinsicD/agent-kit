# Current Task

## Title

Refactor distribution boundary and add results-audit skill

## Task ID

004

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: reviewer

## Mode

Implement

## Goal

Replace the unsafe tracked-tree installation path with a fixed, auditable clean
payload that initializes blank workflow state without overwriting target files,
and add one optional generic results-audit skill distilled from three
independent repository implementations.

## Motivation

Task 003 independently confirmed that the documented `git archive HEAD`
installer collides with existing repositories and copies agent-kit's own state,
tasks, audits, tests, and ARA history. The same accepted assessment found a
recurring, repository-independent results-audit core that is absent from the
generic skill set.

## Success Criteria

- A fixed manifest names every installable source and destination path; the
  installer copies only that allowlist and never exports the tracked tree.
- Operational state and documentation indexes installed into a fresh target
  are blank project templates, not copies of agent-kit's current state or
  history.
- The payload excludes source ARA records, audits, completed tasks, dated
  sessions, regression tests, and the source repository README.
- The installer detects and reports every exact destination or blocking
  ancestor collision before writing anything, exits nonzero, and offers no
  overwrite mode.
- Disposable Git-repository tests prove the fresh install contains exactly the
  declared payload, passes its installed validator, preserves target Git
  metadata, and leaves a collision target unchanged.
- An optional `results-audit` skill requires a claim inventory, raw
  recomputation, source/config binding, controls and accounting checks,
  evidence-scope classification, and explicit claim dispositions without
  importing repository-specific rules.
- `AGENTS.md`, user documentation, skill validation, focused regressions, the
  full regression suite, and live validation agree on the new installation and
  routing behavior.
- An independent Reviewer returns a terminal verdict.

## Constraints

- Use only the Python standard library and a fixed payload definition.
- Treat every existing target path or symlink as protected; never merge,
  replace, or delete target content.
- Keep blank templates separate from agent-kit's live operational state.
- Preserve the target repository's `.git` metadata and unrelated files.
- Implement and test only inside agent-kit or disposable temporary
  repositories.

## Non-Goals

- No installation into Prospect, StructSplat, realtime-gs, or IntrinsicEngine.
- No target-specific authority adapters, skill renaming, CI integration, or
  coordination pilots.
- No configurable plugin/template platform, overwrite/update/uninstall mode,
  or speculative distribution abstraction.
- No P2 maturity vocabulary, periodic audit, or micro-task profile.
- No domain-specific rate, renderer, viewer, checkpoint, or experiment rules
  in the generic results-audit skill.

## Selected Skills

- task-orchestration
- implementation
- code-audit
- handoff

## Current Evidence

- Task 003 and
  `docs/research/cross-repository-agent-workflow-adoption.md` were independently
  Accepted.
- The current README still documents a tracked-tree archive extraction that
  copies repository history and can overwrite target files.
- Prospect, StructSplat, and realtime-gs independently converge on claim
  inventory, raw recomputation, exact provenance, controls/accounting, bounded
  evidence scope, and explicit dispositions.
- The current workflow has 10 routed skills, 31 regression tests, and three
  validated task archives.

## Minimal Plan

1. Commit this task setup on a dedicated branch.
2. Add fixed payload/template files and a narrow preflight-then-copy installer.
3. Add disposable fresh-install, collision/no-write, payload-boundary, and Git
   metadata regressions.
4. Add the optional generic results-audit skill and update routing and user
   documentation.
5. Run focused and full validation, self-audit the boundary and scope, commit
   the implementation, and hand the fixed commit to the Reviewer.

## Status

In review

## Human Decisions

None.

## Handoff Log

Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`.

### Handoff

#### Objective

Independently falsify the Task 004 implementation at commit
`92148b4c19b84614301c03ff77b736de54cb65d7`: replace tracked-tree extraction
with a fixed clean distribution boundary and add the optional generic
`results-audit` procedure without expanding into target-specific or
configurable infrastructure.

#### Changes

- Added a 22-file source/destination manifest containing the reusable
  authority, all 11 skills, the validator, four separate blank state templates,
  and five blank documentation indexes.
- Added a standard-library installer that validates manifest paths and source
  ownership, reports the complete set of exact and blocking-ancestor
  collisions before writes, uses exclusive destination creation, and rolls
  back only paths it created after a copy failure.
- Replaced the tracked-tree installation instructions and obsolete archive
  regression. The installed validator no longer requires the deliberately
  excluded source README.
- Added six disposable distribution regressions covering the exact boundary,
  fresh blank installation, installed validation, Git metadata preservation,
  complete exact/ancestor collision reporting with no writes, nonexistent
  targets, and injected-failure rollback.
- Added and routed `results-audit`, including exact claim inventory, raw
  recomputation, source/config binding, chronology and controls, accounting,
  evidence boundaries, and explicit dispositions while keeping domain rules
  local.
- Recorded the Driver code audit in
  `docs/audits/distribution-installer.md`.

#### Evidence

- Implementation commit:
  `92148b4c19b84614301c03ff77b736de54cb65d7`.
- All Python checks used `PYTHONDONTWRITEBYTECODE=1`.
- `python3 scripts/validate_agent_workflow.py` passed with 11 routed skills and
  3 task archives.
- `python3 tests/test_distribution.py -v` passed all 6 focused regressions. Its
  fresh target independently passed the installed validator with 11 skills and
  0 archives.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v` passed all 36 tests
  after the implementation commit.
- Ruff lint and format checks for all changed Python paths passed, as did
  `git diff --check`.
- The post-implementation worktree was clean before this handoff-only state
  update.

#### Assumptions

- Installation runs against an existing, stable target directory with no
  concurrent process rewriting paths during preflight and copy.
- Refusing every existing payload destination is preferable to implicit merge
  behavior; overwrite, update, and uninstall remain explicit non-goals.
- Python 3.12.9 was the exercised runtime; the implementation uses only the
  standard library.

#### Uncertainties

- No real target repository was modified, per task scope; evidence comes from
  disposable Git repositories.
- No separate non-POSIX platform matrix was run. The current regressions
  exercise regular files, directories, and symlinks on the repository's Linux
  environment.
- The Driver self-audit cannot establish the required independent verdict.

#### Review Focus

- Recompute the manifest boundary and confirm no live state, historical
  artifact, test, source README, installer, or `.git` path can enter a target.
- Attempt to falsify collision completeness, protected-target preservation,
  exclusive writes, and rollback ownership.
- Check whether relaxing the validator's root-README requirement is exactly
  bounded to the now-excluded non-runtime document.
- Challenge `results-audit` for missing generic invariants, accidental
  repository-specific policy, duplication, or mandatory routing.
- Confirm no P2 maturity vocabulary, target adapters, configurable
  distribution platform, or overwrite/update/uninstall behavior entered the
  change.

#### Recommended Next Action

Reviewer `codex-a` should reproduce the fixed implementation commit, use
`review-and-falsification` with `code-audit`, append an independent verdict,
set `Turn` back to `driver`, and commit the review state.

### Session Completion

#### Work completed

Initialized Task 004 on its dedicated branch, implemented the fixed clean
payload and installer, added the generic `results-audit` procedure and routing,
replaced the unsafe regression, documented behavior and residual risks,
self-audited the implementation, and committed the reviewable slice.

#### Evidence

Implementation commit `92148b4c19b84614301c03ff77b736de54cb65d7`;
live validation passed; 6 focused and 36 full regressions passed; Ruff and
whitespace checks passed.

#### Files changed

Distribution manifest/templates and installer; `results-audit` and adjacent
routing; `AGENTS.md`; `README.md`; validator requirements; distribution and Git
workflow tests; Driver audit; this task record.

#### Tests or experiments run

Disposable fresh-install, exact collision, blocking-ancestor collision,
nonexistent-target, and injected-copy-failure cases; full unit discovery; live
workflow validation; Ruff lint/format; Git whitespace check.

#### Known limitations

The installer assumes a stable target during its preflight/copy window, and an
uncatchable process termination can leave only newly created payload paths for
manual inspection. It has not been run against any assessed external target or
in a non-POSIX test matrix.

#### Unresolved questions

Only the independent Reviewer verdict and any resulting required changes.

#### Repository state updated

Yes

#### Recommended next action

Reviewer `codex-a` should start from the committed handoff, reproduce the
evidence, and record the Task 004 verdict in this Handoff Log.
