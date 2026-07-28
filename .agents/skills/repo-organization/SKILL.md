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
- `.agents/state/state.md`: compact current state.
- `.agents/state/current-task.md`: only the active task, with its Handoff Log.
- `.agents/state/backlog.md`: validated future work.
- `.agents/state/ideas.md`: unvalidated possibilities.
- `docs/decisions/`: durable consequential decisions.
- `docs/research/`: research that affects the repository.
- `docs/experiments/`: experiment plans and interpretations.
- `docs/audits/`: durable audit results.
- `docs/tasks/`: archived records of completed tasks.

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

At the end of substantial work:

1. Archive the finished task: copy `.agents/state/current-task.md`, including
   its Handoff Log and final status, to `docs/tasks/<task-id>-<slug>.md`, then
   reset `current-task.md` to its template.
2. Update `.agents/state/state.md`.
3. Update the relevant decision, experiment, research, or audit record.
4. Update backlog or ideas only when justified.
5. Run `scripts/validate_agent_workflow.py` and fix anything it reports.
