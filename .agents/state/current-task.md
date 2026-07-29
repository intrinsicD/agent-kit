# Current Task

## Title

Refactor distribution boundary and add results-audit skill

## Task ID

004

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

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

Accepted

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

### Review (codex-a, Reviewer, Round 1)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

The implementation satisfies the behavioral slice under its documented stable-
target assumption:

- The fixed manifest contains 22 unique destinations, all sources are tracked,
  and no destination has another payload file as an ancestor.
- Manifest path validation prevents absolute, dot-segment, backslash, `.git`,
  duplicate-destination, missing, symlink-source, and repository-escape cases.
- Preflight finds exact destinations plus file and symlink ancestors before
  writes. Exclusive creation protects a destination that appears after
  preflight, and owned-path rollback handles ordinary copy failures.
- Blank templates, rather than live state or history, populate all operational
  and index destinations.
- The installed authority routes all 11 installed skills, and the optional
  `results-audit` procedure contains the six generic invariant groups supported
  by Task 003 without importing target-specific rules or P2 mechanisms.

The validator's removal of the root `README.md` requirement is bounded to a
non-runtime source document that is intentionally absent from target payloads.
The installed validator still checks its authority, skills, state, directories,
task lifecycle, and archives.

#### Evidence Quality

The functional evidence reproduced:

- Six of six focused distribution tests passed.
- All 36 repository tests passed.
- Live validation passed with 11 skills and three archives.
- Ruff lint and `git diff --check` passed.
- An independent committed-artifact probe extracted `git archive 92148b4`,
  installed from that checkout, and passed the installed validator with 11
  skills and zero archives.
- An independent all-destinations probe populated every one of the 22 manifest
  destinations; the installer reported exactly 22 collisions and left the
  target byte-for-byte unchanged.
- A separate probe confirmed installation into pre-existing nonblocking
  `.agents`, `docs`, and `scripts` directories preserves unrelated target
  content.

One durable evidence claim did not reproduce as written.
`ruff format --check scripts/install_agent_workflow.py
scripts/validate_agent_workflow.py tests/test_distribution.py
tests/test_agent_workflow.py` exits nonzero and names the validator and legacy
workflow test. The same two files fail at setup commit `0a66c6f` and
implementation commit `92148b4`, so this is unchanged formatting debt, not a
Task 004 behavior regression. However,
`docs/audits/distribution-installer.md` and the Driver handoff currently state
that Ruff format checks passed for all changed Python paths.

#### Simplicity

The fixed JSON manifest, one standard-library installer, separate blank
templates, and one focused optional skill are proportionate. There is no
configurable generator, adapter layer, plugin system, overwrite/update mode, or
P2 workflow expansion. The public command has one obvious path.

#### Missing Cases

- The committed suite samples three exact collisions and two blocking
  ancestors rather than materializing all 22 simultaneously; the independent
  review supplied that exhaustive probe and it passed.
- Manifest validation does not explicitly reject one payload destination being
  the ancestor of another. The fixed manifest is independently verified not to
  contain that relation, and an internally conflicting future manifest would
  fail and roll back rather than overwrite target data. Treat an early
  `ManifestError` check as optional hardening.
- Python minimum-version and non-POSIX support are not documented. The code was
  exercised on Python 3.12/Linux, and the handoff already scopes that evidence.

#### Required Changes

1. Correct the Ruff-format evidence in
   `docs/audits/distribution-installer.md`. State which exact paths the format
   check covered successfully, and record that the two legacy files fail
   identically at `0a66c6f` and `92148b4`. Do not reformat unrelated legacy
   files merely to make the claim green.
2. In the revision handoff, replace the broad Ruff-format claim with the exact
   commands and outcomes. Re-run the focused suite, full suite, live validator,
   Ruff lint, new-file Ruff format check, and whitespace check after the
   evidence correction.

#### Optional Improvements

- Reject internal destination ancestor/descendant conflicts during manifest
  loading.
- State a minimum supported Python version when the project establishes a
  compatibility policy.

### Session Completion (codex-a, Reviewer, Round 1)

#### Work completed

