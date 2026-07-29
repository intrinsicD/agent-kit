# Current Task

## Title

Refactor distribution boundary and add results-audit skill

## Task ID

004

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

## Mode

Implement

## Goal

Replace the unsafe tracked-tree installation path with a fixed, auditable clean
payload that initializes blank workflow state without overwriting target files,
and add one optional generic results-audit skill distilled from three
independent repository implementations.

## Motivation

Task 003 independently confirmed that the documented `git archive HEAD`
installer collides with existing repositories and copies agent-kit's own state,
tasks, audits, tests, and ARA history. The same accepted assessment found a
recurring, repository-independent results-audit core that is absent from the
generic skill set.

## Success Criteria

- A fixed manifest names every installable source and destination path; the
  installer copies only that allowlist and never exports the tracked tree.
- Operational state and documentation indexes installed into a fresh target
  are blank project templates, not copies of agent-kit's current state or
  history.
- The payload excludes source ARA records, audits, completed tasks, dated
  sessions, regression tests, and the source repository README.
- The installer detects and reports every exact destination or blocking
  ancestor collision before writing anything, exits nonzero, and offers no
  overwrite mode.
- Disposable Git-repository tests prove the fresh install contains exactly the
  declared payload, passes its installed validator, preserves target Git
  metadata, and leaves a collision target unchanged.
- An optional `results-audit` skill requires a claim inventory, raw
  recomputation, source/config binding, controls and accounting checks,
  evidence-scope classification, and explicit claim dispositions without
  importing repository-specific rules.
- `AGENTS.md`, user documentation, skill validation, focused regressions, the
  full regression suite, and live validation agree on the new installation and
  routing behavior.
- An independent Reviewer returns a terminal verdict.

## Constraints

- Use only the Python standard library and a fixed payload definition.
- Treat every existing target path or symlink as protected; never merge,
  replace, or delete target content.
- Keep blank templates separate from agent-kit's live operational state.
- Preserve the target repository's `.git` metadata and unrelated files.
- Implement and test only inside agent-kit or disposable temporary
  repositories.

## Non-Goals

- No installation into Prospect, StructSplat, realtime-gs, or IntrinsicEngine.
- No target-specific authority adapters, skill renaming, CI integration, or
  coordination pilots.
- No configurable plugin/template platform, overwrite/update/uninstall mode,
  or speculative distribution abstraction.
- No P2 maturity vocabulary, periodic audit, or micro-task profile.
- No domain-specific rate, renderer, viewer, checkpoint, or experiment rules
  in the generic results-audit skill.

## Selected Skills

- task-orchestration
- implementation
- code-audit
- handoff

## Current Evidence

- Task 003 and
  `docs/research/cross-repository-agent-workflow-adoption.md` were independently
  Accepted.
- The current README still documents a tracked-tree archive extraction that
  copies repository history and can overwrite target files.
- Prospect, StructSplat, and realtime-gs independently converge on claim
  inventory, raw recomputation, exact provenance, controls/accounting, bounded
  evidence scope, and explicit dispositions.
- The current workflow has 10 routed skills, 31 regression tests, and three
  validated task archives.

## Minimal Plan

1. Commit this task setup on a dedicated branch.
2. Add fixed payload/template files and a narrow preflight-then-copy installer.
3. Add disposable fresh-install, collision/no-write, payload-boundary, and Git
   metadata regressions.
4. Add the optional generic results-audit skill and update routing and user
   documentation.
5. Run focused and full validation, self-audit the boundary and scope, commit
   the implementation, and hand the fixed commit to the Reviewer.

## Status

In progress

## Human Decisions

None.

## Handoff Log

Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`.
