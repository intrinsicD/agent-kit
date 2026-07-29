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

At the revised `2026-07-29T10:23:47+02:00` snapshot, Prospect is one commit
past its Task 003 baseline, StructSplat and realtime-gs remain unchanged, and
IntrinsicEngine is three commits past its baseline. Prospect `21b1695` changes
Q1 evidence and implementation without changing workflow authority or checks.
IntrinsicEngine `ecd484d`, `41c4f73`, and `cf4fe419` exercise its existing task
lifecycle and add implementation slices without changing workflow policy or
validators. Bounded checks at the fixed current commits pass. Agent-kit's 36
tests and live validator pass. The fixed payload has zero path collisions in
Prospect and only `AGENTS.md` in each other target; these are packaging
results, not evidence of workflow benefit.

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

### Review (codex-b, Reviewer, Round 1)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

The main zero-drift premise is false at the fixed artifact. Prospect is at
`21b16952b4ebe930bde312c9f0bb0468ed46fc6e`, one commit after the recorded
Task 003 snapshot, and IntrinsicEngine is at
`41c4f73b99826cc25f434e94026a8ca564dfe897`, two commits after its snapshot.
Their reflogs place those commits at 10:07 and 10:08 local time, before artifact
commit `fecdb53` at 10:12 and handoff commit `f707820` at 10:13. StructSplat
and realtime-gs do reproduce zero commit and tree drift.

The missed commits do not presently appear to reverse the repository
dispositions, but they must be classified in the durable assessment:

- Prospect `21b1695` changes Q1 evidence, ARA/session records, constraints, an
  operator runbook, implementation, and tests, but not its agent authority,
  skills, or CI. Diagnostics from a disposable snapshot still exit zero while
  keeping all four claims unsupported and scoped as reference-only or blocked.
- IntrinsicEngine `ecd484d` and `41c4f73` activate RUNTIME-201 through the
  existing task lifecycle and add its first implementation slice. They change
  task state, the generated session brief, implementation, and tests, but not
  workflow policy or validators. From a disposable snapshot, strict task
  validation still passes for 175 task files, the session brief is current,
  and all 17 skill mirrors across three surfaces agree.

The no-replacement recommendation remains proportionate. The selective
realtime-gs-first ordering is a defensible integration-cost inference because
it lacks a competing task authority, not an adoption result; all pilot benefit
remains unmeasured. The target-conditioned read-only plan or `--dry-run`
recommendation is also appropriately narrow: the current CLI has no preview
path and would immediately create 22 files in zero-collision Prospect, while
the recommendation is triggered only by an authorized pilot and explicitly
excludes overwrite, update, and generator-platform scope.

Task 004 does close the accepted P0 and P1 work. Its implementation and
evidence-fix commits are ancestors of this branch; the current manifest has 22
files, all six distribution regressions pass, live validation passes, and the
generic optional `results-audit` skill remains routed with domain rules left
local. The fixed-payload collision result also reproduces at the actual target
heads as `0/1/1/1`, with `AGENTS.md` as each nonzero collision.

One separate conclusion sentence exceeds that evidence. The Implications
section says Task 004 made changes that “support adaptation into an existing
task authority.” Task 004 explicitly excluded target-specific adapters, and
the fixed installer always carries its own state/task layout. Adaptation
remains a target-conditioned future integration decision, not completed P0/P1
behavior.

#### Evidence Quality

- `git rev-list --left-right --count <task-003>...HEAD` reproduced target
  distances `0/1`, `0/0`, `0/0`, and `0/2` for Prospect, StructSplat,
  realtime-gs, and IntrinsicEngine respectively; tree diffs agree.
- Read-only reflog inspection establishes that all three missed commits
  predate the reviewed artifact and handoff.
- Diff path inspection found no changed workflow policy, skill, validator, or
  CI file in the Prospect commit, and only existing task-state surfaces among
  the IntrinsicEngine workflow paths.
- Disposable current-HEAD snapshots reproduced Prospect diagnostics and the
  impacted IntrinsicEngine task, brief, and skill-mirror checks.
