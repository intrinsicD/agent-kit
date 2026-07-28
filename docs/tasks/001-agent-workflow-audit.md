# Current Task

## Title

Audit the two-agent workflow for correctness and failure modes

## Task ID

001

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: none

## Mode

Validate

## Goal

Determine whether the repository's agentic workflow is internally consistent,
executable as documented, and protected against likely coordination and state
corruption failures.

## Motivation

The user requested a repository review focused on problems in the agentic
workflow.

## Success Criteria

- Run the existing workflow validator on both the clean repository and targeted
  malformed-state fixtures.
- Trace the documented task lifecycle from initialization through review and
  completion, checking rules against templates, skills, and validator behavior.
- Record prioritized, line-specific findings with reproducible evidence and
  concrete remediation guidance in `docs/audits/`.
- Obtain an independent Reviewer verdict that attempts to falsify the Driver's
  findings.

## Constraints

- Run one agent at a time in the shared working tree.
- Review only the workflow; do not implement fixes beyond audit/task records.
- Prefer executable checks over purely textual concerns.

## Non-Goals

- Redesigning the workflow.
- Changing product code, dependencies, or public interfaces.
- Treating hypothetical feature requests as defects.

## Selected Skills

- task-orchestration
- handoff
- review-and-falsification
- repo-organization

## Current Evidence

- The repository begins on `main` with a clean worktree.
- `.agents/state/state.md` and `.agents/state/current-task.md` were unfilled
  templates.
- `docs/tasks/000-example-task.md` is explicitly illustrative, so no real
  previous role assignment exists to swap.
- The baseline validator passes and reports ten skills plus one archived task.
- A disposable install probe showed the README command replacing the target
  repository's remote, branch, and HEAD with this kit's Git metadata.
- Eleven targeted validator fixtures produced eleven protocol/validator
  mismatches.
- Durable findings are recorded in
  `docs/audits/agent-workflow-audit.md` at commit `24c73c2`.

## Minimal Plan

1. Inspect every workflow source of truth and map the documented lifecycle.
2. Run the validator and targeted fixtures for state-transition edge cases.
3. Record only demonstrated or directly traceable problems in a durable audit.
4. Commit and hand the fixed branch state to the independent Reviewer.

## Status

Accepted with follow-up

## Human Decisions

None.

## Handoff Log

### Handoff (codex-a, Driver)

#### Objective

Determine whether the two-agent workflow is safe to install, internally
consistent, and mechanically protected against invalid task states.

#### Changes

- Added `docs/audits/agent-workflow-audit.md`.
- No workflow implementation or dependency changes were made.

#### Evidence

- Baseline: `python3 scripts/validate_agent_workflow.py` passes.
- Syntax: `python3 -m py_compile scripts/validate_agent_workflow.py` passes.
- Installation probe: the documented `cp -r agent-kit/. target-repository/`
  changed a disposable target's remote, active branch, and HEAD.
- Validator matrix: one documented valid review form was rejected; ten
  protocol-invalid active/archive states were accepted.
- Reviewed commit: `24c73c2`.

#### Assumptions

- An installation command must preserve an existing target's `.git/`.
- Accepted work must have an independent review unless its status remains
  explicitly provisional.
- Archived rejection records must reach the default branch without rejected
  implementation changes.

#### Uncertainties

- The intended status/turn transition table is implied rather than written
  explicitly.
- A selective cherry-pick could close rejected branches, but the repository
  does not currently define that procedure.

#### Review Focus

- Reproduce F1 and F2 independently.
- Try to construct a documented completion path that falsifies F4.
- Challenge the severity of F3-F6 and check for missing counterexamples.
- Verify all source locations and the eleven-case fixture accounting.

#### Recommended Next Action

Return an independent verdict with required versus optional changes.

### Review (codex-b, Reviewer)

#### Verdict

Accepted with follow-up

#### Self-reviewed

No.

#### Correctness

All six findings are supported by the cited workflow sources and observed
behavior.

- F1 reproduced in a disposable target: the documented copy command replaced
  its remote, active branch, and HEAD with the source repository's values and
  copied an untracked marker.
- F2 reproduced with a minimal accepted-task fixture: the skills' level-two
  `## Review` form failed validation, while the example's level-three form
  passed.
- The stated eleven-case accounting reproduced exactly: one documented valid
  state was rejected and all ten protocol-invalid states were accepted.
- F4 resisted falsification. Archiving on the rejected task branch left the
  default branch without the archive; merging that branch transferred both the
  archive and the rejected implementation. No documented third path was found.
- F5 and F6 follow directly from the validator's title-only active-state check,
  archive filename-only checks, and the unqualified fallback to the illustrative
  task record.

#### Evidence Quality

The important claims were reproduced independently from reviewed commit
`24c73c2`, not inferred from the Driver's prose. The baseline validator and
syntax check passed. Source line references for F1-F6 match the current files.
The fixture matrix isolated one condition per case and returned eleven of
eleven claimed mismatches.

#### Simplicity

The audit stays focused on six demonstrated workflow failures and recommends
local schema, validation, installation, and lifecycle corrections rather than a
redesign. The proposed fixes are proportionate to the evidence.

#### Missing Cases

No missing case changes the assessment. Two additional manifestations fit the
existing findings: the handoff skill's level-two `## Session Completion` also
escapes the Handoff Log, and other non-verdict text can satisfy the validator's
broad Review-heading regex. These should be covered when F2/F3 fixtures are
added.

#### Required Changes

None.

#### Optional Improvements

Qualify F4's “impossible choice” as “no documented safe path when a task branch
contains rejected changes.” Git can support a selective closeout, as the audit
already notes; the defect is that the workflow neither defines nor tests one.
The High severity remains reasonable because a literal completion attempt can
either lose durable negative evidence or merge rejected work.

### Session Completion (codex-b)

#### Work completed

Independent falsification review of F1-F6 and the eleven-case fixture matrix.

#### Evidence

Baseline validation, syntax compilation, disposable installation probe,
eleven-case validator matrix, source citation check, and rejected-branch
completion probe.

#### Files changed

`.agents/state/current-task.md` only.

#### Tests or experiments run

`python3 scripts/validate_agent_workflow.py`,
`python3 -m py_compile scripts/validate_agent_workflow.py`, and disposable
Python/Git probes for F1, F2/F3/F5, and F4.

#### Known limitations

The audit recommends fixes but this task intentionally did not implement them.

#### Unresolved questions

None blocking.

#### Repository state updated

Yes.

#### Recommended next action

Driver merges the reviewed audit, performs the `repo-organization` completion
update, and then addresses F1-F4 before recommending adoption.

### Session Completion (codex-a, Driver)

#### Work completed

Merged the independently reviewed audit and completed the repository state and
task archive updates.

#### Evidence

Independent verdict `Accepted with follow-up` at commit `cf05986`; audit merged
to `main`.

#### Files changed

- `docs/audits/agent-workflow-audit.md`
- `docs/tasks/001-agent-workflow-audit.md`
- `.agents/state/state.md`
- `.agents/state/current-task.md`

#### Tests or experiments run

`python3 scripts/validate_agent_workflow.py`, `git diff --check`, and an exact
comparison of this archive against the reviewed active-task record except for
the required `Turn: none` change.

#### Known limitations

This task reviewed and recorded the workflow failures; it did not implement the
recommended fixes.

#### Unresolved questions

None blocking. F1-F4 remain adoption blockers.

#### Repository state updated

Yes.

#### Recommended next action

Fix the installation command before distributing the kit.
