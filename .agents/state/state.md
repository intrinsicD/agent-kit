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
- The opt-in six-file `verify` profile installs three standard-library
  checkers plus target-owned docs-sync rules, a four-stage verification entry
  point, and a CI workflow that invokes that entry point once.
- Raw, rendered, and receipt-inclusive plans reject exact and hierarchical
  destination conflicts before writes. Exclusive creation and owned-path
  rollback preserve pre-existing target content and Git metadata.
- The optional `results-audit` skill adds claim inventory, raw recomputation,
  provenance, controls, accounting, evidence-scope, and disposition checks
  while leaving domain-specific rules local.
- Active and archived task state is validated for exact structure, unique
  visible fields, review semantics, status/turn pairing, terminal status, and
  matching ids.
- `scripts/verify.sh` is the seven-stage source-repository gate for Ruff lint
  and format, workflow structure, strict authority and documentation-link
  checks, the ARA claim ledger, and all 109 regression tests. GitHub Actions
  invokes it verbatim on Python 3.11, 3.12, and 3.13.
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

- Task 008 was accepted with follow-up by repository-owner direction after two
  independent `Revision required` rounds. The shipped target workflow is
  clean, but `workflow_run_directives()` in the anti-drift regression misses a
  relisted checker when `run:` follows `name:` in a YAML step. Named scalar
  and named block-form mutation regressions remain open.
- Historical findings and their dispositions remain in `docs/audits/` and
  `docs/tasks/`.

## Important Decisions

- Do not install agent-kit into, or replace the existing workflow of, Prospect,
  StructSplat, realtime-gs, or IntrinsicEngine.
- Distribute agent-kit only through schema-v2 named manifest groups and
  non-overwriting writes. `core` remains the exact 22-file payload; installs
  require `--slug` or `--no-prefix`, and dry-run, generated receipts, and
  read-only doctor are supported. Overwrite, update, repair, uninstall, and
  unapproved profile content are not implied.
- The optional `verify` profile is accepted for initial installation. Its
  docs-sync policy is empty and target-owned by default; authority and link
  checks run strictly in the target gate. Do not claim complete workflow
  mutation coverage until the named-step follow-up is closed.
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
- Optional `verify` payload files: 6.
- Agent workflow regression tests: 30.
- Installer distribution regression tests: 30.
- Validator-pack regression tests: 19.
- Verification wiring regression tests: 7.
- Unified verification tests: 109.
- ARA checker fixtures: 23.
- Tracked ARA claims: 17.
- Archived operational tasks: 8.
- Remediated audit findings: 6 of 6.
- Task 007 review findings resolved: 3 of 3.
- Task 008 review groups resolved before promotion: 4 of 5; one accepted
  follow-up remains.
- Assessed target workflows: 4.
- Task 008 final disposition: Accepted with follow-up by repository-owner
  promotion after independent Round 2 `Revision required`.

## Immediate Next Step

Close the named-step anti-drift regression gap when prioritized. The next
unstarted maturity slice is Plan 008, the opt-in task-tree profile, which would
bind as actual task 009; do not initialize it or pull later slices forward
without a new task request.

## Last Completed Task

- Task ID: 008
- Driver: codex-b
- Reviewer: codex-a (repository owner promoted the result with follow-up)
