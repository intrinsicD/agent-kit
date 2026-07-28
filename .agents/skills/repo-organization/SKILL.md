---
name: repo-organization
description: Keep repository state, decisions, experiments, backlog, and agent handoffs minimal, current, searchable, and reproducible.
---

# Repository Organization

Use when bootstrapping a repository, finishing substantial work, or correcting
state and documentation drift.

## Sources of truth

- `README.md`: purpose, current capabilities, quick start, reproduction.
- `AGENTS.md`: routing and universal rules.
- `.agent/state.md`: compact current state.
- `.agent/current-task.md`: only the active task.
- `.agent/backlog.md`: validated future work.
- `.agent/ideas.md`: unvalidated possibilities.
- `docs/decisions/`: durable consequential decisions.
- `docs/research/`: research that affects the repository.
- `docs/experiments/`: experiment plans and interpretations.
- `docs/audits/`: durable audit results.

Chat history is not a source of truth.

## Maintenance rules

- Remove stale and duplicated documentation.
- Do not create documents merely to satisfy process.
- Keep experimental outputs separate from stable APIs.
- Link decisions to evidence.
- Move validated ideas to backlog only after evidence or explicit human choice.
- Mark superseded decisions and rejected experiments rather than deleting useful history.
- Keep raw machine-readable results separate from prose interpretation.
- Maintain one obvious entry point for building, testing, and reproducing results.

## Decision record

Use only for consequential choices:

```markdown
# Decision: <title>

Date:
Status: Proposed / Accepted / Superseded / Rejected

## Context
## Decision
## Alternatives
## Evidence
## Consequences
## Risks
## Reversal Condition
```

## Completion update

At the end of substantial work, update:

1. `.agent/current-task.md`
2. `.agent/state.md`
3. relevant decision, experiment, research, or audit record
4. backlog or ideas only when justified