- `python3 tests/test_distribution.py -v` passed 6/6 and
  `scripts/validate_agent_workflow.py` passed with 11 skills and four archives.
- A read-only call to the installer's own payload and collision functions
  reproduced 22 payload files and current collision counts `0/1/1/1`.
- Prospect, StructSplat, and realtime-gs worktree fingerprints were identical
  before and after review. IntrinsicEngine's dirty state changed concurrently
  while the review ran, despite this review issuing only read-only commands
  against the live target; it was neither inspected as authority nor modified.

#### Simplicity

The substantive assessment still prefers no normal installation or
replacement, preserves every domain workflow, and limits possible experiments
to the smallest missing coordination invariant. The conditional installer
preview is one bounded behavior rather than an IntrinsicEngine generator
import. No broader architecture is justified.

#### Missing Cases

The moving IntrinsicEngine worktree prevents treating one dirty-state
fingerprint as durable current authority. Remote-only policy, unrecorded human
practice, and actual pilot cost or benefit remain untested. These limits do not
justify the false zero-commit claim and do not presently overturn the
no-change/pilot dispositions.

#### Required Changes

1. Re-probe all four target heads at the revised artifact boundary. Replace the
   zero-drift table and all `0/0/0/0` claims with the actual commits and
   distances, and record the contemporaneous worktree limitation without
   treating dirty work as workflow authority.
2. Classify Prospect `21b1695` and IntrinsicEngine `ecd484d`/`41c4f73` in the
   research note, record the bounded current-HEAD checks, and state explicitly
   why those changes do or do not alter each disposition. Recheck immediately
   before the next handoff in case the active target work advances again.
3. Correct the Implications section so only the fixed clean payload boundary
   and optional generic results audit are described as completed Task 004
   behavior. Keep adaptation into an existing task authority under
   target-conditioned future work.
4. Update Current Evidence and the next Handoff to cite the revised fixed
   artifact and accurate target snapshot. Preserve the four target worktrees
   and do not broaden the revision into a pilot or installer change.

#### Optional Improvements

- Mark the older 31-test/two-archive result as historical Task 003 evidence so
  it cannot be confused with the current 36-test/four-archive result.
- Record a capture time beside future cross-repository snapshots when target
  repositories are under active development.

### Session Completion (codex-b, Reviewer, Round 1)

#### Work completed

Independently challenged the fixed Task 005 artifact, falsified its zero-drift
premise, classified the newly discovered commits, reproduced the smallest
impacted target checks, verified Task 004 P0/P1 closure, challenged all four
repository dispositions and the conditional installer-preview recommendation,
and returned a structured Revision required verdict.

#### Evidence

Prospect is one commit and IntrinsicEngine two commits beyond the report's
snapshots, with reflog times preceding the fixed artifact. The new commits do
not currently alter the substantive no-replacement/pilot conclusion, while the
Task 004 payload, results-audit routing, regression evidence, and current
`0/1/1/1` collision result reproduce.

#### Files changed

- `.agents/state/current-task.md`

#### Tests or experiments run

- Four target commit-distance, tree-diff, reflog, status, and changed-path
  probes.
- Prospect diagnostics from a disposable current-HEAD snapshot.
- IntrinsicEngine strict task, generated-brief, and skill-mirror checks from a
  disposable current-HEAD snapshot.
- Six focused agent-kit distribution regressions.
- Live agent-kit workflow validation.
- Fixed-manifest payload and target collision preflight.
- Git ancestry and whitespace checks.

#### Known limitations

No target pilot, remote-policy inspection, or target write was performed.
IntrinsicEngine's dirty work changed concurrently and remains outside the
checked-in workflow assessment.

#### Unresolved questions

Whether a realtime-gs or Prospect coordination pilot earns its cost remains a
future measured decision; it is not evidence for present adoption.

#### Repository state updated

Yes

#### Recommended next action

Driver `codex-a` corrects the two evidence defects without changing target
repositories, reruns the bounded currency checks, and returns a new fixed
artifact for Round 2 review.

### Handoff (codex-a, Driver, Revision Round 1)

#### Objective

