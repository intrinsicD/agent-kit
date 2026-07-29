# Current Task

## Title

Implement generic validator pack and target CI template

## Task ID

008

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

## Mode

Implement

## Goal

Make a fresh opt-in `core` + `verify` installation self-enforcing through
generic authority, document-link, and documentation-sync checks, one target
verification entry point, and a CI template that invokes that entry point
verbatim.

## Motivation

Task 007 established safe profile-aware distribution but fresh targets still
receive only structural validation. They have no single command that runs all
generic checks and no CI wiring that stays aligned with the local command.
Authority-surface drift, broken repository-document links, and missed
documentation updates are recurring failure classes in the assessed sibling
repositories.

The mechanism must remain generic. In particular, prior evidence shows that
opinionated documentation-sync rules rapidly become vacuous or noisy, so the
shipped rules file should teach the schema without imposing target-specific
policy.

## Success Criteria

1. `scripts/check_authority.py` and `scripts/check_doc_links.py` are
   standard-library-only, expose `--root` and `--strict`, follow the repository
   exit convention (0 pass, 1 findings, 2 usage/environment/schema error), pass
   on the live repository, fail controlled fixtures, and run in the source
   `scripts/verify.sh`.
2. `scripts/check_docs_sync.py` reads `[[rule]]` entries through Python 3.11+
   `tomllib`, accepts changed files through `--files` or `--base`, requires
   non-empty reasons, warns by default, and exits successfully with a warning
   outside Git or when no base can be resolved in non-strict mode.
3. A new opt-in manifest group `verify` installs the three checker source
   files, a nearly empty `docs-sync-rules.toml`, a target
   `scripts/verify.sh` containing `# TODO: repository-specific gates`, and
   `.github/workflows/agent-workflow.yml`.
4. The target workflow invokes `./scripts/verify.sh` verbatim and does not
   duplicate its stages; regression tests pin this anti-drift property.
5. Installing `core` + `verify` into a disposable Git repository succeeds,
   preserves the 22-file `core` group, and the installed verification script
   exits 0 immediately.
6. Checker fixtures, distribution regressions, source verification, and the
   Python 3.11–3.13 CI matrix pass; README guidance and a durable audit record
   accurately describe the supported interface and evidence boundary.

## Constraints

- Keep the profile opt-in and leave `core` at exactly 22 payload files.
- Use only the Python standard library in the three shipped checkers.
- Resolve authority according to the accepted design: optional `CLAUDE.md`
  must symlink to `AGENTS.md` or carry an explicit redirect marker; only one
  physical skills root may exist; skill frontmatter names must match
  directories; optional `.codex/config.yaml` must reference the contract.
- Scan Markdown only under the bounded accepted roots, resolve relative and
  repository-root-relative paths, ignore fenced code, and skip external
  schemes and same-document anchors.
- Use the accepted `[[rule]]` schema with `trigger`, `one_of`, and non-empty
  `reason`; do not hand-roll TOML parsing.
- Name the target workflow `agent-workflow.yml` and have it run
  `./scripts/verify.sh` verbatim.
- Preserve installer collision, ownership, rollback, receipt, dry-run, doctor,
  and slug-rendering guarantees.

## Non-Goals

- Opinionated target documentation-sync rules.
- Root-hygiene, workflow-name, or GitHub pull-request contract checks.
- Any target-repository installation pilot.
- Later task-tree, evidence, or process-growth profiles.
- Overwrite, update, repair, or uninstall behavior.

## Selected Skills

- `task-orchestration`
- `implementation`
- `code-audit`
- `handoff`
- `repo-organization`

## Current Evidence

- Accepted Task 007 provides schema-v2 named manifest groups, a fixed 22-file
  `core`, full-union collision preflight, safe slug rendering, dry-run,
  bounded receipts, and read-only doctor behavior.
- The live source gate currently runs Ruff lint and format, workflow structure,
  ARA validation, and 86 regressions on Python 3.11–3.13.
- The planning record identifies authority drift, broken document links, and
  diff-triggered documentation checks as recurring donor-repository needs,
  while also recording false-positive and near-vacuous docs-sync policies.
- Python 3.11 is the supported floor, so stdlib `tomllib` is available.
- Existing installation templates are user-owned and immutable code is hashed
  in the generated receipt, providing a tested ownership model for this
  profile.

## Minimal Plan

1. Inspect current verification, manifest, installer-mode, and template tests;
   fix the smallest explicit interfaces before adding payload.
2. Implement authority and document-link checkers with live-tree and
   induced-failure fixtures, then wire both into the source verification gate.
3. Implement the TOML docs-sync checker and its warning/strict Git behavior
   with schema, changed-file, and no-Git tests.
4. Add the six-file opt-in `verify` group, target verification and workflow
   templates, executable-mode handling if required, and anti-drift assertions.
5. Install `core` + `verify` into a disposable Git repository and exercise the
   installed gate; run focused and full verification plus an independent
   Driver code audit.
6. Document the interface and evidence, commit bounded slices, and hand the
   fixed branch to Reviewer `codex-a` for independent falsification.

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
