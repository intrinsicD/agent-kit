# Current Task

## Title

Cross-repository agent workflow adoption assessment

## Task ID

003

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: driver

## Mode

Decide

## Goal

Determine whether prospect, structsplat, realtime-gs, and IntrinsicEngine
should adopt or replace their existing agentic workflows with agent-kit, and
identify any workflow mechanisms from those repositories that should be
integrated into agent-kit.

## Motivation

The repositories may have different operating needs and existing coordination
mechanisms. A blanket installation could duplicate, weaken, or conflict with
working repository-specific practices, while useful mechanisms may be missing
from agent-kit.

## Success Criteria

- Inventory workflow-related instructions, state, automation, and history in
  agent-kit and each of the four target repositories.
- Give one evidence-backed disposition per target repository: adopt, replace,
  selectively integrate, or leave unchanged.
- Identify reciprocal integration candidates for agent-kit and distinguish
  required improvements from repository-specific features.
- Document conflicts, migration risks, and the smallest safe next step for
  every recommendation.
- Obtain an independent Reviewer verdict on the evidence and conclusions.

## Constraints

- Treat the four target repositories as read-only.
- Base claims on the current local checkout and record the inspected commit for
  each repository.
- Do not install, replace, or migrate any workflow during this assessment.
- Keep repository observations separate from agent inference.

## Non-Goals

- Implementing recommended migrations.
- Redesigning application code or research methods unrelated to agent
  operation.
- Comparing general-purpose agent products or hosted orchestration platforms.

## Selected Skills

- task-orchestration
- research-methods
- review-and-falsification
- handoff
- repo-organization

## Current Evidence

- Task 002 independently accepted the hardened agent-kit workflow.
- The target repositories have not yet been inventoried in this task.

## Minimal Plan

1. Record the current commit and workflow-related surface of all five
   repositories.
2. Compare authority, roles, state, validation, lifecycle, specialization, and
   migration compatibility.
3. Write a decision-oriented research note with per-repository recommendations
   and reciprocal integration candidates.
4. Commit the evidence and hand it to the Reviewer for independent
   falsification.
5. Address any required revisions, then archive the accepted assessment.

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
