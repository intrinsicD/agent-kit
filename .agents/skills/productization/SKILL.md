---
name: productization
description: Convert experimentally validated functionality into robust, documented, maintainable, user-facing software without prematurely expanding scope.
---

# Productization

Use only when the central functionality has already demonstrated value.

## Entry gate

Do not productize unless:

- core behavior is validated,
- target users or use cases are identified,
- important failure modes are known,
- success metrics exist,
- continued maintenance is justified.

## Productization work

Consider only what is currently needed:

- stable public API,
- clear configuration,
- input validation,
- error messages,
- packaging,
- compatibility,
- observability,
- reproducible deployment,
- performance guarantees,
- documentation and examples,
- migration and versioning,
- security and licensing review.

## Constraints

- Preserve a minimal architecture.
- Do not add a plugin system merely for imagined integrations.
- Expose one preferred workflow.
- Keep experimental features visibly separate.
- Add reliability before adding breadth.
- Make operational failures diagnosable.
- Define support boundaries and unsupported cases.

## Release readiness

Require:

- acceptance tests,
- regression tests,
- documented limitations,
- reproducible build,
- audited dependencies,
- measured performance on target workloads,
- Reviewer approval,
- updated README and repository state.
