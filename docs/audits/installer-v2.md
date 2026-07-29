# Audit: Installer v2

Date: 2026-07-29

Reviewed implementation: `5ceaceb`, `c3c4fcb`

## Scope

Driver self-audit of Task 007's manifest schema v2, group selection, slug
renderer, install and dry-run paths, generated receipt, doctor command,
regression suite, and user-facing installation contract. The audit asks whether
the implementation preserves target ownership and the existing
refuse-on-collision guarantee while adding the interfaces approved in the task
record. Quantitative and performance claims are not in scope.

## Contracts Reviewed

### Manifest and configuration

- The manifest accepts only schema v2 with named, nonempty groups and a
  required `core` group. Rows are strict source/destination pairs.
- Source and destination paths are safe relative paths. Sources must be unique
  regular files inside the source checkout; destinations must be globally
  unique, may not enter `.git`, and may not claim the generated receipt path.
- CLI selection always begins with `core`; repeated profiles form a stable
  union and unknown profiles fail with exit 2 before target writes.
- `install` requires exactly one of `--slug` and `--no-prefix`. Slugs implement
  the recorded regex and 24-character limit.

### Rendering and installed behavior

- The renderer has an explicit eleven-token allowlist. With a slug, it changes
  only matching skill directory segments, exact skill frontmatter names, and
  token occurrences inside single-backtick spans.
- Prose outside backticks is byte-for-byte unaffected by the rewrite. Tests
  specifically retain prose uses of “implementation”, “implementations”, and
  “handoff”.
- Rendering rejects duplicate final destinations. A disposable Git target
  proves that all eleven prefixed skills agree with their frontmatter and
  routing entries and that the installed validator passes.

### Preflight, writes, and rollback ownership

- Dry-run and install use the same rendered plan and collision function. The
  plan includes all selected payload entries and the generated receipt.
- Preflight reports every exact destination and blocking file/symlink ancestor.
  It writes nothing in both clean and colliding dry runs.
- Actual files use exclusive creation. The rollback ledger contains only files
  and directories created by that invocation, so pre-existing target content
  is never deleted.
- Fault injection covers a mid-payload copy failure and a partial receipt write
  after all payload files were created; both restore the exact pre-install
  target snapshot.
- The installer does not expose overwrite, force, update, repair, or uninstall
  behavior and uses only the Python standard library.

### Receipt and doctor trust boundary

- The receipt records its schema version, raw-manifest SHA-256 and version,
  slug/prefix/groups, UTC timestamp, hashes for immutable rendered files, and
  presence-only paths for user-owned templates.
- Receipt paths receive the same relative-path and `.git` protections as
  manifest paths. Receipt schema, hash shapes, ownership disjointness, config
  consistency, and timestamp timezone are validated before inspection.
- Doctor never writes. Immutable regular files are `OK`, `MODIFIED`, or
  `MISSING`; user templates are `PRESENT` or `MISSING`. Symlinks and blocking
  ancestors cannot satisfy immutable hashes, including a correct external file
  reached through a symlinked directory.
- A missing receipt is always a finding and explicitly reports unknown
  integrity/profile selection. Its bounded fallback checks current `core`
  presence and recognizes either unprefixed or valid slug-prefixed skill
  directories.
- Exit codes follow the approved contract: 0 clean/success, 1
  findings/collision/write failure, and 2 usage/environment/schema error.

## Findings and Disposition

No open critical, high, or medium findings remain in the Driver audit.

Two boundary issues were identified and resolved before this record:

1. Programmatic plan construction could previously put a non-core group first,
   producing a receipt that doctor would correctly reject. Plan construction
   now requires `core` first, matching the CLI and receipt schema.
2. A target could replace an immutable file's parent directory with a symlink
   to an external tree containing identical bytes. Doctor now classifies that
   path as `MODIFIED` without trusting the external file; a regression pins the
   behavior. The receipt itself receives the same ancestor check.

## Evidence

All Python test commands used `PYTHONDONTWRITEBYTECODE=1`.

- `python3 tests/test_distribution.py -q`: 24 focused tests passed. They cover
  manifest failures and group union, CLI migration and slug validation,
  bounded rendering, clean/colliding dry-run snapshots, exact and ancestor
  collisions, exclusive rollback including receipt failure, receipt
  provenance/ownership, doctor clean/modified/missing/template/missing-receipt
  states, no-write snapshots, installed validation, and Git metadata
  preservation.
- `./scripts/verify.sh`: all five gates passed; Ruff lint and format were clean,
  workflow state and 14 ARA claims validated, and all 82 regression tests
  passed.
- A separate disposable Git-target probe installed 22 `core` payload files and
  the receipt with slug `probe`; the installed validator found 11 valid skills
  and zero archived tasks; doctor exited 0 clean, then reported
  `MODIFIED AGENTS.md` and exited 1 after an induced edit. The target stayed on
  `main` at its original commit throughout.

## Required Fixes

None identified by the Driver self-audit.

## Optional Improvements

None recommended within this task. Update, repair, uninstall, cryptographic
signing, and inference of missing optional profiles would expand the approved
interface or threat model.

## Residual Risks

- The receipt detects accidental drift, not an adversary able to modify both
  payload and receipt; it is deliberately unsigned.
- Preflight plus exclusive file creation prevents overwrites but is not a
  filesystem transaction. A concurrent actor can still cause a refused or
  rolled-back install, and an uncatchable process termination can leave
  installer-created paths for a later collision report.
- Without a receipt, doctor cannot recover hashes or optional profile
  selection. Its presence-only `core` report is intentionally labeled unknown.
- This is a Driver self-audit. Independent Reviewer falsification is still
  required before acceptance.

## Verdict

Ready for independent review, subject to the final verification evidence in the
Driver handoff.
