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

### Review (codex-b, Reviewer, Round 1)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

The central negative conclusion is correct: the documented tracked-tree
installer is not a safe distribution boundary, none of the four target
workflows should be replaced wholesale, and existing task, evidence, and
domain-specific authorities must remain authoritative.

The adoption strengths and priorities do not yet follow from the evidence.
Prospect and realtime-gs both lack validator-enforced author/reviewer identity,
but recent history shows durable non-author/referee handoffs that found real
defects. That is a narrower gap than "missing independent review" and does not
by itself establish `High`/`Highest` adoption priority or justify moving from a
pilot to an adoption decision. StructSplat and IntrinsicEngine likewise record
review practices without enforcing identity separation. The report needs to
distinguish a review norm, a recorded reviewer label, and mechanically enforced
independence before ranking the repositories.

The P0/P1 split is also too broad. Clean packaging plus a disposable proof that
blank state is emitted and development history is excluded is the reproduced
deployment blocker. Skill prefixing, authority redirects, and target CI wiring
may be useful, but the report does not demonstrate a live multi-repository
skill collision or show that each is required before a safe pilot. An
"optional CI gate" cannot simultaneously be a universal P0 deployment
requirement.

#### Evidence Quality

- Against source commit `d8d6495`, direct tracked-path intersections reproduced
  the report's exact collision counts: Prospect 11, StructSplat 12, realtime-gs
  11, and IntrinsicEngine 12.
- `git archive d8d6495` contains agent-kit's active state, both completed task
  archives, audit, workflow test, and dated ARA sessions. A tracked-set
  difference confirmed the same non-colliding development-history paths would
  be added to every target.
- Prospect history `e41b22e` -> `bde6266` records a handoff to a next
  non-author reviewer and a third adversarial review; earlier non-author
  reviews found blocking defects. Its Q1 schema still accepts any nonempty
  reviewer string and cannot enforce identity separation.
- realtime-gs history `095313d` -> `ca11378` records a separate fresh-workspace
  scientist pass, with a different Git author and a machine-readable audit,
  before claims C25-C27 were promoted. Its results-audit skill requires a
  referee stance, but no task/state validator binds reviewer identity.
- StructSplat's FIT-042 acceptance criteria require an independent artifact
  audit, and completed FIT-043 records an independent cold audit. Its task
  checker does not require proposer/reviewer identities or a terminal review
  verdict.
- IntrinsicEngine's RUNTIME-190 clean-workshop record names `Reviewer: Codex`,
  and its role guide assigns a Review Agent before merge. The root task
  sequence nevertheless ends in self-review, and the clean-workshop guide says
  that scorecard is not a per-PR blocker; no validator enforces identity
  separation.
- agent-kit's 31 workflow regression tests and live validator pass on the
  reviewed branch.
- The four target working trees remained unchanged from their recorded initial
  states.

These observations support a narrow independent-identity enforcement gap. They
do not supply measured coordination failures, duplicate-state incidents, or
process-cost baselines sufficient to rank full-profile adoption.

#### Simplicity

The smallest evidenced P0 is an explicit clean payload boundary with blank
project state, collision refusal, development-history exclusions, and a
disposable-repository test. A broad configurable generator may be a valid
implementation, but target naming, harness selection, verification-command
configuration, overwrite support, authority mirroring, skill renaming, and CI
injection should not all be precommitted as one deployment blocker.

Several P1 imports are derived only from IntrinsicEngine and have no recorded
agent-kit failure or measured process cost. Maturity vocabulary, periodic
cross-task audits, and a micro-task profile should remain optional hypotheses
or P2 candidates unless the revision supplies independent evidence for their
current priority. The three-repository results-audit pattern has stronger
support and can remain the leading P1 candidate.

#### Missing Cases

- The report does not separate normative review language, observed
  non-author/reviewer practice, and validator-enforced identity.
- It gives no observed coordination failure or pilot result supporting the
  `High`/`Highest` Prospect and realtime-gs rankings.
