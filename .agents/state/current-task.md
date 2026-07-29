# Current Task

## Title

Implement Installer v2 configuration and diagnostics

## Task ID

007

## Role Assignment

- Driver: codex-a
- Reviewer: codex-b
- Turn: reviewer

## Mode

Implement

## Goal

Make installation configurable and diagnosable through slug-prefixed skill
names, a non-writing dry run, a read-only doctor, and a grouped manifest that
later profiles can extend, while preserving the fixed allowlist,
refuse-on-collision, and no-overwrite guarantees.

## Motivation

All four assessed sibling repositories prefix skills to avoid collisions in
multi-repository discovery surfaces, and the owner's observed workflow opens
five repositories in one such surface. Agent-kit currently installs eleven
generic unprefixed skill names, so two kit-equipped repositories can shadow one
another.

The accepted Task 006 verification foundation now makes this installer slice
reviewable across Python 3.11–3.13. The current installer has a fixed 22-file
allowlist and strong collision/rollback guarantees, but it cannot preview a
write, select future payload groups, record how a target was configured, or
diagnose missing and modified files. IntrinsicEngine supplies evidence that
slug rendering, dry-run, and doctor mechanics are feasible, while its
overwrite-capable behavior remains explicitly excluded.

## Success Criteria

1. `install_agent_workflow.py install <target> --slug acme` creates
   `.agents/skills/acme-<name>/` directories whose frontmatter `name:` values
   match their directories, renders the `AGENTS.md` routing section with the
   prefixed names, leaves no unprefixed skill-name tokens in the installed
   naming surfaces, and produces a target whose installed validator exits 0.
2. `--dry-run` prints the complete selected write plan and every collision,
   exits according to the kit-wide convention, and writes nothing, proven by a
   before/after filesystem snapshot.
3. `doctor <target>` is read-only, classifies immutable manifest entries as
   `OK`, `MODIFIED`, or `MISSING`, classifies user-owned state/templates as
   `PRESENT` or `MISSING`, reports install-receipt state under the selected
   policy, and exits 0 when clean or 1 when it finds issues.
4. Manifest schema v2 validates named groups; the existing 22 payload files
   form `core`; repeated group/profile selection produces the correct union;
   collision preflight covers that full union; and exact-collision refusal,
   blocking-ancestor refusal, exclusive creation, and rollback remain covered
   and passing under the new CLI.
5. The CLI consistently uses exit 0 for success, 1 for findings or operational
   failure, and 2 for usage/environment/schema errors.
6. `./scripts/verify.sh` passes, README installation and expected-layout
   guidance describes the selected interfaces, and an end-to-end disposable
   target passes install, installed validation, clean doctor, tamper detection,
   and no-write checks.

## Constraints

- Do not add overwrite, update, uninstall, or repair behavior. Doctor diagnoses
  only.
- Preserve the fixed-allowlist boundary, refusal on any exact or
  blocking-ancestor collision, exclusive file creation, rollback ownership,
  target Git metadata, and the current 22 payload files in the default `core`
  group.
- Use the kit-wide exit convention: 0 pass, 1 failure/findings, 2
  usage/environment/schema error.
- Rewrite only the eleven known skill-name tokens and only in backtick-quoted
  occurrences, frontmatter `name:` lines, and destination directory names.
  Never rewrite prose words such as “implementation” outside backticks.
- Validate slugs as `^[a-z][a-z0-9-]*$` with a maximum of 24 characters if the
  slug interface is selected.
- Implement mechanics in agent-kit's tested standard-library style; do not
  vendor donor code.
- Do not begin implementation or infer defaults until both pending human
  decisions are recorded.

## Non-Goals

- New payload content for the later validator, task-tree, evidence, or growth
  profiles.
- Any target-repository installation pilot.
- Overwrite, forced update, uninstall, or doctor repair.
- Vendoring or importing IntrinsicEngine's broader `tools/agentkit` generator
  platform.
