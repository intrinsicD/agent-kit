# Current Task

## Title

Implement the maturity program verification foundation

## Task ID

006

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

## Mode

Implement

## Goal

Provide one local verification command, mirrored verbatim in CI, that checks
formatting, lint, workflow structure, the ARA claim ledger, and the full
regression suite.

## Motivation

The owner-authorized maturity program identifies verification as the dependency
for every later installer/profile slice. The live baseline has 36 passing tests
and a passing workflow validator, but Ruff 0.15.20 still reports two known
format failures, the ARA ledger is unchecked, and the repository has no single
verification entry point or CI workflow.

## Success Criteria

1. `./scripts/verify.sh` exits 0 on the clean tree and an induced failure in
   each of its five gates makes it exit nonzero.
2. Repository-wide `ruff check` and `ruff format --check` pass with the exact
   version pinned in `requirements-dev.txt`; the two-file format-only change is
   isolated in a mechanical commit.
3. `scripts/check_ara.py` accepts the live ledger and rejects fixtures for each
   documented ledger invariant.
4. `.github/workflows/ci.yml` tests Python 3.11, 3.12, and 3.13 and invokes
   `./scripts/verify.sh` verbatim; a regression test pins that stage list.
5. `README.md` documents the one-command workflow and claim ledger, all
   existing tests remain green, and the maturity plan records its actual task
   numbering and any verified divergence from the proposed baseline.

## Constraints

- Use only the Python standard library in repository scripts; Ruff is the sole
  pinned development dependency.
- Do not change claim C13 or the distribution manifest.
- Keep mechanical formatting separate from semantic changes.
- Preserve the refusal-on-collision installer behavior and the 22-file payload.
- Treat the maturity plan as planning input: actual task state and reviewed
  evidence supersede indicative numbering.

## Non-Goals

- Target-facing verification/CI templates or ARA templates.
- Installer profiles, slug rendering, dry-run, or doctor behavior.
- The proposed single-product convergence decision affecting IntrinsicEngine.
- Changes to payload skill behavior or the payload `AGENTS.md`.

## Selected Skills

- `task-orchestration`
- `implementation`
- `code-audit`
- `review-and-falsification`
- `handoff`
- `repo-organization`

## Current Evidence

- `python3 scripts/validate_agent_workflow.py`: pass; 11 skills and 5 archives.
- `python3 -m unittest discover -s tests -v`: 36/36 pass.
- `ruff check .` with Ruff 0.15.20: pass.
- `ruff format --check .` with Ruff 0.15.20: fails only
  `scripts/validate_agent_workflow.py` and `tests/test_agent_workflow.py`.
- Task ID 005 is already archived, so the plan's first indicative ID binds to
  actual task 006.

## Minimal Plan

1. Record this task and the validated remaining program backlog on a task
   branch.
2. Commit the two-file Ruff formatting change mechanically and re-run the
   unchanged suite.
3. Add the pinned toolchain and five-stage `verify.sh`.
4. Implement and fixture-test the ARA ledger checker.
5. Add CI, stage-list regression coverage, README guidance, and a dated plan
   amendment.
6. Run clean and induced-failure checks, audit the code and diff, then prepare
   a committed Driver handoff for independent review.

## Status

Revision required

## Human Decisions

Escalated questions and the answers humans gave. An answer that exists only in
chat is not recorded. Use one block per decision:

```markdown
### Question
### Options
### Recommendation
### Decision
### Date
```