- It does not reproduce a live skill-name collision, despite treating skill
  prefixing as universally deployment-blocking.
- The central collision result lacks the exact tracked-set/preflight command,
  making its exact counts harder to reproduce from the note alone.
- The decision table says "adopt" while the body and safe sequence require a
  pilot before wider adoption.

#### Required Changes

1. Add the exact deterministic collision/preflight method, source commit, and
   enough command detail to reproduce both the four counts and the
   non-colliding history payload.
2. Revise the per-repository review inventory to distinguish review norms,
   recorded reviewer practice, and enforced identity separation. Incorporate
   the recent Prospect, realtime-gs, StructSplat, and IntrinsicEngine evidence
   above.
3. Reconcile the Prospect/realtime-gs decision-table dispositions and priority
   labels with the unresolved pilot. Either recommend a selective pilot, or
   provide evidence that supports an adoption decision and the relative
   `High`/`Highest` ranking. Keep observations separate from that inference.
4. Restrict universal P0 to the evidenced distribution boundary and its
   disposable no-history/collision regression. Reclassify authority redirects,
   skill prefixing, and CI integration as target-conditioned requirements or
   follow-ups unless additional evidence proves they block every safe pilot.
5. Demote the single-source, unmeasured IntrinsicEngine-derived additions from
   P1 to optional hypotheses/P2, or tie each to an observed agent-kit failure
   and a falsifiable adoption criterion. Avoid building a platform from one
   implementation.
6. Make the Decision Summary, repository recommendations, P0/P1 list, and
   Smallest Safe Adoption Sequence use one consistent adopt-versus-pilot
   decision.

#### Optional Improvements

- Add a compact matrix with columns for review trigger, persisted evidence,
  distinct identity recorded, and distinct identity enforced.
- Name the minimal coordination invariant proposed for each target instead of
  referring to a single "clean coordination profile" whose contents vary by
  repository.

### Session Completion (codex-b, Reviewer, Round 1)

#### Work completed

Independently reviewed commit `4576828`, reproduced the distribution finding,
inspected a distinct recent workflow path in every target, searched for
overlooked review enforcement, and challenged the repository dispositions and
reverse-integration priorities.

#### Evidence

Exact collision counts and non-colliding history contamination were reproduced
from tracked sets and the archive payload. Recent review/task history was
checked at Prospect `e41b22e`/`bde6266`, realtime-gs
`095313d`/`ca11378`, StructSplat FIT-042/FIT-043, and IntrinsicEngine
RUNTIME-190/RUNTIME-191.

#### Files changed

- `.agents/state/current-task.md`

#### Tests or experiments run

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`:
  31/31 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py`:
  passed with 10 skills and two archived tasks.
- Four tracked-path collision probes and four history-payload difference
  probes.
- Read-only Git history, policy, task, audit, and review inspection in all four
  targets.

#### Known limitations

No remote-only branch protection, issue tracker, or unrecorded human practice
was inspected. Heavy target test suites were not rerun because the review
question was workflow evidence and every target was kept read-only.

#### Unresolved questions

The operational cost and defect-detection benefit of adding task-level
Driver/Reviewer turns to Prospect or realtime-gs remain unmeasured and require
a pilot rather than an adoption claim.

#### Repository state updated

Yes

#### Recommended next action

Driver makes the six bounded report revisions and returns the same artifact for
a second independent review.

### Handoff (codex-a, Driver, Revision Round 1)

#### Objective

Verify that the revised assessment now distinguishes observed review practice
from mechanical enforcement, limits universal P0 to the reproduced
distribution failure, and consistently recommends experiments rather than
unsupported adoption.

#### Changes

- Added the exact source commit and deterministic commands for filesystem
  collision counts, tracked-set history differences, and archive enumeration.
- Added a five-repository matrix separating review norms, recorded distinct
  review practice, persisted evidence, and identity/verdict enforcement.
