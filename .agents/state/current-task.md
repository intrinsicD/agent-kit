# Current Task

## Title

Implement the maturity program verification foundation

## Task ID

006

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: human

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

Blocked on human decision

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

### Question

After two independent `Revision required` rounds, should task 006 receive one
final bounded correction and review?

### Options

1. **Authorize one final bounded revision.** Add two regressions and fixes:
   reject empty or punctuation-only `Status` values, and detect repeated gate
   commands after removing trailing shell comments. Re-run the local/CI matrix
   and one final independent review. This preserves the task's success criteria
   with a small, reversible change.
2. **Accept the known false negatives.** Keep the implementation as-is and
   weaken the documented status and exact-stage claims. This avoids another
   round but knowingly permits malformed claims and duplicate executed gates.
3. **Close as inconclusive.** Do not merge the branch; retain the task record
   and leave the maturity program blocked on its verification dependency.

### Recommendation

Option 1. Both defects are reproduced, acceptance-blocking false negatives with
small local fixes; neither requires a new dependency, abstraction, or scope
expansion.

### Decision

Pending the repository owner's answer in the task conversation.

### Date

2026-07-29

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

### Handoff (codex-b, Driver, Round 2)

#### Objective

Verify that commit `04322dc` closes all four Round 1 bypasses without widening
task scope or weakening any original gate.

#### Changes

1. Added `status_disposition()` and use it for both status allowlisting and
   disposed-claim proof enforcement.
2. Resolve every recognized proof path with `strict=True`, require the resolved
   target to remain under the repository root, and reject both traversal and
   symlink escapes.
3. Parse any bold field-like bullet with a colon, including punctuated names
   and whitespace before the colon, then reject names outside the required and
   optional field allowlists.
4. Require each of the five exact gate commands to occur once in
   `scripts/verify.sh`, in addition to checking stage order.
5. Added four focused checker regressions plus traversal and symlink variants;
   the full suite grows from 57 to 61 tests.

#### Evidence

- Focused ARA suite: 21/21 pass; focused verification suite: 4/4 pass.
- Clean `./scripts/verify.sh`: exit 0 with 61/61 tests and all five gates.
- Disposable copies of `04322dc`: the punctuated-status/no-path bypass,
  `/etc/passwd` traversal, punctuated unknown field, and duplicate ARA gate
  each exit 1 at the expected ARA or unit-test stage.
- The original five induced failures still exit 1 at stages 1 through 5.
- GitHub Actions run
  `https://github.com/intrinsicD/agent-kit/actions/runs/30439177610` succeeds on
  Python 3.11, 3.12, and 3.13 at `04322dc`.
- `distribution/manifest.json` remains unchanged.

#### Assumptions

No new assumption. Repository containment is evaluated on resolved paths, so a
symlink to an in-repository artifact is allowed and a symlink out of the
repository is rejected.

#### Uncertainties

The explicitly accepted limitations from Round 1 remain: reference-style PAPER
links, Git resolution of commit-shaped proofs, Windows support, and immutable
action SHA pinning are out of scope.

#### Review Focus

- Re-run the four exact Round 1 counterexamples and try nearby punctuation,
  path-normalization, and symlink variants.
- Mutate `verify.sh` with a duplicate expected command and confirm the
  verification regression fails.
- Confirm the shared status normalization cannot diverge between validation
  and proof enforcement.
- Reproduce the clean suite and inspect CI run `30439177610`.

#### Recommended Next Action

Perform Round 2 independent review. If the four required changes are closed,
record `Accepted`, return `Turn: driver`, and let the Driver run the accepted
closeout flow.

### Review (codex-a, Reviewer, Round 2)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

Commit `04322dc` closes each exact Round 1 counterexample:

- `supported:` with commit-only proof is rejected, as is the nearby
  `:SuPpOrTeD;,` spelling; an unknown `accepted:` disposition is also rejected.
- `Mystery-key`, slash, underscore, and Unicode-punctuation field names are
  parsed and rejected as unknown.
- The original traversal to `/etc/passwd`, a direct external symlink, and a
  symlinked external directory are rejected. Normalized traversal and symlinks
  that resolve inside the repository remain valid.
- An exact duplicate gate command, including one indented with whitespace,
  reaches the regression stage and fails its uniqueness assertion.

Two nearby counterexamples still violate the documented invariants:

1. `status_disposition()` normalizes punctuation-only input to an empty string,
   and `check_claim_statuses()` treats that result like an absent field and
   silently continues. Replacing C01's status with either `- **Status**: :;,.`
   or an empty `- **Status**:` makes `check_ara.py` exit 0. A present Status
   field therefore need not have the documented first-word disposition.
2. Gate uniqueness is based on exact stripped-line equality. Duplicating
   `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_ara.py` with only a trailing
   `# duplicated gate` comment executes the ARA checker twice, yet
   `./scripts/verify.sh` exits 0 and all 61 tests pass. The regression therefore
   still permits a directly re-listed gate and does not fully pin the five-stage
   command list.

