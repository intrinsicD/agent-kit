# Task Records

Archived records of completed tasks, copied from
`.agents/state/current-task.md` at completion, including their Handoff Logs
and final status.

Name files `<task-id>-<slug>.md` with a zero-padded incrementing id and a
lowercase slug, for example `007-neighbor-search-benchmark.md`. Ids must be
unique; `scripts/validate_agent_workflow.py` checks this and refuses a new task
that reuses an archived id.

Archived records carry `Turn: none`, since no role acts next. Rejected and
inconclusive tasks are archived too — their record is what stops the next task
from repeating the attempt.

`000-example-task.md` is an illustrative example of a filled-in record, not
real project history.