- Replaced Prospect and realtime-gs adoption/ranking claims with bounded pilots
  and explicit measurements; changed StructSplat and IntrinsicEngine to
  conditional in-place experiments.
- Restricted P0 to a clean allowlisted payload boundary plus disposable
  fresh-target, collision-refusal, no-history, and no-partial-write tests.
- Reclassified authority redirects, skill naming, and CI as
  target-conditioned; no live skill collision is claimed.
- Kept the three-source results-audit pattern as P1 and demoted maturity
  vocabulary, periodic audits, and micro-task records to P2 hypotheses with
  falsifiable promotion criteria.
- Reconciled the summary, per-repository sections, competing methods, priority
  list, decision sequence, and conclusion around pilot-versus-adoption status.

#### Evidence

- Revised artifact commit:
  `2b8d392fbf0326f36790c9c7655c1ab87212c9da`.
- The exact collision method remains bound to source commit
  `d8d649512f454c219dba55dd12f4d0398cb742e9`.
- The report incorporates the Reviewer's independent Prospect
  `e41b22e`/`bde6266`, realtime-gs `095313d`/`ca11378`, StructSplat
  FIT-042/FIT-043, and IntrinsicEngine RUNTIME-190 evidence.
- All 31 workflow regression tests pass.
- Live workflow validation and `git diff --check` pass.

#### Assumptions

- A repository label is mechanically distinct when the validator rejects equal
  nonempty Driver/Reviewer labels; neither agent-kit nor the targets
  authenticate the human or process behind a label.
- The clean payload behavior is established before choosing a static manifest
  or generator implementation.

#### Uncertainties

- Pilot process cost and defect-detection benefit remain unmeasured by design.
- No remote-only policy, private issue tracker, or unrecorded human practice
  was inspected.
- No live multi-repository skill-name collision was reproduced.

#### Review Focus

- Check all six required changes against the revised report rather than the
  original decision table.
- Confirm the exact commands can reproduce both collision and
  history-contamination evidence.
- Look for any remaining language that silently promotes a pilot to adoption
  or treats a target-conditioned integration choice as universal P0.
- Challenge whether the P1 results-audit recommendation has broader support
  than the three P2 single-source hypotheses.

#### Recommended Next Action

Review commit `2b8d392`, rerun the agent-kit workflow checks, and return an
independent terminal verdict or a precisely bounded remaining correction.

### Session Completion (codex-a, Driver, Revision Round 1)

#### Work completed

Addressed all six required changes from Review round 1, validated the revised
assessment, committed it, and returned the turn to the Reviewer.

#### Evidence

Revision commit `2b8d392`; all 31 workflow tests and live validation pass.

#### Files changed

- `docs/research/cross-repository-agent-workflow-adoption.md`
- `.agents/state/current-task.md`

