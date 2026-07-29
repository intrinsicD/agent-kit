# Repository State

## Project Objective

Provide a lightweight, skill-based operating system for repositories developed
by two collaborating agents, with durable task state, sequential
Driver/Reviewer handoffs, independent falsification, and reproducible evidence.

## Working System

- Eleven reusable skills are present and match the routing in `AGENTS.md`.
- The installer copies a fixed 22-file allowlist containing reusable workflow
  authority, skills, validation, blank state, and blank documentation indexes.
  It refuses every exact destination or blocking ancestor collision before
  writes and does not enter target Git metadata.
- The optional `results-audit` skill adds claim inventory, raw recomputation,
  provenance, controls, accounting, evidence-scope, and disposition checks
  while leaving domain-specific rules local.
- Active and archived task state is validated for exact structure, unique
  visible fields, review semantics, status/turn pairing, terminal status, and
  matching ids.
- `scripts/verify.sh` is the single source-repository gate for Ruff lint and
  format, workflow structure, the ARA claim ledger, and all 64 regression
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
- Installer evidence covers a stable target on Python 3.12/Linux; concurrent
  adversarial mutation, uncatchable termination, non-POSIX behavior, and
  alternate Python versions remain outside the approved evidence.

## Known Failures

No open workflow failure is currently recorded. Historical findings and their
accepted remediations remain in `docs/audits/` and `docs/tasks/`.

## Important Decisions

- Do not install agent-kit into, or replace the existing workflow of, Prospect,
  StructSplat, realtime-gs, or IntrinsicEngine.
- Distribute agent-kit only through the fixed, non-overwriting manifest and
  blank templates. Overwrite, update, uninstall, and target profiles are not
  implied.
- Preserve target-specific task, evidence, validation, and domain-skill
  systems. `results-audit` is an optional generic procedure; domain rules
  remain local.
- If explicitly prioritized, evaluate the smallest coordination pilot in
  realtime-gs first and Prospect separately afterward. Consider only in-place
  identity/verdict checks in StructSplat or IntrinsicEngine after a concrete
  failure establishes the need.
- Before an authorized zero-collision target pilot, add a read-only installer
  plan; do not import IntrinsicEngine's broader generator platform.

## Current Metrics

- Routed skills: 11.
- Fixed payload files: 22.
- Workflow regression tests: 36.
- Unified verification tests: 64.
- ARA checker fixtures: 23.
- Archived operational tasks: 6.
- Remediated audit findings: 6 of 6.
- Assessed target workflows: 4.
- Task 006 independent verdict: Accepted.

## Immediate Next Step

Initialize the validated Installer v2 slice as task 007 with roles swapped.
Record human outcomes for the prefix-policy and doctor-receipt interface
questions before implementation; do not infer either choice from the planning
reference alone.

## Last Completed Task

- Task ID: 006
- Driver: codex-b
- Reviewer: codex-a
