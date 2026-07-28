# Current Task

## Title

Fix agent workflow audit findings

## Task ID

002

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: driver

## Mode

Stabilize

## Goal

Make the two-agent workflow safe to install and internally enforce the
documented task, review, archive, and closeout lifecycle.

## Motivation

The accepted audit demonstrated six installation, schema, validation, branch
closeout, archive, and example-history failures that block safe adoption.

## Success Criteria

- Installation uses a tracked-file export that cannot copy `.git/`, with
  explicit collision behavior and guidance.
- Handoff and review templates use headings nested under `## Handoff Log`.
- The validator rejects all eleven audit matrix failures and enforces role,
  structured-review, status, and turn semantics while accepting valid
  independent and self-reviewed lifecycles.
- Accepted, Rejected, Inconclusive, and Superseded branch closeout paths are
  explicit and safely preserve metadata without merging rejected changes.
- Partial active records and malformed archives fail validation; valid archives
  require matching ids, terminal statuses, `Turn: none`, and valid verdicts.
- The illustrative task is outside operational history and automated regression
  tests cover the audit matrix plus valid lifecycle, archive, and closeout cases.
- Focused tests, full workflow validation, syntax compilation, and diff checks
  pass.

## Constraints

- Preserve the existing lightweight Markdown workflow and Python standard
  library implementation.
- Avoid external dependencies, speculative redesign, and unrelated changes.
- Work sequentially in the shared tree and hand the committed branch to the
  independent Reviewer.

## Non-Goals

- Turning the cooperative `Turn` marker into a concurrency lock.
- Automating merges, pushes, or cross-machine coordination.
- Generalizing the validator beyond this repository's documented schema.

## Selected Skills

- `task-orchestration`
- `implementation`
- `handoff`

## Current Evidence

- `docs/audits/agent-workflow-audit.md` records six findings and eleven
  reproduced validator mismatches.
- The audited validator treated only a non-empty title as active, recognized
  review text by a broad heading regex, and validated archives only by
  filename/id uniqueness.
- The audited README installed with `cp -r agent-kit/.`, which included
  `.git/`.
- The pre-fix regression run produced 13 expected failures across the audited
  invalid states and archive requirements.
- The candidate implementation passes all 21 tests, including the eleven-case
  audit matrix, valid active/archive lifecycles, target Git-metadata
  preservation, accepted merge closeout, and metadata-only closeout for
  Rejected, Inconclusive, and Superseded branches.
- Full validation now reports ten routed skills, one operational archive, and
  no active-state issues; the illustrative record is outside `docs/tasks/`.

## Minimal Plan

1. Add regression fixtures for the audit matrix and valid lifecycle/archive
   cases.
2. Align documented templates and implement structured active/archive
   validation.
3. Document safe installation and terminal branch closeout flows, and move the
   illustrative record outside operational history.
4. Run focused and full validation, self-audit the diff, and hand the branch to
   the Reviewer.

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