#### Tests or experiments run

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py`
- `git diff --check`

#### Known limitations

This assessment makes no target-repository changes and supplies pilot decision
rules rather than adoption outcomes.

#### Unresolved questions

The operating value and cost of mechanically enforced final-review identity
remain pilot questions.

#### Repository state updated

Yes

#### Recommended next action

Reviewer independently evaluates the revised artifact at commit `2b8d392`.

### Review (codex-b, Reviewer, Round 2)

#### Verdict

Accepted

#### Self-reviewed

No

#### Correctness

The revision satisfies all six required changes from Round 1:

1. It records the fixed source commit and exact collision, tracked-set
   difference, and archive-enumeration commands.
2. It distinguishes review norms, recorded review practice, persisted
   evidence, and mechanically enforced identity/verdict state, and incorporates
   the alternate evidence path from every target.
3. It removes unsupported `High`/`Highest` adoption rankings and makes
   Prospect and realtime-gs bounded pilots with explicit measurements rather
   than adoption decisions.
4. It limits universal P0 to a clean allowlisted payload boundary and
   disposable fresh-target/collision/no-history regression. Authority adapters,
   skill names, and target CI are correctly target-conditioned.
5. It retains the independently recurring three-repository results-audit
   pattern as P1 and demotes the single-source maturity, periodic-audit, and
   micro-task ideas to P2 hypotheses with falsifiable promotion triggers.
6. The Decision Summary, per-repository recommendations, competing method,
   priority sections, decision sequence, and conclusion consistently separate
   safe pilots from adoption.

The durable decision is appropriately narrow: do not install or replace any
target workflow now; first repair agent-kit's distribution boundary, then use
bounded pilots to decide whether selected coordination invariants earn their
cost.

#### Evidence Quality

- Running the report's filesystem collision command against source
  `d8d649512f454c219dba55dd12f4d0398cb742e9` reproduced Prospect 11,
  StructSplat 12, realtime-gs 11, and IntrinsicEngine 12.
- Running its tracked-set command for all four targets reproduced the
  non-colliding active state, state summary, Task 001/002 archives, audit,
  workflow test, and dated ARA-session payload.
- Enumerating the actual archive confirmed those history paths are present in
  the install artifact.
- The review-practice matrix agrees with the independently inspected Prospect
  `e41b22e`/`bde6266`, realtime-gs `095313d`/`ca11378`, StructSplat
  FIT-042/FIT-043, and IntrinsicEngine RUNTIME-190/RUNTIME-191 evidence while
  preserving the targets' lack of identity enforcement.
- The common claim-table, raw-recomputation, source/config binding, control
  audit, accounting, and disposition requirements are present in all three
  target results-audit skills and absent as mandatory structure from
  agent-kit's generic experiment/review pair. P1 is therefore supported by
  more than one implementation.
- `git diff --check 37c3a1f..2b8d392`, all 31 workflow tests, and live state
  validation pass.
- All target working trees remain exactly in their recorded initial states.

#### Simplicity

The revision specifies P0 behavior and tests without preselecting a generator
platform. It proposes only one task record and the narrow validator needed for
each pilot, avoids a parallel task authority in StructSplat and IntrinsicEngine,
and conditions broader enforcement on measured value. No speculative
extension point is required for acceptance.

#### Missing Cases

Remote-only policy and unrecorded human practice remain outside the inspected
scope. Pilot cost, coordination defects, and defect-detection benefit remain
unmeasured. The report now states these as limitations and decision inputs
rather than treating them as evidence, so they do not block the assessment.

#### Required Changes

None.

#### Optional Improvements

- If the task's four-label disposition vocabulary is used mechanically in a
  later summary, render each present-state pilot recommendation as
  `leave unchanged pending a bounded pilot`; this does not change the current
  decision.
- Add the newly inspected review artifacts to `Key Sources` if the note later
  becomes a standalone evidence index rather than a decision record.

### Session Completion (codex-b, Reviewer, Round 2)

#### Work completed

Independently checked every Round 1 required change against revised artifact
commit `2b8d392fbf0326f36790c9c7655c1ab87212c9da`, reproduced its central
commands, challenged the P1/P2 evidence split, and returned an Accepted
verdict.

#### Evidence

All six corrections are present and internally consistent. Exact collision
counts, history contamination, archive contents, and three-source P1 support
were independently reproduced.

#### Files changed

- `.agents/state/current-task.md`

#### Tests or experiments run

- Four verbatim filesystem collision probes: `11/12/11/12`.
- Four tracked-set history-contamination probes and one archive enumeration.
- `git diff --check 37c3a1f..2b8d392`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`:
  31/31 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py`:
  passed with 10 skills and two archived tasks.
- Read-only target status checks; no target changed.

#### Known limitations

No adoption pilot or remote-policy inspection was performed. Those are
explicitly deferred decision evidence, not claims approved by this review.

#### Unresolved questions

Whether either pilot earns adoption remains unresolved by design and must be
decided from the report's stated cost, handoff, duplicate-state, and material-
finding measurements.

#### Repository state updated

Yes

#### Recommended next action

Driver follows the accepted-flow repository completion procedure: merge the
task branch, archive Task 003, update repository state, and preserve the
assessment's no-install decision.
