---
name: research-methods
description: Research methods, theory, primary literature, adjacent terminology, implementations, and known failure modes for a repository problem.
---

# Research Methods

Use for method selection, theoretical questions, literature review, or locating
strong baselines and implementations.

## Required framing

Start with a specific research question. Avoid open-ended research.

Examples:

- Which methods solve the observed failure mode?
- Has this proposed mechanism appeared under another name?
- What is the strongest reproducible baseline?
- Under what assumptions are two formulations equivalent?

## Search strategy

Investigate:

1. direct terminology,
2. synonyms and mathematical formulations,
3. application-specific names,
4. foundational primary sources,
5. recent work citing foundational sources,
6. adjacent research fields,
7. open-source implementations,
8. critical or negative results.

Prefer primary literature and official implementations.

## Evidence classification

Mark each statement as one of:

- established result,
- source author claim,
- repository observation,
- agent inference,
- unverified hypothesis.

Do not merge these categories.

## Independent coverage

The Reviewer must search at least one meaningfully different path, such as:

- alternate terminology,
- another field,
- critical literature,
- implementation-oriented sources,
- more recent citing work.

## Repository artifact

Create or update `docs/research/<topic>.md`:

```markdown
# Research Note: <topic>

## Research Question
## Key Sources
## Established Results
## Competing Methods
## Assumptions
## Known Failure Modes
## Relevant Implementations
## Open Questions
## Implications for This Repository
```

Do not accumulate summaries that have no effect on a decision, experiment, or implementation.
