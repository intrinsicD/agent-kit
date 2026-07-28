---
name: code-audit
description: Audit critical code for correctness, numerical behavior, performance validity, API quality, ownership, concurrency, and maintainability.
---

# Code Audit

Use for critical components, numerical code, performance changes, public APIs,
or pre-release stabilization.

## Correctness audit

Check:

- invariants,
- preconditions and postconditions,
- ownership and lifetime,
- error handling,
- undefined behavior,
- edge cases,
- deterministic behavior,
- concurrency and synchronization,
- serialization and compatibility where relevant.

## Mathematical and numerical audit

Check:

- dimensions and units,
- domains,
- boundary conditions,
- existence assumptions,
- limiting cases,
- conditioning,
- tolerances,
- floating-point behavior,
- equivalence claims,
- availability of a reference result.

## Performance audit

Check:

- representative workload,
- warmup,
- synchronization,
- compiler and build mode,
- hardware context,
- hidden transfers,
- allocation behavior,
- CPU/GPU timing separation,
- comparison fairness,
- performance regressions elsewhere.

Do not accept optimization claims without a benchmark and measured bottleneck.

## API and architecture audit

Check:

- one obvious usage path,
- dependency direction,
- stable domain boundaries,
- accidental coupling,
- unnecessary wrappers,
- speculative extension points,
- compatibility impact,
- testability.

## Output

Write `docs/audits/<topic>.md` for durable audits:

```markdown
# Audit: <topic>

## Scope
## Findings
## Severity
## Evidence
## Required Fixes
## Optional Improvements
## Residual Risks
## Verdict
```
