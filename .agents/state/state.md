# Repository State

## Project Objective

Provide a lightweight, skill-based operating system for repositories developed
by two collaborating agents, with durable task state, sequential
Driver/Reviewer handoffs, independent falsification, and reproducible evidence.

## Working System

- Eleven reusable skills are present and match the routing in `AGENTS.md`.
- The installer consumes schema-v2 manifest groups while keeping `core` at the
  accepted 22-file payload. Every install explicitly selects slug-prefixing or
  no-prefix behavior; dry-run uses the same plan, install emits a receipt, and
  doctor checks immutable hashes plus presence-only user templates.
- Raw, rendered, and receipt-inclusive plans reject exact and hierarchical
  destination conflicts before writes. Exclusive creation and owned-path
  rollback preserve pre-existing target content and Git metadata.
- The optional `results-audit` skill adds claim inventory, raw recomputation,
  provenance, controls, accounting, evidence-scope, and disposition checks
  while leaving domain-specific rules local.
- Active and archived task state is validated for exact structure, unique
  visible fields, review semantics, status/turn pairing, terminal status, and
  matching ids.
- `scripts/verify.sh` is the single source-repository gate for Ruff lint and
  format, workflow structure, the ARA claim ledger, and all 86 regression
  tests. GitHub Actions invokes it verbatim on Python 3.11, 3.12, and 3.13.
- The standard-library ARA checker enforces required artifacts, claim shape,
  dispositions, dependencies, repository-contained proof paths, staging
  references, and ledger discoverability.
- Accepted merge closeout and metadata-only non-merge closeout are documented
  and covered by executable Git probes.
- The four target-workflow dispositions were revalidated at explicit commits:
  no normal installation or replacement, with only bounded conditional pilots.
- The regression suite and live validator pass on the completed repository.

## Experimental Components

- The `Turn` field remains a cooperative protocol marker rather than a
  concurrency lock.
- Markdown role labels do not cryptographically authenticate agent identity.
- Installer evidence covers Linux and the CI floor of Python 3.11–3.13.
  Unsigned-receipt tampering, concurrent adversarial mutation, uncatchable
  termination, and Windows/non-POSIX behavior remain outside the approved
  evidence. Without a receipt, doctor intentionally cannot recover hashes or
  optional-profile selection.

## Known Failures

No open workflow failure is currently recorded. Historical findings and their
accepted remediations remain in `docs/audits/` and `docs/tasks/`.

## Important Decisions

- Do not install agent-kit into, or replace the existing workflow of, Prospect,
  StructSplat, realtime-gs, or IntrinsicEngine.
- Distribute agent-kit only through schema-v2 named manifest groups and
  non-overwriting writes. `core` remains the exact 22-file payload; installs
  require `--slug` or `--no-prefix`, and dry-run, generated receipts, and
  read-only doctor are supported. Overwrite, update, repair, uninstall, and
  unapproved profile content are not implied.
- Preserve target-specific task, evidence, validation, and domain-skill
  systems. `results-audit` is an optional generic procedure; domain rules
  remain local.
- If explicitly prioritized, evaluate the smallest coordination pilot in
  realtime-gs first and Prospect separately afterward. Consider only in-place
  identity/verdict checks in StructSplat or IntrinsicEngine after a concrete
  failure establishes the need.
- Any authorized target pilot begins with the accepted read-only dry-run and
  requires zero collisions; do not import IntrinsicEngine's broader generator
  platform.

## Current Metrics

- Routed skills: 11.
- Fixed `core` payload files: 22.
- Agent workflow regression tests: 30.
- Installer distribution regression tests: 28.
- Verification wiring regression tests: 5.
- Unified verification tests: 86.
- ARA checker fixtures: 23.
- Archived operational tasks: 7.
- Remediated audit findings: 6 of 6.
- Task 007 review findings resolved: 3 of 3.
- Assessed target workflows: 4.
- Task 007 independent verdict: Accepted.

## Immediate Next Step

Initialize the generic validator pack and target CI template as actual task
008, applying the role swap implied by the Last Completed Task. Keep the
profile opt-in and do not pull later maturity-program slices forward.

## Last Completed Task

- Task ID: 007
- Driver: codex-a
- Reviewer: codex-b