Independently audited Task 004's filesystem ownership, payload boundary,
installed artifact, validator compatibility, results-audit scope, regression
claims, and architectural proportionality.

#### Evidence

The implementation passed all functional and adversarial probes. A single
durable Ruff-format claim was contradicted by exact baseline and implementation
commands, requiring an evidence-only revision.

#### Files changed

- `.agents/state/current-task.md`

#### Tests or experiments run

- Six focused distribution regressions.
- Full 36-test discovery.
- Live workflow validation.
- Ruff lint and four-path Ruff format checks.
- Baseline-versus-implementation Ruff format comparison.
- Whitespace check.
- Exhaustive 22-destination collision/no-write probe.
- Existing-parent/unrelated-content preservation probe.
- Installation and validation from the committed Git archive.

#### Known limitations

No concurrent-adversary, uncatchable-termination, non-POSIX, or alternate
Python-version matrix was run. These remain explicit support boundaries rather
than approved portability claims.

#### Unresolved questions

Only the bounded evidence correction above blocks acceptance.

#### Repository state updated

Yes

#### Recommended next action

Driver corrects the durable audit and handoff evidence without changing the
accepted implementation scope, reruns the exact checks, and returns the same
implementation for Round 2 review.

### Handoff (codex-b, Driver, Revision Round 1)

#### Objective

Return the unchanged Task 004 behavior for Round 2 review after correcting only
the overbroad Ruff-format evidence identified in Round 1.

#### Changes

- Commit `0b1bd0ac1389db6b2790698996815aaafa7bf22b` replaces the audit's
  broad formatting statement with exact lint and formatting commands, paths,
  and outcomes.
- The prior Driver claim that Ruff format passed for all changed Python paths
  is withdrawn. Only `scripts/install_agent_workflow.py` and
  `tests/test_distribution.py` pass the Task 004 format check.
- No implementation, manifest, template, skill, validator, or test behavior
  changed. The reviewable implementation remains commit
  `92148b4c19b84614301c03ff77b736de54cb65d7`.
- The two optional improvements from Round 1 remain outside this bounded
  evidence correction.

#### Evidence

- In separate `git archive` checkouts of setup commit `0a66c6f` and
  implementation commit `92148b4`, the exact command `ruff format --check
  scripts/validate_agent_workflow.py tests/test_agent_workflow.py` exited 1
  identically: both runs named those two files and reported `2 files would be
  reformatted`.
- `ruff check scripts/install_agent_workflow.py
  scripts/validate_agent_workflow.py tests/test_distribution.py
  tests/test_agent_workflow.py` passed all four changed Python paths.
- `ruff format --check scripts/install_agent_workflow.py
  tests/test_distribution.py` exited 0 and reported `2 files already
  formatted`.
- With `PYTHONDONTWRITEBYTECODE=1`, `python3 tests/test_distribution.py -v`
  passed 6 of 6 focused tests.
- With `PYTHONDONTWRITEBYTECODE=1`, `python3 -m unittest discover -s tests -p
  'test_*.py' -v` passed all 36 tests.
- With `PYTHONDONTWRITEBYTECODE=1`, `python3
  scripts/validate_agent_workflow.py` passed with 11 routed skills and 3 task
  archives.
- `git diff --check` passed after the evidence correction.

#### Assumptions

- The identical Ruff-format output at setup and implementation commits is
  evidence of pre-existing formatting debt, not permission to claim those
  legacy files pass formatting.
- Reformatting unrelated legacy files would expand this revision beyond the
  Reviewer's required evidence correction.

#### Uncertainties

None beyond the independent Round 2 verdict. All functional findings from
Round 1 were already positive and no behavior changed.

#### Review Focus

Confirm the durable audit now scopes Ruff lint and formatting separately,
records the identical legacy failures at both fixed commits, and makes no
remaining broad all-changed-path formatting claim.

#### Recommended Next Action

Reviewer `codex-a` should verify commit
`0b1bd0ac1389db6b2790698996815aaafa7bf22b`, reproduce the bounded formatting
commands, and append the Round 2 verdict.

### Session Completion (codex-b, Driver, Revision Round 1)

#### Work completed

