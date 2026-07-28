# Repository State

## Project Objective

Provide a lightweight, skill-based operating system for repositories developed
by two collaborating agents, with durable task state, sequential
Driver/Reviewer handoffs, independent falsification, and reproducible evidence.

## Working System

- Ten reusable skills are present and match the routing in `AGENTS.md`.
- Installation exports only tracked files, preserves target Git metadata, and
  documents collision handling.
- Active and archived task state is validated for exact structure, unique
  visible fields, review semantics, status/turn pairing, terminal status, and
  matching ids.
- Accepted merge closeout and metadata-only non-merge closeout are documented
  and covered by executable Git probes.
- The regression suite and live validator pass on the completed repository.

## Experimental Components

- The `Turn` field remains a cooperative protocol marker rather than a
  concurrency lock.
- Markdown role labels do not cryptographically authenticate agent identity.

## Known Failures

None currently recorded. Task 002 resolved all six findings from the
[historical workflow audit](../../docs/audits/agent-workflow-audit.md) and
received an independent `Accepted` verdict after two bounded revision rounds.

## Important Decisions

None recorded.

## Current Metrics

- Routed skills: 10.
- Workflow regression tests: 31.
- Archived operational tasks: 2.
- Remediated audit findings: 6 of 6.
- Task 002 independent verdict: Accepted.

## Immediate Next Step

No adoption-blocking workflow fix remains. The next substantial task swaps the
roles recorded below and starts with `task-orchestration`.

## Last Completed Task

- Task ID: 002
- Driver: codex-b
- Reviewer: codex-a
