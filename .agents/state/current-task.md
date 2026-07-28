# Current Task

## Title

Cross-repository agent workflow adoption assessment

## Task ID

003

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: reviewer

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
- The assessment is committed at `4576828`.
- The documented archive installer has 11 exact path collisions with
  prospect, 12 with structsplat, 11 with realtime-gs, and 12 with
  IntrinsicEngine, and would also copy non-colliding agent-kit task/ARA
  history.
- StructSplat's structural workflow checks and seven regression tests pass.
- realtime-gs's structural checks and 12 workflow-checker tests pass.
- IntrinsicEngine's task policy, 811-ID state links, generated brief, skill
  mirrors, ARA checker, and portable agentkit self-test pass.
- Prospect's diagnostic gate runs and explicitly refuses unsupported
  capability claims.

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

### Handoff (codex-a, Driver)

#### Objective

Independently falsify the cross-repository adoption assessment and determine
whether its deployment blocker, per-repository dispositions, and reverse
integration priorities follow from the inspected repositories.

#### Changes

- Added
  `docs/research/cross-repository-agent-workflow-adoption.md`.
- Indexed the note from `docs/research/README.md`.
- Recorded the current commit and working-tree condition of all five
  repositories.
- Compared authority, task state, independent review, evidence discipline,
  validation, CI, migration compatibility, and process proportionality.

#### Evidence

- Reviewed artifact commit: `4576828`.
- agent-kit: 31/31 workflow tests and live validation pass.
- Prospect: `make epistemic-diagnostics` exits zero while correctly retaining
  `claim_supported: false` dispositions.
- StructSplat: docs, ARA, task, and script structural checks pass; workflow
  checker tests pass 7/7.
- realtime-gs: docs, ARA, and script checks pass; workflow checker tests pass
  12/12 with `PYTHONPATH=src`.
- IntrinsicEngine: strict task policy, task state links, generated session
  brief, skill mirrors, and ARA checks pass; its agentkit disposable-repository
  self-test passes.
- Direct installation collision preflight counts are recorded in the report.

#### Assumptions

- Checked-in local workflow files are the available authority.
- The target ARA and task histories must not be overwritten or renumbered.
- The intended operating topology remains two cooperating agents.

#### Uncertainties

- Private branch protection, issue trackers, and unrecorded human practices
  were not inspected.
- The cost of mandatory independent review in Prospect and realtime-gs needs a
  pilot.
- The report recommends adapting IntrinsicEngine's generator model; it does not
  yet prove which implementation should be ported or rewritten.

#### Review Focus

- Reproduce the archive collision/history-contamination finding independently.
- Search a meaningfully different path through each target, especially recent
  process tasks, CI, or history that could contradict the report.
- Challenge whether realtime-gs and Prospect need the full coordination
  profile or only selected invariants.
- Check whether StructSplat or IntrinsicEngine already enforce independent
  per-task approval in a surface the Driver missed.
- Separate required agent-kit changes from attractive but nonessential imports.

#### Recommended Next Action

Return an evidence-based verdict. Required corrections should name the report
section and the contradictory repository evidence.

### Session Completion (codex-a, Driver)

#### Work completed

Completed the five-repository workflow inventory, executable structural probes,
adoption matrix, reverse-integration ranking, migration risks, and smallest
safe adoption sequence.

#### Evidence

Commit `4576828` plus the command results summarized in the handoff.

#### Files changed

- `docs/research/cross-repository-agent-workflow-adoption.md`
- `docs/research/README.md`
- `.agents/state/current-task.md`

#### Tests or experiments run

- agent-kit: 31 workflow regression tests and live validator.
- Prospect: epistemic diagnostic gate.
- StructSplat: four structural checks and seven workflow-checker tests.
- realtime-gs: three structural checks and 12 workflow-checker tests.
- IntrinsicEngine: five structural/state checks and the agentkit self-test.
- Four direct collision-preflight probes.

#### Known limitations

No target repository was modified, no remote-only policy was inspected, and no
adoption pilot was run.

#### Unresolved questions

Whether the target-specific review threshold should cover every substantial
task or only high-risk classes remains a pilot/policy question.

#### Repository state updated

Yes

#### Recommended next action

Reviewer independently falsifies the assessment at commit `4576828`.
