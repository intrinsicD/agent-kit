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
- `.agents/state/state.md`: compact current state, including the roles of the
  last completed task.
- `.agents/state/current-task.md`: only the active task, with its Handoff Log
  and any recorded human decisions.
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

The Driver runs this at the end of substantial work, after the Reviewer has
returned a verdict and passed the turn back. `Superseded` is the exception: the
Driver can close it after recording the replacement or reason.

### Accepted branch

Use this flow only for `Accepted` or `Accepted with follow-up`:

1. Commit the reviewed task branch and merge it into the up-to-date default
   branch.
2. On the default branch, copy `.agents/state/current-task.md`, including its
   Handoff Log, human decisions, and final status, to
   `docs/tasks/<task-id>-<slug>.md`; set `Turn` to `none` in the archived copy;
   then reset `current-task.md` to its complete template.
3. Update `.agents/state/state.md`, including `## Last Completed Task` with the
   archived id and Driver/Reviewer labels so the next task can swap roles.
4. Update relevant decision, experiment, research, audit, backlog, or idea
   records only when the evidence justifies it.
5. Run `scripts/validate_agent_workflow.py`, commit the completion update, and
   push when another clone needs it.

### Non-merge terminal branch

Use this flow for `Rejected`, a closed `Inconclusive`, or `Superseded`. It
preserves the task record on the default branch without carrying any task
implementation:

1. On the task branch, ensure all earlier work is committed and the worktree is
   clean. `Rejected` and `Inconclusive` require the matching Reviewer verdict
   and `Turn: driver`; `Superseded` requires its reason and replacement, when
   any, in the Handoff Log.
2. Copy the final task record to `docs/tasks/<task-id>-<slug>.md`, set the
   archived copy to `Turn: none`, reset `current-task.md` to its complete
   template, and update `.agents/state/state.md` with the terminal result and
   `## Last Completed Task`.
3. Stage exactly these metadata paths:

   ```bash
   git add .agents/state/current-task.md .agents/state/state.md \
     docs/tasks/<task-id>-<slug>.md
   git diff --cached --name-only
   ```

   Stop if the listing contains any other path. Commit this as the closeout
   commit and record its hash.
4. Switch to the up-to-date default branch and cherry-pick only the closeout
   commit:

   ```bash
   git switch <default-branch>
   git pull --ff-only
   git cherry-pick <closeout-commit>
   ```

   Do not merge the task branch. Cherry-picking the single metadata commit
   excludes its implementation ancestors. If the cherry-pick conflicts, stop
   and resolve only after confirming the three-path scope.
5. Run `scripts/validate_agent_workflow.py` on the default branch and push when
   another clone needs the record. Retain or delete the unmerged task branch
   according to the repository's normal branch-retention policy.

An `Inconclusive` task that will run another resolving experiment is not
terminal: update its plan, set `Status: In progress`, and continue instead of
archiving it. `Provisionally accepted (self-reviewed)` is also nonterminal
until an independent agent or human promotes it.
