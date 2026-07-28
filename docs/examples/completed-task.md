# Example Completed Task Record

This is an illustrative example of a completed task record, not real project
history. It shows the level of detail the workflow expects.

## Title

Replace brute-force neighbor search with a uniform grid

## Task ID

000

## Role Assignment

- Driver: agent-a
- Reviewer: agent-b
- Turn: none

## Mode

Implement

## Goal

Reduce neighbor-query time in the particle pipeline without changing query
results.

## Motivation

Profiling on the 100k-particle benchmark shows 78% of frame time in
`find_neighbors` (see `docs/experiments/neighbor-profile.md`).

## Success Criteria

- `find_neighbors` returns identical neighbor sets to the brute-force
  reference on the existing test inputs.
- At least 10x speedup on the 100k-particle benchmark.
- No regression in total memory above 1.2x of the current peak.

## Constraints

- Fixed query radius; no need to support variable radii yet.
- Single-threaded; parallelism is out of scope for this task.

## Non-Goals

- No kd-tree or BVH; a uniform grid is sufficient for the observed density.
- No API change for callers of `find_neighbors`.

## Selected Skills

- task-orchestration
- implementation
- review-and-falsification

## Current Evidence

- Profile: `docs/experiments/neighbor-profile.md`.
- Reference implementation kept as `find_neighbors_bruteforce` for testing.

## Minimal Plan

1. Add a failing equivalence test comparing grid output to brute force.
2. Implement the uniform grid behind the existing function signature.
3. Benchmark both implementations on the 100k input.

## Status

Accepted with follow-up

## Human Decisions

None. Nothing in this task required a product, risk, or cost judgement.

## Handoff Log

### Handoff (agent-a, Driver)

#### Objective

Grid-based neighbor search with identical results and at least 10x speedup.

#### Changes

`src/neighbors.py` contains the grid implementation and
`tests/test_neighbors.py` contains equivalence and boundary tests.

#### Evidence

The equivalence test passes on all existing inputs; the benchmark shows 23x
speedup at 100k particles; peak memory is 1.1x baseline.

#### Assumptions

The query radius never exceeds twice the mean particle spacing.

#### Uncertainties

Behavior when all particles fall into one cell is untested.

#### Review Focus

Cell-boundary correctness and the radius assumption.

#### Recommended Next Action

Review, then merge.

### Review (agent-b, Reviewer)

#### Verdict
Accepted with follow-up

#### Self-reviewed
No

#### Correctness
Equivalence holds on existing inputs and on a new randomized test with
particles placed exactly on cell boundaries.

#### Evidence Quality
Benchmark is representative; ran it independently, reproduced 21x.

#### Simplicity
Appropriately minimal; no speculative abstractions found.

#### Missing Cases
Degenerate all-particles-in-one-cell input falls back to quadratic time
silently.

#### Required Changes
None blocking.

#### Optional Improvements
Add the degenerate-density case to the backlog with a measured threshold.

### Session Completion (agent-a)

#### Work completed

Grid implementation merged.

#### Evidence

Tests and benchmark linked above.

#### Files changed

`src/neighbors.py` and `tests/test_neighbors.py`.

#### Tests or experiments run

Full test suite and 100k benchmark.

#### Known limitations

Quadratic fallback on degenerate density.

#### Unresolved questions

None.

#### Repository state updated

Yes

#### Recommended next action

Add a backlog item for degenerate density handling.
