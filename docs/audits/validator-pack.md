# Audit: Generic validator pack

## Scope

Driver audit and independent Reviewer Round 1 falsification of Task 008's three
standard-library checkers, source verification wiring, six-file opt-in
`verify` manifest group, target verification entry point, CI template,
installer ownership classification, and regression fixtures. The audit covers
correctness, failure semantics, path containment, Git change-set accounting,
executable modes, and interface drift. It does not approve target-specific
documentation rules or later maturity-program profiles.

## Findings

Two edge cases were found during the Driver pass and fixed before handoff:

1. The first document-link parser stopped at the first closing parenthesis.
   It now retains balanced parentheses in inline destinations, with a fixture
   that resolves a real parenthesized filename.
2. The first Git diff path could collapse a rename to only its destination.
   Docs-sync now uses `--no-renames`, validates explicit path/ref inputs before
   evaluating even an empty policy, and covers recursive and character-class
   glob behavior.

Ownership stays explicit: the three checker programs are immutable
receipt-hashed payload, while the rules file, target gate, and workflow are
user-owned templates checked for presence only. The target workflow contains
one `./scripts/verify.sh` invocation and none of the gate commands it delegates.

Independent Reviewer Round 1 reproduced five additional correction groups:

1. Comment-only `AGENTS.md` text satisfies the optional Codex configuration
   reference check.
2. An empty external directory symlink at a Markdown scan root passes.
3. Valid balanced/escaped-bracket link text can hide missing destinations.
4. Malformed docs-sync character classes can traceback as exit 1 or pass on
   an empty change set instead of producing configuration exit 2.
5. The target workflow is clean, but the anti-drift regression accepts a
   semantically equivalent relisted checker command.

Exact inputs and full dispositions are recorded in
`.agents/state/current-task.md`.

## Severity

- Critical: none.
- High: none.
- Medium: five open bounded Reviewer correction groups.
- Low: bounded parser and operating-environment limitations remain under
  Residual Risks.

## Evidence

- `tests/test_validator_pack.py` exercises live-tree passes, strict and warning
  dispositions, authority aliases and forks, skill-name drift, Codex contract
  drift, fenced and escaping links, balanced destinations, invalid TOML,
  explicit changed files, merge-base diffs, unavailable change sets, safe
  input validation, and glob semantics.
- `tests/test_distribution.py` fixes `core` at 22 files, fixes `verify` at six
  files, installs `core` + `verify` into disposable Git, runs the installed
  target gate, checks receipt ownership counts, and confirms doctor is clean.
- `tests/test_verification.py` pins all source and target gate commands and
  proves that both source and target workflows invoke their respective
  verification entry points without relisting stages.
- Focused evidence before handoff: 15 validator-pack, 30 distribution, and
  seven verification tests pass. The unified source gate passes 105 tests,
  both live strict checkers, workflow validation, Ruff, and ARA validation.
- Reviewer Round 1 independently reproduced all focused counts and the
  105-test gate, inspected green Python 3.11–3.13 CI run `30448167432`,
  repeated a committed disposable `core` + `verify` install with clean
  four-stage gate and doctor, and challenged authority symlinks/frontmatter,
  Markdown syntax/containment/scan roots, docs-sync
  TOML/globs/path/ref/merge-base/rename/no-Git behavior, manifest
  ownership/modes/core mapping, and workflow mutation resistance.

## Required Fixes

1. Reject comment-only Codex contract references.
2. Enforce scan-root containment before Markdown enumeration.
3. Recognize balanced and escaped bracket forms in valid inline link text.
4. Eagerly validate all docs-sync globs and classify malformed syntax as exit
   2 regardless of the change set.
5. Make the anti-drift regression reject alternate spellings of relisted
   checker stages.

## Optional Improvements

- Validate Markdown heading fragments only after a concrete broken-anchor
  failure justifies the additional parser surface.
- Add HTML-link and autolink scanning only if those forms become common in a
  target corpus.
- Add an automatic CI base-selection convention only after a target supplies a
  stable branch/event contract. The generic checker deliberately requires
  `--files` or `--base` once rules exist.

## Residual Risks

- Markdown scanning is intentionally bounded to inline links, images, and
  reference definitions outside fenced code. It does not implement all of
  CommonMark, validate anchors, or inspect raw HTML.
- `--base` evaluates committed paths between the merge base and `HEAD`.
  Working-tree and untracked changes require explicit `--files`.
- Warning mode intentionally returns success for findings. The target gate
  selects strict authority and link checks, while docs-sync remains warning
  mode because its shipped policy is empty and target-owned.
- Filesystem checks are not an adversarial transaction. Concurrent path
  mutation, Windows behavior, and non-UTF-8 repository paths remain outside the
  accepted evidence boundary.

## Verdict

Revision required after independent Reviewer Round 1. The overall slice remains
appropriately small and its main install/gate path works, but the five bounded
correction groups above must close before the self-enforcement and anti-drift
claims can be accepted.
