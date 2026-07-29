# Current Task

## Title

Implement the maturity program verification foundation

## Task ID

006

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

## Mode

Implement

## Goal

Provide one local verification command, mirrored verbatim in CI, that checks
formatting, lint, workflow structure, the ARA claim ledger, and the full
regression suite.

## Motivation

The accepted maturity program identifies verification as the dependency for
every later installer/profile slice. The live baseline has 36 passing tests and
a passing workflow validator, but Ruff 0.15.20 still reports two known format
failures, the ARA ledger is unchecked, and the repository has no single
verification entry point or CI workflow.

## Success Criteria

1. `./scripts/verify.sh` exits 0 on the clean tree and an induced failure in
   each of its five gates makes it exit nonzero.
2. Repository-wide `ruff check` and `ruff format --check` pass with the exact
   version pinned in `requirements-dev.txt`; the two-file format-only change is
   isolated in a mechanical commit.
3. `scripts/check_ara.py` accepts the live ledger and rejects fixtures for each
   documented ledger invariant.
4. `.github/workflows/ci.yml` tests Python 3.11, 3.12, and 3.13 and invokes
   `./scripts/verify.sh` verbatim; a regression test pins that stage list.
5. `README.md` documents the one-command workflow and claim ledger, all
   existing tests remain green, and the maturity plan records its actual task
   numbering and any verified divergence from the proposed baseline.

## Constraints

- Use only the Python standard library in repository scripts; Ruff is the sole
  pinned development dependency.
- Do not change claim C13 or the distribution manifest.
- Keep mechanical formatting separate from semantic changes.
- Preserve the refusal-on-collision installer behavior and the 22-file payload.
- Treat the maturity plan as planning input: actual task state and reviewed
  evidence supersede indicative numbering.

## Non-Goals

- Target-facing verification/CI templates or ARA templates.
- Installer profiles, slug rendering, dry-run, or doctor behavior.
- The proposed single-product convergence decision affecting IntrinsicEngine.
- Changes to payload skill behavior or the payload `AGENTS.md`.

## Selected Skills

- `task-orchestration`
- `implementation`
- `code-audit`
- `review-and-falsification`
- `handoff`
- `repo-organization`

## Current Evidence

- `python3 scripts/validate_agent_workflow.py`: pass; 11 skills and 5 archives.
- `python3 -m unittest discover -s tests -v`: 36/36 pass.
- `ruff check .` with Ruff 0.15.20: pass.
- `ruff format --check .` with Ruff 0.15.20: fails only
  `scripts/validate_agent_workflow.py` and `tests/test_agent_workflow.py`.
- Task ID 005 is already archived, so the plan's first indicative ID binds to
  actual task 006.

## Minimal Plan

1. Record this task and the validated remaining program backlog on a task
   branch.
2. Commit the two-file Ruff formatting change mechanically and re-run the
   unchanged suite.
3. Add the pinned toolchain and five-stage `verify.sh`.
4. Implement and fixture-test the ARA ledger checker.
5. Add CI, stage-list regression coverage, README guidance, and a dated plan
   amendment.
6. Run clean and induced-failure checks, audit the code and diff, then prepare
   a committed Driver handoff for independent review.

## Status

In progress

## Human Decisions

Escalated questions and the answers humans gave. An answer that exists only in
chat is not recorded. Use one block per decision:

```markdown
### Question
### Options
### Recommendation
### Decision
### Date
```

## Handoff Log

Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`.
