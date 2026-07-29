# Current Task

## Title

Revalidate cross-repository agent workflow adoption

## Task ID

005

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: driver

## Mode

Validate

## Goal

Determine whether workflow changes since Task 003 alter the accepted decision
for Prospect, StructSplat, realtime-gs, IntrinsicEngine, or agent-kit.

## Motivation

The user requested the same cross-repository adoption assessment after Task 003
was accepted and Task 004 removed agent-kit's distribution blocker. The prior
recommendation should be reused only if it remains supported at current
repository heads.

## Success Criteria

- Record current commits and worktree state for all five repositories.
- Compare workflow-related paths against the commits assessed in Task 003 and
  classify every material change.
- Run the smallest relevant existing workflow checks needed to validate current
  behavior.
- Give an evidence-backed add, replace, bounded-pilot, or no-change disposition
  for each target and for candidate imports into agent-kit.
- Obtain an independent Reviewer verdict before promoting the conclusion.

## Constraints

- Keep Prospect, StructSplat, realtime-gs, and IntrinsicEngine read-only.
- Preserve all existing tracked and untracked user work.
- Treat checked-in workflow files and executable checks as authority.
- Do not infer workflow adoption merely because agent-kit is now safe to
  distribute.

## Non-Goals

- Installing, replacing, or migrating any target workflow.
- Auditing domain algorithms, research results, or product architecture except
  where they directly define workflow requirements.
- Designing a generalized cross-repository workflow platform.

## Selected Skills

- `task-orchestration`
- `research-methods`
- `handoff`
- `review-and-falsification`
- `repo-organization`

## Current Evidence

Task 003 independently accepted a no-wholesale-adoption conclusion at Prospect
`537966bf`, StructSplat `ebf860bc`, realtime-gs `dd84c28d`, and IntrinsicEngine
`5f7843c9`. Task 004 then made agent-kit distribution collision-safe without
authorizing installation into those repositories.

## Minimal Plan

1. Diff current workflow surfaces from the Task 003 baselines and inspect only
   relevant changed authority, state, skill, checker, and CI files.
2. Re-run bounded native workflow checks and update the existing research note
   with current evidence and dispositions.
3. Self-audit, commit, and hand the fixed commit to the independent Reviewer.
4. Resolve the verdict and complete repository state through the documented
   closeout flow.

## Status

In progress

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
