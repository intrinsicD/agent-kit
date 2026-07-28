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
- Review round 1 at `0e1e708` reproduced exact-structure, duplicate-section,
  fenced-review, Superseded-reason, and Selected Skills placeholder bypasses
  and returned `Revision required`.
- The bounded revision adds seven regression methods (including active and
  archived placeholder cases), checks fenced Review entries and nested fields,
  and passes all 28 tests plus full validation.
- Review round 2 at `f171162` confirmed the first revision and isolated
  fence-aware Role Assignment parsing plus duplicate role and Review state
  fields as the final required changes.
- The second bounded revision adds three focused regression methods covering
  six reproduced field bypasses; all 31 tests and full validation pass.

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

Accepted

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

### Handoff (codex-b, Driver, Revision Round 1)

#### Objective

Close the four bounded validator gaps from Review round 1 and preserve all
previously valid lifecycle behavior.

#### Changes

- Task parsing now requires the exact `# Current Task` root, rejects unexpected
  or duplicate level-two sections, and includes the exact section set in fresh
  template recognition.
- A small fence-aware Markdown line scanner prevents fenced examples from
  supplying Review entries or nested Verdict/Self-reviewed fields while
  preserving fenced content in task section bodies.
- Superseded rejects blank or stock instructional Handoff Logs, and active or
  archived tasks reject the `-` Selected Skills placeholder.
- Seven regression methods cover the Reviewer's counterexamples, including
  both fenced Review entries and fenced nested fields and both active and
  archived Selected Skills placeholders.

#### Evidence

- Revision implementation commit:
  `876fe17164f4cc7bd196855300a58d2f1492243f`.
- Before the validator change, all seven new regression methods failed against
  independently reproduced accepted states.
- After the change, all 28 tests pass.
- `python3 scripts/validate_agent_workflow.py` passes with ten routed skills and
  one validated operational archive.
- Syntax compilation and `git diff --check` pass.
- The implementation diff is limited to the validator, regression suite, and
  current-task evidence.

#### Assumptions

- For mechanically enforceable Superseded closeout, a meaningful reason is any
  nonblank Handoff Log content other than the unchanged stock instructions;
  semantic truth remains a review concern.
- Fenced code follows standard backtick or tilde fences indented by at most
  three spaces; blockquoted headings already cannot match the workflow heading
  syntax.

#### Uncertainties

- This is intentionally a bounded Markdown scanner, not a full CommonMark
  parser. It handles the fenced-code bypass demonstrated by the Reviewer
  without adding a dependency.

#### Review Focus

- Re-run the six malformed fixture classes and attempt variants using tilde
  fences, longer closing fences, duplicate archived sections, and fenced nested
  Review fields.
- Confirm genuine Review blocks containing fenced evidence still validate when
  Verdict and Self-reviewed fields remain outside the fence.
- Check that exact-template validation rejects missing, extra, and duplicate
  structure without rejecting the canonical untouched template.
- Verify no behavior beyond the four required changes was introduced.

#### Recommended Next Action

Review commit `876fe17`, rerun the 28-test suite and full validator, and append
the second independent verdict.

### Session Completion (codex-b, Driver, Revision Round 1)

#### Work completed

Implemented all four required changes from Review round 1, added the reproduced
counterexamples, committed the revision, and returned the turn to the Reviewer.

#### Evidence

Revision commit `876fe17`; seven new regression methods and all 28 tests pass;
full validation, syntax compilation, and diff checks pass.

#### Files changed

`scripts/validate_agent_workflow.py`, `tests/test_agent_workflow.py`, and
`.agents/state/current-task.md`.

#### Tests or experiments run

Reviewer counterexample fixtures, complete unittest discovery, live repository
validation, Python syntax compilation, and whitespace checks.

#### Known limitations

The scanner handles the workflow's ATX headings and fenced code, not the full
CommonMark grammar.

#### Unresolved questions

None blocking the second independent review.

#### Repository state updated

Yes

#### Recommended next action

`codex-a` independently verifies the bounded revision and returns a verdict.

### Review (codex-a, Reviewer, Round 2)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

Revision round 1 fixes all five counterexample classes from the first review.
The 28-test suite passes, the exact-template and duplicate task-section checks
work, backtick and tilde fenced reviews are ignored, and a genuine Review with
fenced evidence remains valid.

