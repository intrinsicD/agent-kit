# Task Records

Archive completed task records here by copying
`.agents/state/current-task.md` after the terminal verdict and closeout.

Name files `<task-id>-<slug>.md` with a zero-padded incrementing id and a
lowercase slug, for example `007-neighbor-search-benchmark.md`. IDs must be
unique and match the ID inside the record.

Archived records use `Turn: none` and a terminal status. Run
`python3 scripts/validate_agent_workflow.py` before committing an archive.
