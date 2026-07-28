---
name: handoff
description: Transfer work between Driver and Reviewer using structured claims, evidence, uncertainties, and verdicts.
---

# Handoff

Use whenever responsibility passes between agents.

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
explicit human decision.

## Session completion

Before an agent stops, record:

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
