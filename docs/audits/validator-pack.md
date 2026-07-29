# Audit: Generic validator pack

## Scope

Driver audit of Task 008's three standard-library checkers, source verification
wiring, six-file opt-in `verify` manifest group, target verification entry
point, CI template, installer ownership classification, and regression
fixtures. The audit covers correctness, failure semantics, path containment,
Git change-set accounting, executable modes, and interface drift. It does not
approve target-specific documentation rules or later maturity-program
profiles.

## Findings

No required correctness finding remains open in the reviewed scope.

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

## Severity

- Critical: none.
- High: none.
- Medium: none open; both implementation-pass findings above were resolved.
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

## Required Fixes

None at Driver handoff.

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

Ready for independent review. The implementation is the smallest complete
opt-in slice in Plan 007: it adds no core payload, no target-specific policy,
and no later profile behavior.