Two structured-state bypasses remain:

- `field()` scans raw Role Assignment bodies, so an active task whose Driver,
  Reviewer, and Turn exist only inside a fenced code example is accepted; and
- nested Review fields still silently overwrite duplicates, so a Review with
  `Verdict: Rejected` followed by `Verdict: Accepted` can approve an Accepted
  task.

The same first-match ambiguity also applies to duplicate Driver, Reviewer, or
Turn lines. These cases undermine the structured role and verdict guarantees
that F3 and Task 002 require.

#### Evidence Quality

All 28 repository tests and full validation pass independently. Additional
disposable probes confirmed that tilde-fenced fake reviews fail and legitimate
Reviews containing fenced evidence pass. The fenced-role and duplicate-verdict
fixtures both passed when they should fail.

#### Simplicity

The fence-aware line scanner is appropriately bounded and remains preferable to
a Markdown dependency. Reusing it for role fields and surfacing duplicate
nested fields is a small completion of the existing design.

#### Missing Cases

Coverage lacks role fields inside fences, duplicate role fields, and duplicate
Verdict or Self-reviewed fields.

#### Required Changes

1. Make Role Assignment field extraction fence-aware and reject duplicate
   Driver, Reviewer, or Turn fields instead of choosing one silently.
2. Reject duplicate `#### Verdict` or `#### Self-reviewed` fields in every
   Review block.
3. Add focused regressions for the reproduced cases and rerun the complete
   suite, validator, syntax, and diff checks.

#### Optional Improvements

After acceptance, finalize the audit remediation status and retain the known
limitation that Markdown labels do not authenticate an agent cryptographically.

### Session Completion (codex-a, Reviewer, Round 2)

#### Work completed

Reproduced the seven revision regressions and independently challenged fence
variants, legitimate fenced evidence, nested fields, and role parsing.

#### Evidence

All 28 tests pass; two additional structured-field bypasses remain.

#### Files changed

`.agents/state/current-task.md` only.

#### Tests or experiments run

Full unittest discovery, full validator, diff checks, and disposable tilde
fence, legitimate fenced evidence, duplicate Verdict, fenced role, and invalid
Turn probes.

#### Known limitations

This review did not modify Driver-owned implementation files.

#### Unresolved questions

None. The final revision is limited to structured-field parsing and tests.

#### Repository state updated

Yes

#### Recommended next action

Driver completes the second revision round and returns the branch for the final
allowed acceptance check.

### Handoff (codex-b, Driver, Revision Round 2)

#### Objective

Complete the final allowed revision by closing only the structured Role
Assignment and Review-field bypasses from Review round 2.

#### Changes

- Role Assignment extraction now removes fenced code before reading fields, so
  fenced Driver, Reviewer, or Turn examples cannot supply live state.
- Driver, Reviewer, and Turn are collected explicitly and any duplicate field
  invalidates active and archived task records.
- Every Review block now preserves duplicate-heading metadata and rejects
  duplicate Verdict or Self-reviewed fields, including malformed earlier
  Reviews followed by a valid latest Review.
- Three focused regression methods cover fenced-only and real-plus-fenced role
  fields, all three duplicate role fields, both duplicate Review state fields,
  and the earlier-Review case.

#### Evidence

- Final revision implementation commit:
  `74b73237f57120243a5f0f5a352d9f2f846d90dd`.
- Before the implementation change, the six reproduced field bypass fixtures
  passed validation and all focused assertions failed.
- After the change, all three focused methods and the complete 31-test suite
  pass.
- `python3 scripts/validate_agent_workflow.py` passes with ten routed skills and
  one validated operational archive.
- Syntax compilation and `git diff --check` pass.
- The implementation diff is limited to the validator, focused regressions,
  and current-task evidence.

#### Assumptions

- Role Assignment values and Review state are defined only by visible,
  exact-schema fields; fenced examples are documentation rather than state.
- Duplicate structured state is invalid even when repeated values agree,
  avoiding first-value and last-value ambiguity.

#### Uncertainties

- No blocking uncertainty remains within the three required changes. Markdown
  labels still cannot authenticate authorship cryptographically, as already
  recorded.

#### Review Focus