These are bounded false negatives in success criteria 3 and 4, not requests
for a richer value grammar or a general shell parser.

#### Evidence Quality

- Local Python 3.12.9 with Ruff 0.15.20: clean `./scripts/verify.sh` exited 0,
  accepted 13 live claims, and passed 61 tests.
- GitHub Actions run `30439177610` is tied to implementation commit `04322dc`.
  Its CPython 3.11.15, 3.12.13, and 3.13.14 jobs each installed Ruff 0.15.20,
  invoked `./scripts/verify.sh`, accepted 13 claims, and passed 61 tests.
- Disposable archives of branch HEAD `57b5c7c` reproduced all exact and nearby
  status, field, traversal, symlink, and duplicate-gate cases described above.
- The original external traversal and two external-symlink variants exited 1;
  an internal normalized path and internal symlink each exited 0, confirming
  containment rather than blanket symlink rejection.
- The exact duplicate gate exited 1 at the unit-test stage. The same executed
  command with a trailing comment ran twice and exited 0, isolating the
  remaining regression-test gap.
- The Round 2 implementation commit changes only `scripts/check_ara.py`,
  `tests/test_check_ara.py`, and `tests/test_verification.py`; distribution
  content remains unchanged.

#### Simplicity

The shared normalization helper, resolved-path containment check, wider
field-like pattern, and per-command uniqueness assertion are small and
proportionate. The remaining corrections require only rejecting an empty
normalized status and making the existing textual uniqueness check recognize
an executed command with an inline comment. No new dependency, parser
framework, or payload change is justified.

#### Missing Cases

The Round 1 accepted limits—reference-style PAPER links, Git lookup of
commit-shaped proofs, Windows support, and immutable action SHA pinning—remain
out of scope. This review also does not require recognizing arbitrary
shell-equivalent rewrites; the failing variant repeats the complete expected
command text on an executable line and adds only an inline comment.

#### Required Changes

1. Treat an empty normalized disposition as invalid when the Status field is
   present. Add focused regressions for an empty value and punctuation-only
   value, while preserving the corrected punctuated-supported behavior.
2. Make the stage-list regression reject the complete expected gate command
   when it is repeated on an executable line with an inline shell comment.
   Preserve the existing order and exact-duplicate checks and add the reviewed
   trailing-comment fixture.
3. Re-run the focused counterexamples, clean verification, and supported Python
   matrix after any authorized correction.

#### Optional Improvements

- Keep arbitrary semantic shell-command equivalence outside this textual
  regression's scope.
- Retain the previously recorded optional reference-link, commit-resolution,
  and action-SHA hardening as separate future work.

### Session Completion (codex-a, Reviewer, Round 2)

#### Work completed

Independently inspected the Round 2 revision, reproduced the clean local and CI
evidence, exercised the four exact fixes and nearby variants, and recorded the
remaining two false negatives without changing implementation.

#### Evidence

The clean 61-test gate, CI run `30439177610`, status and field variants,
traversal and symlink boundaries, and exact/commented duplicate-gate outcomes
are recorded in the Review above.

#### Files changed

`.agents/state/current-task.md` only.

#### Tests or experiments run

`./scripts/verify.sh`; GitHub run/job/log inspection; three status variants
plus empty and punctuation-only statuses; four unknown-field spellings;
external and internal traversal; direct and directory external symlinks;
an internal symlink; and exact, indented, and inline-comment duplicate gates.

#### Known limitations

Only the explicitly scoped cases under Missing Cases remain untested or
unrequired.

#### Unresolved questions

Per the repository protocol, two full revision rounds have now ended without
an accepting verdict. A human must decide whether to authorize one final
bounded correction or accept the two known false negatives.

#### Repository state updated

Yes

#### Recommended next action

Driver `codex-b` follows the two-round escalation rule: record the two options,
evidence, consequences, and recommendation under Human Decisions, set
`Status: Blocked on human decision` and `Turn: human`, commit, and raise the
decision through the task conversation before any third revision.

### Escalation (codex-b, Driver)

#### Trigger

Round 1 and Round 2 both returned independent `Revision required` verdicts.
Repository policy prohibits beginning a third revision without a human
decision.

#### Evidence

Round 2 confirms every Round 1 bypass is closed and the clean 61-test gate plus
Python 3.11–3.13 CI are green. It also reproduces two remaining false
negatives: empty/punctuation-only Status values pass, and a duplicated gate
with a trailing shell comment runs twice while the stage-list test passes.

#### Recommendation

Authorize one final bounded correction comprising two tests, the minimal
validation changes, fresh local/CI evidence, and one final independent review.

#### Recommended Next Action

The repository owner chooses one option under Human Decisions. The receiving
Driver records that answer and date before any implementation work resumes.
