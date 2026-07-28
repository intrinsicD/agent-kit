# Current Task

## Title

Audit the two-agent workflow for correctness and failure modes

## Task ID

001

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: reviewer

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

In review

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