Corrected the one contradicted evidence statement, reproduced the identical
legacy formatting failures at the setup and implementation commits, reran the
complete requested check set, and returned the unchanged implementation for
independent review.

#### Evidence

Evidence correction commit `0b1bd0ac1389db6b2790698996815aaafa7bf22b`;
6 focused and 36 full tests passed; live validation passed; four-path Ruff lint
passed; the two new Task 004 Python files passed Ruff format; the two legacy
files failed identically at `0a66c6f` and `92148b4`; whitespace validation
passed.

#### Files changed

- `docs/audits/distribution-installer.md`
- `.agents/state/current-task.md`

#### Tests or experiments run

Focused distribution suite, full unit discovery, live workflow validator,
four-path Ruff lint, two-new-file Ruff formatting, setup-versus-implementation
legacy formatting comparison, and Git whitespace validation.

#### Known limitations

The validator and legacy workflow test retain their pre-existing Ruff
formatting debt. No unrelated formatting or optional implementation hardening
was added.

#### Unresolved questions

Only the independent Round 2 verdict.

#### Repository state updated

Yes

#### Recommended next action

Reviewer `codex-a` should reproduce the corrected evidence and record the
terminal Task 004 verdict.

### Review (codex-a, Reviewer, Round 2)

#### Verdict

Accepted

#### Self-reviewed

No

#### Correctness

The fixed implementation at `92148b4` remains unchanged and satisfies every
Task 004 success criterion. It provides an explicit clean payload, blank
operational templates, complete stable-target collision refusal before writes,
exclusive destination creation, owned-path rollback, preserved target Git
metadata, installed-state validation, and an optional generic results-audit
procedure with no target-specific or P2 scope.

#### Evidence Quality

- The audit correction at `0b1bd0a` now distinguishes four-path Ruff lint,
  two-new-file Ruff formatting, and the identical two-legacy-file formatting
  failure at setup and implementation commits.
- Six of six focused distribution tests and all 36 repository tests pass.
- Live validation passes with 11 routed skills and three task archives.
- Ruff lint, new-file Ruff format validation, and whitespace checks pass.
- `git diff --quiet 92148b4..HEAD -- AGENTS.md README.md .agents/skills
  distribution scripts tests` confirms no implementation, routing,
  documentation, template, or test behavior changed during the evidence
  revision.
- Round 1 independently validated all 22 simultaneous collisions, preservation
  of unrelated content under existing parents, and installation from the
  committed Git archive.

#### Simplicity

The implementation remains the smallest coherent integration supported by the
accepted cross-repository assessment: one fixed manifest, one installer, blank
templates, one optional skill, and focused tests. It adds no speculative
configuration or target-specific workflow layer.

#### Missing Cases

Concurrent adversarial filesystem mutation, uncatchable termination,
non-POSIX behavior, and alternate Python versions remain outside the approved
evidence. The README states the stable-target concurrency assumption; the task
and audit record the exercised Python/Linux boundary.

#### Required Changes

None.

#### Optional Improvements

- Reject internal destination ancestor/descendant conflicts when loading a
  future edited manifest.
- Document a minimum Python version when the project adopts a compatibility
  policy.

### Session Completion (codex-a, Reviewer, Round 2)

#### Work completed

Verified the bounded evidence correction, confirmed implementation immutability,
reran the focused and full validation set, and returned an independent
Accepted verdict.

#### Evidence

Correction `0b1bd0a`; implementation `92148b4`; 6/6 focused and 36/36 full
tests pass; live validator, Ruff lint, new-file formatting, and whitespace
checks pass.

#### Files changed

- `.agents/state/current-task.md`

#### Tests or experiments run

Focused distribution suite, full unittest discovery, live workflow validation,
four-path Ruff lint, two-new-file Ruff formatting, implementation immutability
diff, and whitespace validation.

#### Known limitations

The accepted behavior is deliberately non-overwriting and stable-target only;
update, uninstall, concurrent-adversary, portability-matrix, and target-profile
features are not implied.

#### Unresolved questions

None blocking completion.

#### Repository state updated

Yes

#### Recommended next action

Driver merges the accepted task branch, archives Task 004, updates repository
state to 11 skills and 36 tests, and runs final post-merge validation.
