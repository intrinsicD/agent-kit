# Current Task

## Title

Revalidate cross-repository agent workflow adoption

## Task ID

005

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: reviewer

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

All four target `HEAD`s remain exactly at the Task 003 commits. Checks rerun
from disposable committed snapshots passed: Prospect diagnostics, StructSplat
structural checks and 8 tests, realtime-gs structural checks and 12 tests, and
IntrinsicEngine task/state/brief/skill/ARA checks plus its generator self-test.
Agent-kit's 36 tests and live validator pass. The fixed payload currently has
zero path collisions in Prospect and only `AGENTS.md` in each other target;
these are packaging results, not evidence of workflow benefit.

## Minimal Plan

1. Diff current workflow surfaces from the Task 003 baselines and inspect only
   relevant changed authority, state, skill, checker, and CI files.
2. Re-run bounded native workflow checks and update the existing research note
   with current evidence and dispositions.
3. Self-audit, commit, and hand the fixed commit to the independent Reviewer.
4. Resolve the verdict and complete repository state through the documented
   closeout flow.

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

Independently falsify whether current repository evidence still supports the
Task 003 adoption dispositions after Task 004 closed agent-kit's distribution
blocker.

#### Changes

- Updated the existing cross-repository research note rather than creating a
  duplicate assessment.
- Recorded the zero-commit drift result for all four targets and current
  worktree limitations.
- Reproduced bounded target workflow checks from disposable committed
  snapshots.
- Distinguished fixed-payload collision safety from target workflow fit.
- Marked Task 003 P0 and P1 recommendations completed by Task 004 and added one
  target-conditioned `--dry-run` hypothesis for an authorized pilot.

#### Evidence

- Reviewed artifact commit: `fecdb531eaf6966b80ed592846ca721de69a8bc1`.
- Target commit distances from the Task 003 snapshots: 0/0/0/0.
- Prospect diagnostics exited zero with unsupported claims still scoped as
  reference-only or blocked.
- StructSplat structural checks passed and focused tests passed 8/8.
- realtime-gs structural checks passed and focused tests passed 12/12.
- IntrinsicEngine validated 175 task files and 811 task IDs; session brief,
  skill mirror, ARA, and generator self-test checks passed.
- agent-kit passed all 36 tests and live workflow validation.
- Current fixed-payload preflight collision counts are Prospect 0, StructSplat
  1, realtime-gs 1, and IntrinsicEngine 1; each nonzero collision is
  `AGENTS.md`.
- `git diff --check` passed.

#### Assumptions

- Checked-in local workflow files remain the relevant authority.
- Zero target commit drift permits reuse of the independently accepted Task 003
  semantic inspection.
- Safe packaging does not establish target benefit, proportionality, or
  adoption priority.

#### Uncertainties

- Prospect and IntrinsicEngine have preserved uncommitted work that was not
  treated as workflow authority.
- Remote-only policy and unrecorded human practice remain outside scope.
- No pilot has measured coordination cost, duplicate state, handoff
  reconstruction, or material defects found.
- The proposed installer preview is a bounded safety inference; its value
  should be challenged rather than assumed.

#### Review Focus

- Verify every target `HEAD` equals its Task 003 snapshot and no committed
  workflow drift was missed.
- Challenge whether Task 004 actually closes P0 and P1 without authorizing
  adoption.
- Attempt to falsify the per-repository dispositions, especially the ordering
  of realtime-gs before Prospect.
- Decide whether `--dry-run` is justified by the zero-collision Prospect
  preflight or should remain omitted.
- Confirm target working trees were preserved and the report clearly separates
  historical tracked-tree collisions from current fixed-payload collisions.

#### Recommended Next Action

Return an evidence-based verdict. Require revision if any conclusion exceeds
the unchanged repository evidence or if the optional preview recommendation is
not justified.

### Session Completion (codex-a, Driver)

#### Work completed

Completed the currency check, updated the durable assessment, self-audited its
scope, and prepared the fixed commit for independent review.

#### Evidence

Recorded in the preceding Handoff and in the updated research note.

#### Files changed

- `.agents/state/current-task.md`
- `docs/research/cross-repository-agent-workflow-adoption.md`

#### Tests or experiments run

- Four target commit-distance and worktree probes.
- Disposable target workflow checks listed in the Handoff.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
  -p 'test_*.py' -v`: 36/36 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py`:
  passed.
- Fixed-manifest collision preflight against all four targets.
- `git diff --check`: passed.

#### Known limitations

No target pilot or remote-policy inspection was performed. Dirty target work
was preserved and excluded from checked-in workflow conclusions.

#### Unresolved questions

Whether a realtime-gs or Prospect pilot earns its coordination cost remains
unresolved by design.

#### Repository state updated

Yes

#### Recommended next action

codex-b independently reviews commit `fecdb53` and records a verdict.
