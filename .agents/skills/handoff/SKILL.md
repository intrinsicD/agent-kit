---
name: handoff
description: Transfer work between Driver and Reviewer using structured claims, evidence, uncertainties, and verdicts.
---

# Handoff

Use whenever responsibility passes between agents.

## Transport

Handoffs travel through the repository, never through chat alone:

1. Commit your work on the task branch. Without branches, record the reviewed
   commit hash in the handoff instead.
2. Append your block to the Handoff Log in `.agents/state/current-task.md`.
3. Set the `Turn` field to the other role and commit.
4. Push when the other agent works from a different clone. On a shared clone,
   committing is enough.

The receiving agent starts by reading the Handoff Log. When agents share one
working tree, stop before the other one starts: the `Turn` field records whose
move it is, but it does not prevent concurrent writes.

## Driver handoff

```markdown
## Handoff

### Objective
### Changes
### Evidence
### Assumptions
### Uncertainties
### Review Focus
### Recommended Next Action
```

The Driver must identify weak points rather than hide them.

## Reviewer response

```markdown
## Review

### Verdict
Accepted / Accepted with follow-up / Revision required / Rejected / Inconclusive

### Self-reviewed
Yes / No. Yes means the Driver reviewed their own work because no second agent
was available. Pair it with the status
`Provisionally accepted (self-reviewed)`; the claim stays unapproved until an
independent agent or a human confirms it.

### Correctness
### Evidence Quality
### Simplicity
### Missing Cases
### Required Changes
### Optional Improvements
```

## Disagreement protocol

Do not argue indefinitely. Record:

```markdown
Claim A:
Claim B:
Evidence needed:
Experiment or decision rule:
Outcome:
```

Resolve with an experiment, test, benchmark, literature search, prototype, or
explicit human decision. Record human decisions under `## Human Decisions` in
`.agents/state/current-task.md`, following the escalation rules in `AGENTS.md`.

Two full revision rounds without an accepting verdict is the signal to
escalate rather than start a third.

## Session completion

Before an agent stops, append to the Handoff Log:

```markdown
## Session Completion

Work completed:
Evidence:
Files changed:
Tests or experiments run:
Known limitations:
Unresolved questions:
Repository state updated: Yes / No
Recommended next action:
```
