---
name: review-and-falsification
description: Independently challenge a proposed idea, experiment, architecture, or implementation and return an evidence-based verdict.
---

# Review and Falsification

The Reviewer uses this skill. The objective is to discover errors and unjustified
complexity, not to restyle the Driver's work.

## Review sequence

1. Restate the claim or required behavior.
2. Identify assumptions.
3. Inspect evidence independently.
4. Search for counterexamples and missing cases.
5. Check whether a simpler approach suffices.
6. Reproduce important tests, experiments, or benchmarks.
7. Compare conclusions with the actual evidence.
8. Return a verdict.

## Falsification questions

- What observation would prove this wrong?
- Does the test isolate the claimed mechanism?
- Can the result be explained by a confounder?
- Are there hidden input, parameter, or dataset dependencies?
- Is the baseline strong and fair?
- Does the implementation satisfy behavior outside the happy path?
- Is an abstraction justified by current requirements?
- Can code or structure be removed without losing value?

## Verdicts

- Accepted
- Accepted with follow-up
- Revision required
- Rejected
- Inconclusive

Required changes must be separated from optional improvements.

## Artifact and placement

```markdown
### Review

#### Verdict
#### Self-reviewed
#### Correctness
#### Evidence Quality
#### Simplicity
#### Missing Cases
#### Required Changes
#### Optional Improvements
```

Append the review to the Handoff Log in `.agents/state/current-task.md`.
Record durable findings that outlive the task in `docs/audits/`.

A review written by the Driver because no second agent was available sets
`Self-reviewed: Yes` and the status `Provisionally accepted (self-reviewed)`.
Only an independent agent or a human promotes it to `Accepted`.

Do not approve substantial work solely because tests pass. Check whether the
tests and success criteria are meaningful.