- Resolving the separate single-product convergence direction.

## Selected Skills

- `task-orchestration`
- `implementation`
- `code-audit`
- `handoff`

## Current Evidence

- Accepted Task 006 supplies a green five-stage source gate with 64 tests and a
  Python 3.11–3.13 CI matrix.
- `distribution/manifest.json` is schema v1 with one explicit 22-file list; all
  eleven skills currently retain generic unprefixed destinations.
- `scripts/install_agent_workflow.py` has one positional install path, validates
  safe sources/destinations, rejects all collisions before writing, uses
  exclusive creation, rolls back only owned paths, and has no dry-run, group,
  receipt, or doctor behavior.
- Six distribution regressions cover the clean payload, fresh installation,
  exact collisions, blocking ancestors, nonexistent targets, and copy-failure
  rollback.
- `scripts/validate_agent_workflow.py` discovers routed names from `AGENTS.md`
  rather than hardcoding them, so consistent rendering of routing,
  frontmatter, and directories can preserve validation.
- Four sibling repositories provide observed multi-repository prefixing
  evidence; the current problem does not require new profiles, a generator
  platform, or an overwrite path.

## Minimal Plan

1. Record the owner's D6.2 prefix-policy and D6.4a doctor-receipt decisions,
   including date and consequences. Then restore `Mode: Implement`,
   `Status: In progress`, and `Turn: driver` before any code change.
2. Introduce and validate manifest schema v2 with named groups, migrate the
   unchanged 22-file payload to `core`, and update distribution fixtures.
3. Implement bounded install-time rendering for the selected slug policy and
   add snapshot, leakage, invalid-slug, and installed-validator tests.
4. Add `--dry-run` on the same selected payload/preflight path and prove a
   byte-for-byte unchanged target for clean and colliding plans.
5. Implement the selected receipt policy and read-only `doctor`, covering clean,
   tampered immutable file, missing file, user-owned template, and missing
   receipt scenarios.
6. Update README CLI, migration, and expected-layout guidance without adding
   future profile content.
7. Run focused and full verification plus a disposable Git-target end to end;
   perform a Driver code audit; commit each bounded slice; and hand the fixed
   branch to Reviewer `codex-b`.

## Status

In review

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

### Question

D6.2 prefix policy: should project slug prefixing be the safe default or an
optional behavior?

### Options

1. **Require `--slug`, with explicit `--no-prefix` escape.** Every install must
   make the naming choice visible. The normal path avoids cross-repository
   shadowing; deliberate single-repository users can opt out. This is a
   breaking CLI change and requires one extra argument or explicit escape.
2. **Keep unprefixed installation as the default and make `--slug` optional.**
   Existing command ergonomics remain familiar, but unattended/default use
   silently reproduces the observed multi-repository collision hazard and
   makes safe naming dependent on every caller remembering an option.

### Recommendation

Option 1: require `--slug` with an explicit `--no-prefix` escape. The observed
operating mode is multi-repository, so safety should be the normal path and
unprefixed installation should require an intentional choice.

### Decision

Option 1 selected. The repository owner replied "1, 1", requiring `--slug`
for the normal install path and retaining `--no-prefix` as the explicit escape
hatch.

### Date

Decided 2026-07-29.

### Question

D6.4a doctor receipt policy: what target-owned record, if any, should define
the installed configuration and drift boundary?

### Options

1. **Write `.agents/kit-install.json` with bounded ownership.** Record manifest
   version and hash, selected slug/prefix mode and groups, installation
   timestamp, and per-file hashes for immutable payload. Doctor hashes
   immutable files, checks user-owned state/templates for presence only, and
   reports a missing receipt as `unknown installation` while falling back to
   presence checks. The generated receipt joins collision preflight. This
   diagnoses meaningful drift without flagging normal task/state edits.