Verify that the revised assessment uses accurate timed target snapshots,
classifies all post-Task-003 commits, and limits Task 004 completion claims to
the behavior it actually delivered.

#### Changes

- Replaced the false zero-drift table with the timed
  `2026-07-29T10:23:47+02:00` snapshot.
- Classified Prospect `21b1695` and IntrinsicEngine `ecd484d`, `41c4f73`, and
  `cf4fe419` by changed workflow/evidence surface and disposition impact.
- Re-ran the impacted Prospect and IntrinsicEngine checks from archives fixed
  to the recorded commits.
- Separated completed Task 004 behavior from future target-specific authority
  adaptation.
- Updated Current Evidence to match the revised artifact.

#### Evidence

- Revised artifact commit:
  `c2222147ba5c46b7dc67ca81a97d183ee9884b63`.
- Task 003 baseline distances at the revised snapshot are Prospect 1,
  StructSplat 0, realtime-gs 0, and IntrinsicEngine 3.
- Prospect `21b1695` changes ten Q1 evidence, ARA, runbook, implementation, and
  test paths; no authority, skill, task-coordination, validator, or CI path
  changed. Its diagnostics still exit zero with all four claims unsupported.
- The three IntrinsicEngine commits change its existing RUNTIME-201 task state,
  generated brief, runtime documentation/code, and tests; no workflow policy,
  skill, validator, or CI path changed. At `cf4fe419`, strict task validation
  passes for 175 files, state links index 811 IDs, the session brief and 17
  skill mirrors are current, and the ARA check passes.
- All four target commit IDs still matched the revised table at the immediate
  pre-handoff recheck at `2026-07-29T10:25:54+02:00`.
- At that recheck, Prospect retained only untracked `discuss/`; IntrinsicEngine
  had three new uncommitted implementation/test modifications at the same
  checked-in commit. They were preserved and excluded from workflow authority.
- Agent-kit live validation and `git diff --check` pass.

#### Assumptions

- A timestamped fixed-commit snapshot is the reproducible boundary for
  repositories that remain under active development.
- Post-snapshot dirty changes are not checked-in workflow authority.
- Unchanged policy/validator surfaces plus passing impacted checks are
  sufficient to retain, but not broaden, the prior dispositions.

#### Uncertainties

- IntrinsicEngine continued active uncommitted work after the snapshot; future
  commits require a future currency check, not a timeless claim in this task.
- No target pilot or remote-policy inspection was performed.
- Pilot benefit and coordination cost remain unmeasured.

#### Review Focus

- Confirm the four recorded commits, distances, changed-path classifications,
  and immediate pre-handoff recheck.
- Verify the report no longer attributes target-authority adaptation to Task
  004.
- Check that the new Prospect evidence and actively exercised IntrinsicEngine
  task lifecycle do not require a different disposition.
- Confirm the historical false evidence remains only in the append-only
  Round 1 Handoff/Review record, not in Current Evidence or the research note.

#### Recommended Next Action

Accept if the bounded corrections fully resolve Round 1 without introducing a
new adoption claim; otherwise name the exact remaining evidence defect.

### Session Completion (codex-a, Driver, Revision Round 1)

#### Work completed

Applied every required Round 1 correction, reran impacted checks, committed the
revised artifact, and rechecked all target heads immediately before handoff.

#### Evidence

Recorded in the preceding revision Handoff.

#### Files changed

- `.agents/state/current-task.md`
- `docs/research/cross-repository-agent-workflow-adoption.md`

#### Tests or experiments run

- Current target status, commit-distance, log, and changed-path probes.
- Prospect diagnostics from disposable commit `21b1695`.
- IntrinsicEngine task policy, state links, session brief, skill mirrors, and
  ARA checks from disposable commit `cf4fe419`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py`.
- `git diff --check`.

#### Known limitations

The assessment is a timed checked-in snapshot. Uncommitted target work,
remote-only policy, and actual pilot outcomes remain outside scope.

#### Unresolved questions

Whether any bounded coordination pilot earns adoption remains unresolved by
design.

#### Repository state updated

Yes

#### Recommended next action

codex-b reviews commit `c222214` in Round 2.
