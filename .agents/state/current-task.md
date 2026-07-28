# Current Task

## Title

Fix agent workflow audit findings

## Task ID

002

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

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

### Review (codex-a, Reviewer)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

The implementation resolves the six original happy-path reproductions and the
Driver's 21 tests pass, but the validator still accepts malformed states that
violate the stated exact-template, structured-review, and recorded-reason
invariants:

- the untouched task template plus an extra `##` section is treated as the
  untouched template;
- the task template with its `# Current Task` heading removed is treated as the
  untouched template;
- an active task with duplicate `## Status` sections is accepted using only the
  last value;
- an Accepted task can obtain approval from a syntactically complete
  `### Review` embedded inside a fenced Markdown example; and
- Superseded accepts the stock instructional Handoff Log as its recorded
  reason, while an active task also accepts the `-` Selected Skills placeholder.

These are not speculative schema extensions. They are counterexamples to F3,
F4, F5, and Task 002's explicit success criteria.

#### Evidence Quality

The full 21-test suite, validator, syntax compilation, and diff checks pass.
Five independent disposable fixtures then reproduced the invalid acceptances
above. The fenced-review fixture was bounded by a following fake `###` heading
inside the fence, demonstrating that raw regular-expression scanning can treat
example content as an approval block.

#### Simplicity

The implementation remains standard-library-only and the documented
metadata-only closeout is appropriately small. The validator refactor is
justified by the audited state machine; no unnecessary architecture or
dependency was introduced.

#### Missing Cases

Regression coverage does not yet include duplicate task sections, headings
inside fenced code blocks, exact-template extra/missing structure, meaningful
Superseded reasons, or active placeholder Selected Skills.

#### Required Changes

1. Make untouched-template recognition genuinely exact: require the root
   heading and exactly the expected level-two section set, and reject duplicate
   task sections rather than silently taking the last value.
2. Ignore fenced code blocks when identifying Review entries and nested Review
   fields; add a regression proving fenced examples cannot approve work.
3. Reject the stock Handoff Log text as a Superseded reason and reject the
   Selected Skills `-` placeholder in active or archived records.
4. Add the counterexamples above to the regression suite and rerun focused and
   full validation.

#### Optional Improvements

After acceptance, change the audit's remediation status from “candidate,
pending independent review” to the final reviewed outcome and bind historical
line references to the pre-remediation commit where useful.

### Session Completion (codex-a, Reviewer)

#### Work completed

Independently audited the validator, documentation, templates, tests, install
path, and terminal branch-closeout flow.

#### Evidence

The Driver's 21 tests reproduced successfully; five additional malformed-state
classes passed when they should fail.

#### Files changed

`.agents/state/current-task.md` only.

#### Tests or experiments run

Full unittest discovery, full workflow validation, syntax compilation, diff
checks, and disposable exact-template, duplicate-section, fenced-review,
Superseded-reason, and placeholder-field probes.

#### Known limitations

This review did not modify Driver-owned implementation files.

#### Unresolved questions

None. The required changes are bounded by executable counterexamples.

#### Repository state updated

Yes

#### Recommended next action

Driver implements the four required changes and returns the branch for a second
review round.