2. **Write a receipt and hash every installed file.** Doctor gets full
   byte-for-byte comparison, but normal edits to user-owned task state and
   documentation templates become false `MODIFIED` findings and blur the
   ownership boundary.
3. **Write no receipt.** Doctor can check presence only and avoids one generated
   target file, but cannot reliably identify the manifest/configuration used or
   distinguish modified immutable payload from a clean install.

### Recommendation

Option 1: write `.agents/kit-install.json`, hash immutable payload only, treat
user-owned templates as presence-only, and use the explicit
missing-receipt/unknown-install fallback. This retains diagnostic value while
respecting target ownership after installation.

### Decision

Option 1 selected. The repository owner replied "1, 1", authorizing
`.agents/kit-install.json` with immutable-payload hashes, presence-only checks
for user-owned templates, and the missing-receipt unknown-install fallback.

### Date

Decided 2026-07-29.

## Handoff Log

Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`.

### Escalation (codex-a, Driver)

#### Trigger

Task 007 is a consequential interface decision followed by implementation.
Prefix defaults affect collision risk and CLI compatibility; receipt ownership
affects what doctor may label as drift. Neither choice can be inferred from the
planning reference.

#### Evidence

The current 22-file installer is non-overwriting and collision-safe but has no
prefix, preview, configuration receipt, or diagnostic mode. Multi-repository
skill shadowing is now observed, while target state/templates are explicitly
user-owned after installation.

#### Options and recommendation

The complete alternatives and consequences are recorded under Human Decisions.
Recommend required `--slug` with explicit `--no-prefix`, plus a bounded
`.agents/kit-install.json` receipt that hashes immutable payload and treats
user-owned templates as presence-only.

#### Recommended next action

The repository owner answers both pending questions. Driver `codex-a` records
the answers and date, restores the implementing state, and only then begins the
smallest manifest-and-renderer slice.

### Handoff (codex-a, Driver)

#### Objective

Independently falsify the Installer v2 implementation at fixed implementation
tip `e562259`: schema-v2 group selection, required naming choice and bounded
slug rendering, receipt-inclusive dry-run/install behavior, and read-only
doctor diagnostics, while confirming every pre-existing collision, ownership,
rollback, and target-Git guarantee remains true.

#### Changes

- Commit `5ceaceb` migrates the unchanged 22-file payload to manifest schema v2
  group `core`, adds strict group/source/destination validation and stable group
  union, replaces the old positional CLI with `install`, requires `--slug` or
  explicit `--no-prefix`, and renders only the eleven approved skill tokens in
  directory names, exact frontmatter names, and single-backtick naming
  surfaces.
- Commit `c3c4fcb` makes one rendered plan authoritative for install and
  `--dry-run`, adds the collision-protected generated
  `.agents/kit-install.json`, preserves exclusive creation and owned-path
  rollback through receipt failure, and adds receipt-backed `doctor` plus the
  missing-receipt unknown/presence fallback. Immutable paths reached through
  symlinked ancestors cannot pass integrity checks.
- Commit `e562259` updates README installation, migration, receipt, doctor,
  layout, and exit-code guidance and adds the durable Driver code audit at
  `docs/audits/installer-v2.md`.
- `tests/test_distribution.py` now has 24 focused cases spanning every success
  criterion and named failure mode. No payload content, ARA file, dependency,
  update/overwrite/uninstall/repair interface, or target pilot was added.

#### Evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_distribution.py -v`: 24/24
  passed at `e562259`.
- `./scripts/verify.sh`: all five gates passed at `e562259`; Ruff lint and
  format were clean, workflow state and 14 ARA claims validated, and 82/82
  regressions passed.
- Separate disposable Git target: slugged install wrote 22 payload files plus
  receipt; the installed validator found 11 valid skills and zero archives;
  doctor exited 0 clean; after an `AGENTS.md` edit it reported `MODIFIED` and
  exited 1; the target remained on `main` at its original HEAD.
