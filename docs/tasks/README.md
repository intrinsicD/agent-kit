# Task Records

Archived records of completed tasks, copied from
`.agents/state/current-task.md` at completion, including their Handoff Logs
and final status.

Name files `<task-id>-<slug>.md` with a zero-padded incrementing id and a
lowercase slug, for example `007-neighbor-search-benchmark.md`. Ids must be
unique; `scripts/validate_agent_workflow.py` checks this and refuses a new task
that reuses an archived id.

Archived records carry `Turn: none`, since no role acts next, and use a
terminal status: `Accepted`, `Accepted with follow-up`, `Rejected`,
`Inconclusive`, or `Superseded`. The validator applies the complete task schema,
requires the Task ID to match the filename, and checks the structured review
semantics for statuses that require a verdict.

Rejected, closed Inconclusive, and Superseded task branches use the
metadata-only closeout in the `repo-organization` skill. Their archive reaches
the default branch without merging the discarded implementation.

Illustrative records live under `docs/examples/`, outside this operational
history and its id allocation.
