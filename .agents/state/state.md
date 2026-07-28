# Repository State

## Project Objective

Provide a lightweight, skill-based operating system for repositories developed
by two collaborating agents, with durable task state, sequential
Driver/Reviewer handoffs, independent falsification, and reproducible evidence.

## Working System

- Ten reusable skills are present and match the routing in `AGENTS.md`.
- The documented installer exports tracked files and preserves target Git
  metadata, but is not a clean distribution boundary for repositories that
  already have agent workflow state.
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

- The tracked-tree installer collides with all four assessed target
  repositories and would copy agent-kit's own state, task, audit, test, and ARA
  history. A clean payload boundary and disposable distribution regression are
  required before any target pilot.
- Task 002 resolved all six findings from the
  [historical workflow audit](../../docs/audits/agent-workflow-audit.md).

## Important Decisions

- Do not install agent-kit into, or replace the existing workflow of, Prospect,
  StructSplat, realtime-gs, or IntrinsicEngine.
- After the distribution blocker is fixed, evaluate only bounded coordination
  pilots in realtime-gs and Prospect. Consider in-place schema experiments in
  StructSplat or IntrinsicEngine only after a concrete failure establishes the
  need.
- Preserve the targets' stronger task, evidence, validation, and domain-skill
  systems. The leading reciprocal P1 candidate is a generic research-results
  audit; single-source IntrinsicEngine ideas remain P2 hypotheses.

## Current Metrics

- Routed skills: 10.
- Workflow regression tests: 31.
- Archived operational tasks: 3.
- Remediated audit findings: 6 of 6.
- Assessed target workflows: 4.
- Task 003 independent verdict: Accepted.

## Immediate Next Step

Replace the tracked-tree installer with an explicit clean payload boundary and
add disposable fresh-target, collision-refusal, no-history, and payload
allowlist regressions. The next substantial task swaps the roles recorded
below and starts with `task-orchestration`.

## Last Completed Task

- Task ID: 003
- Driver: codex-a
- Reviewer: codex-b