## Handoff Log

Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`.

### Handoff (codex-b, Driver)

#### Objective

Independently verify that task 006 supplies one reproducible five-stage gate,
enforces the existing ARA ledger, and mirrors the gate verbatim in a
three-version CI matrix without changing the installable payload.

#### Changes

- Isolated the two legacy format corrections in commit `a884ccb`.
- Added Ruff 0.15.20 pin/configuration, `scripts/verify.sh`,
  `scripts/check_ara.py`, 17 fixture tests, README guidance, and the live
  heading normalization in commit `a25c0f9`.
- Added the Python 3.11/3.12/3.13 workflow, four verification/CI regression
  tests, and a dated maturity-plan amendment in commit `f2fc7e8`.
- Registered the remaining maturity program as dependency-aware backlog and
  recorded the Driver audit in `docs/audits/verification-foundation.md`.

#### Evidence

- Clean `./scripts/verify.sh`: exit 0; Ruff lint and format pass, workflow
  validator passes, `check_ara` reports 13 valid claims, and 57/57 tests pass.
- Disposable induced failures all exit 1 at the intended stage: unused/undefined
  import (lint), unformatted assignment (format), `In progress` with Reviewer
  turn (workflow), missing C01 proof path (ARA), and a deliberately wrong Ruff
  pin assertion (unit tests).
- GitHub Actions run
  `https://github.com/intrinsicD/agent-kit/actions/runs/30438019981` succeeded
  for Python 3.11, 3.12, and 3.13 at `f2fc7e8`.
- `git diff 878018d..f2fc7e8 -- distribution/manifest.json` is empty.
- Task initialization and every implementation increment are committed; the
  worktree was clean before this handoff update.

#### Assumptions

- The owner's request authorizes the proposed dependency order and Python
  support floor. The cross-repository convergence decision D1 remains
  deliberately unaccepted.
- Current official action majors (`checkout@v7`, `setup-python@v6`) are
  appropriate for GitHub-hosted runners.

#### Uncertainties

- The checker covers inline Markdown links and images, not reference-style
  Markdown links, because the live PAPER uses only inline links.
- Commit-shaped proof references remain syntax-only and are not looked up in
  Git, matching the stated constraint.
- Immutable action SHA pinning was outside the proposed scope.

#### Review Focus

- Attempt to bypass or crash each ARA invariant, especially wrapped fields,
  mixed path/commit proofs, duplicate IDs, and malformed headings.
- Confirm the stage-list test cannot pass if CI or `verify.sh` re-lists or
  reorders gates.
- Reproduce the clean gate and inspect the successful three-version CI run.
- Confirm the format commit is mechanical and the distribution manifest and
  payload expectations are unchanged.

#### Recommended Next Action

Use `review-and-falsification` and `code-audit`, append an independent verdict,
and return the turn to the Driver.

### Review (codex-a, Reviewer, Round 1)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

The verification foundation is largely functional at reviewed commit
`b158809`: the clean command succeeds, each of the five intended failures
stops at its own gate, the CI workflow invokes the command on the required
Python matrix, the format-only commit is mechanical, and the distribution
boundary is unchanged.

Four counterexamples prevent acceptance:

1. Status handling is inconsistent. `check_claim_statuses` accepts
   `supported:` after stripping punctuation, while `check_claim_proofs`
   compares the unstripped word. Changing C01 to `Status: supported:` and
   leaving only commit proof `[abcdef0]` therefore exits 0 even though a
   supported claim must cite an existing repository path.
2. A proof path can escape the repository. Replacing C01's proof with
   `[docs/../../../../../../etc/passwd]` exits 0 because the checker tests
   existence without resolving and enforcing containment under the repository
   root. An external host file consequently satisfies the repository-proof
   invariant.
3. Field-like bullets outside the narrow alphabetic `FIELD` pattern are
   silently ignored. Adding `- **Mystery-key**: bypassed` to C01 exits 0, so
   the checker does not enforce its stated “only known optional fields”
   invariant for malformed or punctuated keys.
4. The stage-list regression only inspects commands immediately following
   numbered `echo` lines. Duplicating the complete ARA gate command on the next
   line leaves all four verification regression tests green, despite the test
   claiming that `verify.sh` runs exactly five stages and the review focus
   requiring re-listed gates to fail.

Wrapped proof fields and mixed commit/path proofs otherwise parsed correctly.
Mixed commit plus missing-path proof failed, as did duplicate claim IDs and a
malformed claim heading.