- Snapshot tests prove clean and colliding dry runs and every exercised doctor
  path write nothing. Fault injection proves rollback after both a mid-payload
  copy failure and a partial final receipt write.
- `jq` reports manifest version 2, only group `core`, and `core_count: 22`.
  `git diff --check 5262f9d..e562259` passed. The complete task diff contains
  only `README.md`, `distribution/manifest.json`,
  `docs/audits/installer-v2.md`, `scripts/install_agent_workflow.py`, and
  `tests/test_distribution.py`; no `ara/` or `.ara/` path changed.

#### Assumptions

- The receipt is a local drift baseline, not a signature against an actor who
  can rewrite both receipt and payload.
- Files sourced from `distribution/templates/` are user-owned after install;
  all other selected payload files are immutable for doctor accounting.
- Single-backtick spans are the naming surfaces present in the approved
  22-file payload. Ordinary prose tokens intentionally remain unprefixed.

#### Uncertainties

- A missing receipt cannot recover hashes or optional profile selection. The
  fallback can recognize current unprefixed or valid slug-prefixed `core`
  skills, but deliberately reports the installation as unknown.
- Preflight plus exclusive creation is not an adversarial transaction. An
  uncatchable termination can leave installer-created paths, and concurrent
  target mutation can force refusal or rollback.
- Local evidence used Python 3.12. The existing branch CI matrix is responsible
  for independent Python 3.11 and 3.13 reproduction after push.

#### Review Focus

1. Attempt to falsify the rewrite boundary: all routing/frontmatter/directory
   names must be prefixed while prose remains unchanged and the installed
   validator passes.
2. Challenge no-write and ownership guarantees for colliding dry runs,
   receipt collision, partial receipt failure, symlink ancestors, and doctor
   paths.
3. Audit receipt schema/path validation and verify modified user templates do
   not become false immutable findings.
4. Confirm the breaking CLI and exit 0/1/2 behavior match both recorded human
   decisions and README, without an implicit unprefixed or repair path.
5. Inspect the complete diff for unnecessary abstraction or accidental scope
   expansion, and reproduce the focused suite plus `./scripts/verify.sh`.

#### Recommended Next Action

Reviewer `codex-b` checks the fixed branch tip, records an independent
structured verdict, and returns `Turn` to `driver`. Any required revision
should name a reproducer and the smallest failing contract.

### Session Completion (codex-a, Driver)

#### Work completed

Implemented all approved Installer v2 behavior, regression coverage,
documentation, and durable code audit in three bounded commits; completed the
Driver self-audit and prepared the branch for independent review.

#### Evidence

Focused distribution suite 24/24; full five-stage verification 82/82; separate
disposable Git install/validate/doctor/tamper probe passed; fixed-tip diff and
22-file `core` boundary inspected.

#### Files changed

- `distribution/manifest.json`
- `scripts/install_agent_workflow.py`
- `tests/test_distribution.py`
- `README.md`
- `docs/audits/installer-v2.md`
- `.agents/state/current-task.md` (handoff metadata only)

#### Tests or experiments run

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_distribution.py -v`
- `./scripts/verify.sh`
- Disposable Git target: slugged install, installed validator, clean doctor,
  induced immutable drift, doctor finding, Git HEAD/branch comparison
- Manifest version/group/core-count query, fixed-tip diff check, CLI help and
  ARA-path scope inspection

#### Known limitations

Receipt integrity is unsigned; missing-receipt fallback is presence-only and
cannot infer optional profiles; filesystem preflight is cooperative rather
than transactional. No overwrite, update, uninstall, or repair behavior exists.

#### Unresolved questions

None for Driver implementation. Independent Reviewer verdict and CI matrix
results remain pending.

#### Repository state updated

Yes

#### Recommended next action

Reviewer `codex-b` begins with this Handoff Log and fixed implementation tip
`e562259`, reproduces the evidence, and records a verdict before any Driver
closeout.