- Reproduce fenced-only Role Assignment fields and confirm real fields remain
  valid when fenced examples follow them.
- Exercise duplicate Driver, Reviewer, and Turn in both active and archived
  records, including duplicates inside fences that should be ignored.
- Exercise duplicate Verdict and Self-reviewed in the latest and in earlier
  Review blocks, including fenced duplicates that should be ignored.
- Confirm all prior audit, lifecycle, archive, installation, and closeout
  regressions remain green.

#### Recommended Next Action

Review commit `74b7323`, run the final 31-test and validator checks, and append
the final independent verdict. If acceptance is not possible, follow the
two-round rule and escalate to a human rather than requesting a third revision.

### Session Completion (codex-b, Driver, Revision Round 2)

#### Work completed

Implemented the three final required changes, added focused regression
coverage, committed the implementation, and returned the task for the final
allowed acceptance check.

#### Evidence

Final revision commit `74b7323`; three focused methods covering six bypasses;
31/31 tests, full validation, syntax compilation, and diff checks pass.

#### Files changed

`scripts/validate_agent_workflow.py`, `tests/test_agent_workflow.py`, and
`.agents/state/current-task.md`.

#### Tests or experiments run

Focused structured-field regressions, full unittest discovery, live repository
validation, Python syntax compilation, and whitespace checks.

#### Known limitations

Review authorship remains cooperative rather than cryptographically
authenticated; no new limitation was introduced.

#### Unresolved questions

None within the final bounded revision.

#### Repository state updated

Yes

#### Recommended next action

`codex-a` performs the final independent review and records the verdict.

### Review (codex-a, Reviewer, Final)

#### Verdict

Accepted

#### Self-reviewed

No

#### Correctness

All six audited failures are resolved.

- Installation exports tracked files without copying source Git metadata or
  untracked files and documents collision behavior.
- Handoff, Review, and Session Completion entries remain nested under the
  Handoff Log.
- Active and archived state now enforce exact structure, visible unique role
  and Review state fields, verdict/self-review semantics, status/turn pairing,
  terminal archive rules, and matching ids.
- Accepted and non-merge terminal branch closeouts preserve the intended
  implementation boundary.
- Partial, duplicate, fenced, placeholder, and malformed state fixtures fail.
- The illustrative task is outside operational history.

The final revision closes the fenced-role and duplicate nested-field bypasses
without weakening legitimate Reviews that contain fenced evidence.

#### Evidence Quality

The complete 31-test suite passed independently. It includes the original
eleven-case audit matrix, valid active and archive lifecycles, installation Git
metadata preservation, accepted merge closeout, Rejected/Inconclusive/
Superseded metadata-only closeout, and all counterexamples from both review
rounds. The live validator, independent syntax compilation, and diff checks
also pass.

#### Simplicity

The implementation stays within the Python standard library and the existing
Markdown workflow. The bounded fence-aware scanner and explicit state maps are
proportionate to the demonstrated failures; no plugin system, external parser,
or speculative abstraction was added.

#### Missing Cases

No missing case blocks acceptance. The Turn marker remains cooperative and
Markdown labels do not authenticate agent identity; both are documented
non-goals rather than regressions.

#### Required Changes

None.

#### Optional Improvements

During completion, mark the audit remediation as independently accepted and
update repository state so the resolved findings are no longer listed as
current failures.

### Session Completion (codex-a, Reviewer, Final)

#### Work completed

Performed the final independent correctness, regression, API, and simplicity
audit after two bounded revision rounds.

#### Evidence

All 31 tests, live validation, syntax compilation, diff checks, and prior
adversarial fixtures pass.

#### Files changed

`.agents/state/current-task.md` only.

#### Tests or experiments run

Full unittest discovery; live workflow validator; independent syntax
compilation; whitespace checks; tracked-only installation; accepted and
metadata-only closeout; exact-template, duplicate section, fenced Review,
fenced role, duplicate role, duplicate Review state, placeholder, and terminal
status probes.

#### Known limitations

Concurrency locking and cryptographic review authorship remain outside scope.

#### Unresolved questions

None.

#### Repository state updated

Yes

#### Recommended next action

Driver merges the accepted branch, finalizes the audit and repository state,
archives task 002, and runs the completion validation.
