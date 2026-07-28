---
name: implementation
description: Implement the smallest correct vertical slice with explicit behavior, tests, ownership, and no speculative architecture.
---

# Implementation

Use after behavior is sufficiently defined.

## Before coding

Specify:

- required behavior,
- interfaces affected,
- constraints,
- failure behavior,
- validation strategy,
- non-goals.

## Implementation order

1. Inspect the current path and existing abstractions.
2. Identify the smallest end-to-end change.
3. Add or update a failing test when practical.
4. Implement the narrow path.
5. Run focused tests.
6. Run broader relevant tests.
7. Measure performance only when performance is part of success.
8. Remove temporary code and unnecessary abstractions.
9. Prepare a handoff.

## Abstraction threshold

Add an abstraction only when at least one is true:

- two real implementations already exist,
- duplication causes a demonstrated maintenance problem,
- testing requires substitution,
- the boundary is a stable domain concept,
- performance requires a specialized boundary,
- a public API must remain stable while internals change.

Possible future reuse is insufficient.

## Prohibited patterns without evidence

- interfaces with one implementation,
- plugin systems with one plugin,
- service layers that only forward calls,
- generic factories without multiple creation policies,
- dependency injection without a testing or substitution need,
- configuration for hypothetical users,
- premature distributed architecture,
- broad refactoring mixed with behavior changes.

## Quality rules

Prefer:

- explicit data flow,
- narrow APIs,
- clear ownership,
- deterministic behavior,
- local reasoning,
- reference implementations for optimized code when practical.

Comments explain reasons, invariants, mathematics, and constraints, not syntax.

## Completion

A change is ready for review when:

- success criteria are met,
- relevant tests pass,
- edge cases are covered,
- changed behavior is documented,
- the repository remains buildable,
- unrelated changes are absent.
