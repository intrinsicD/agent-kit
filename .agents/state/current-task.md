# Current Task

## Title

Audit the two-agent workflow for correctness and failure modes

## Task ID

001

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: driver

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

## Minimal Plan

1. Inspect every workflow source of truth and map the documented lifecycle.
2. Run the validator and targeted fixtures for state-transition edge cases.
3. Record only demonstrated or directly traceable problems in a durable audit.
4. Commit and hand the fixed branch state to the independent Reviewer.

## Status

In progress

## Human Decisions

None.

## Handoff Log

No handoff yet.