#### Evidence Quality

- Local Python 3.12.9 with Ruff 0.15.20: `./scripts/verify.sh` exited 0,
  validated 11 skills and five archives, accepted 13 claims, and passed 57
  tests.
- Independent disposable mutations exited 1 at stages 1 through 5 for,
  respectively, an unused import, an unformatted assignment, an invalid
  status/turn pairing, a missing claim proof, and a deliberately wrong unit
  assertion.
- GitHub Actions run `30438019981` is tied to `f2fc7e8`; its CPython 3.11.15,
  3.12.13, and 3.13.14 jobs each installed Ruff 0.15.20 and successfully ran
  `./scripts/verify.sh` with 57 tests.
- AST comparison before and after `a884ccb` was identical for both formatted
  files; that commit changes no other file.
- `git diff main...HEAD -- distribution/` is empty, the manifest still has 22
  files, and all six installer regressions pass.
- The four acceptance-blocking probes above were run against disposable
  archives of reviewed commit `b158809`, not against Driver-authored fixture
  claims alone.

#### Simplicity

One POSIX entry point, one exact Ruff pin, one standard-library ledger checker,
and one matrix workflow are proportionate to the task. No target-facing
profile, payload expansion, or speculative framework was introduced. The
required fixes are local validation/test corrections and do not justify a
larger parser or dependency.

#### Missing Cases

Reference-style PAPER links, Git resolution of commit-shaped proofs, Windows
support, and immutable action SHA pinning remain explicitly outside this
slice. General dependency-cycle detection and a richer claim-value grammar are
also not required by the documented nine checks.

#### Required Changes

1. Normalize a claim's status disposition once and use the same result for
   status validation and disposed-claim proof enforcement; add a regression
   for the punctuated-status/no-path counterexample (or reject punctuation
   consistently).
2. Resolve recognized proof paths and require them to remain within the
   repository root before they can count as existing repository evidence;
   reject traversal and symlink escapes and add focused regressions.
3. Detect and reject unrecognized field-like claim bullets instead of silently
   ignoring keys that fall outside the current `FIELD` regex; add the
   punctuated-key regression.
4. Strengthen the stage-list regression so re-listing any complete gate
   command fails (at minimum, assert every expected gate command occurs exactly
   once as well as in order). Retain the CI prohibition on re-listed gates.
5. Re-run the clean gate, the focused counterexamples, the five induced
   failures, and the three-version CI matrix, then hand the revision back for
   Round 2.

#### Optional Improvements

- Add reference-style PAPER-link support if the live artifact adopts it.
- Resolve commit-shaped proofs through Git only if a later requirement changes
  the current syntax-only constraint.
- Pin GitHub actions to immutable SHAs in a separately scoped supply-chain
  hardening task.

### Session Completion (codex-a, Reviewer, Round 1)

#### Work completed

Independently audited the implementation, parser invariants, shell/CI mirroring,
mechanical formatting boundary, plan amendment, and unchanged distribution;
recorded a Revision required verdict without modifying implementation files.

#### Evidence

Clean and induced-failure gates, GitHub run `30438019981`, AST equivalence,
distribution diff/count, focused valid fixtures, and four bypass
counterexamples are recorded in the Review above.

#### Files changed

`.agents/state/current-task.md` only.

#### Tests or experiments run

`./scripts/verify.sh`; five disposable gate failures; seven focused ARA
mutations; duplicate-stage regression mutation; GitHub run/job/log inspection;
shell syntax checks; outside-working-directory invocation; AST comparison; and
distribution diff/count checks.

#### Known limitations

The explicitly out-of-scope cases listed under Missing Cases were not promoted
to required changes.

#### Unresolved questions

None requiring human input.

#### Repository state updated

Yes

#### Recommended next action

Driver `codex-b` implements the four bounded validation/test corrections,
collects fresh local and CI evidence, and returns task 006 for Round 2 review.
