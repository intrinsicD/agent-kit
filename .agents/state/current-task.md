# Current Task

## Title

Fix agent workflow audit findings

## Task ID

002

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: reviewer

## Mode

Stabilize

## Goal

Make the two-agent workflow safe to install and internally enforce the
documented task, review, archive, and closeout lifecycle.

## Motivation

The accepted audit demonstrated six installation, schema, validation, branch
closeout, archive, and example-history failures that block safe adoption.

## Success Criteria

- Installation uses a tracked-file export that cannot copy `.git/`, with
  explicit collision behavior and guidance.
- Handoff and review templates use headings nested under `## Handoff Log`.
- The validator rejects all eleven audit matrix failures and enforces role,
  structured-review, status, and turn semantics while accepting valid
  independent and self-reviewed lifecycles.
- Accepted, Rejected, Inconclusive, and Superseded branch closeout paths are
  explicit and safely preserve metadata without merging rejected changes.
- Partial active records and malformed archives fail validation; valid archives
  require matching ids, terminal statuses, `Turn: none`, and valid verdicts.
- The illustrative task is outside operational history and automated regression
  tests cover the audit matrix plus valid lifecycle, archive, and closeout cases.
- Focused tests, full workflow validation, syntax compilation, and diff checks
  pass.

## Constraints

- Preserve the existing lightweight Markdown workflow and Python standard
  library implementation.
- Avoid external dependencies, speculative redesign, and unrelated changes.
- Work sequentially in the shared tree and hand the committed branch to the
  independent Reviewer.

## Non-Goals

- Turning the cooperative `Turn` marker into a concurrency lock.
- Automating merges, pushes, or cross-machine coordination.
- Generalizing the validator beyond this repository's documented schema.

## Selected Skills

- `task-orchestration`
- `implementation`
- `handoff`

## Current Evidence

- `docs/audits/agent-workflow-audit.md` records six findings and eleven
  reproduced validator mismatches.
- The audited validator treated only a non-empty title as active, recognized
  review text by a broad heading regex, and validated archives only by
  filename/id uniqueness.
- The audited README installed with `cp -r agent-kit/.`, which included
  `.git/`.
- The pre-fix regression run produced 13 expected failures across the audited
  invalid states and archive requirements.
- The candidate implementation passes all 21 tests, including the eleven-case
  audit matrix, valid active/archive lifecycles, target Git-metadata
  preservation, accepted merge closeout, and metadata-only closeout for
  Rejected, Inconclusive, and Superseded branches.
- Full validation now reports ten routed skills, one operational archive, and
  no active-state issues; the illustrative record is outside `docs/tasks/`.

## Minimal Plan

1. Add regression fixtures for the audit matrix and valid lifecycle/archive
   cases.
2. Align documented templates and implement structured active/archive
   validation.
3. Document safe installation and terminal branch closeout flows, and move the
   illustrative record outside operational history.
4. Run focused and full validation, self-audit the diff, and hand the branch to
   the Reviewer.

## Status

In review

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

Resolve all six independently confirmed workflow audit findings without
expanding the repository beyond its lightweight Markdown and standard-library
design.

#### Changes

- Replaced the destructive copy command with a tracked-file `git archive`
  export, collision preflight, and overwrite/recovery guidance.
- Nested Handoff Log templates at `###`/`####` and made the documented example
  use the same shape.
- Replaced heading-presence checks with explicit active/archive task,
  structured-review, verdict, self-review, role, status, turn, mode, and id
  validation.
- Defined accepted merge closeout and metadata-only cherry-pick closeout for
  Rejected, closed Inconclusive, and Superseded branches.
- Made only the exact complete task template exempt from active validation and
  applied the full task schema to archives.
- Moved the illustrative record from `docs/tasks/` to `docs/examples/`.
- Added a 21-test standard-library regression suite covering the audit matrix,
  valid lifecycle/archive cases, installation safety, and all four terminal
  closeout classes.

#### Evidence

- Implementation commit: `f2474e9172d55aa58915dadd730674594752044f`.
- The corrected pre-fix fixture run exposed 13 expected failures; the
  implementation passes 21 of 21 tests.
- `python3 scripts/validate_agent_workflow.py` passes with ten routed skills and
  one operational archive.
- Syntax compilation passes for `scripts/validate_agent_workflow.py` and
  `tests/test_agent_workflow.py`.
- `git diff --check` passes.
- Disposable Git tests preserve a target's remote, branch, and HEAD during
  installation; exclude untracked source files; merge accepted implementation;
  and keep task implementation off the default branch for Rejected,
  Inconclusive, and Superseded closeouts.

#### Assumptions

- `Superseded` closes work without approving a claim, so it does not need a
  Reviewer verdict but does require a recorded reason.
- `Provisionally accepted (self-reviewed)` remains active until independent or
  human promotion and is therefore not an archive-terminal status.
- Cherry-picking a closeout commit whose diff is limited to the active-task
  reset, repository state, and one archive is the smallest safe way to preserve
  negative evidence without merging implementation ancestors.

#### Uncertainties

- The cooperative `Turn` marker still cannot prevent two concurrently started
  agents from editing one worktree; this was explicitly outside scope.
- Markdown validation can enforce distinct labels and structured fields, but it
  cannot cryptographically authenticate which agent authored a review.

#### Review Focus

- Attempt to bypass review detection with `Review Focus`, malformed nested
  fields, earlier versus latest Review blocks, identical labels, or
  self-reviewed acceptance.
- Reproduce the tracked-file installation and metadata-only closeout probes
  independently.
- Challenge exact-template recognition and archive validation with partial,
  mismatched, duplicate, nonterminal, and wrong-turn records.
- Check that the terminal-flow documentation and tests agree and that no
  unnecessary abstraction or dependency was introduced.

#### Recommended Next Action

Review commit `f2474e9`, rerun the focused suite and full validator, and append
an independent structured verdict.

### Session Completion (codex-b, Driver)

#### Work completed

Implemented and self-audited the six audit remediations, committed the reviewed
candidate, and passed the repository turn to the independent Reviewer.

#### Evidence

Implementation commit `f2474e9`; 21/21 regression tests; full validation,
syntax compilation, and diff checks pass.

#### Files changed

Workflow validator and tests; README and AGENTS contract; handoff, review, and
repository-organization skills; audit/task documentation; task state; and the
relocated illustrative example.

#### Tests or experiments run

Eleven-case audit matrix, valid active/archive lifecycle fixtures,
tracked-file installation probe, accepted merge closeout, non-merge closeout
for three terminal statuses, full workflow validation, syntax compilation, and
diff checks.

#### Known limitations

The Turn field remains cooperative rather than a lock, and review authorship is
not cryptographically authenticated.

#### Unresolved questions

None blocking independent review.

#### Repository state updated

Yes

#### Recommended next action

`codex-a` independently falsifies the implementation and returns a verdict.
