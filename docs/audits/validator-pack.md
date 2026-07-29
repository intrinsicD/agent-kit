# Audit: Generic validator pack

## Scope

Driver audit, two independent Reviewer falsification rounds, and the
repository owner's accepted-with-follow-up promotion of Task 008's three
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
`docs/tasks/008-validator-pack.md`.

Driver revision commit `41e9dee` closes four groups and partially closes the
fifth:

1. Codex configuration text is searched only after comment-aware filtering;
   a comment-only reference now fails while a visible value passes.
2. Every present directory scan root is resolved and checked for repository
   containment before enumeration, so empty and populated external aliases
   both fail.
3. Inline link text is scanned with balanced, backslash-aware bracket
   handling. The revision also masks same-line inline code after the stronger
   parser correctly exposed Markdown-like examples in the immutable Review
   record.
4. Every `trigger` and `one_of` glob is compiled while rules load. Invalid
   classes become configuration exit 2 before any explicit-file or Git diff
   path can affect the result.
5. The workflow assertion accepts exactly one detected `run` directive:
   `./scripts/verify.sh`. Additional direct relisted stages fail with spacing,
   quoted-key, and compact block variants. Reviewer Round 2 showed that named
   scalar and named block steps still bypass detection because their `run` key
   does not begin the sequence item.

## Severity

- Critical: none.
- High: none.
- Medium: one open test-guarantee finding. Four Reviewer correction groups are
  closed; named workflow-step mutation detection remains incomplete.
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
- Focused evidence after revision: 19 validator-pack, 30 distribution, and
  seven verification tests pass. The unified source gate passes 109 tests,
  both live strict checkers, workflow validation, Ruff, and 15-claim ARA
  validation.
- Reviewer Round 1 independently reproduced all focused counts and the
  105-test gate, inspected green Python 3.11–3.13 CI run `30448167432`,
  repeated a committed disposable `core` + `verify` install with clean
  four-stage gate and doctor, and challenged authority symlinks/frontmatter,
  Markdown syntax/containment/scan roots, docs-sync
  TOML/globs/path/ref/merge-base/rename/no-Git behavior, manifest
  ownership/modes/core mapping, and workflow mutation resistance.
- Reviewer Round 2 independently passed all four implementation corrections,
  their positive controls, 19/30/7 focused tests, the 109-test source gate,
  and the disposable install controls. Direct, spaced, quoted, and compact
  block workflow mutations were caught; named scalar and named block steps
  reproduced the remaining bypass.
- After the repository owner explicitly directed merge with the remaining gap
  preserved as follow-up, the accepted task record passed the complete
  seven-stage source gate again: both strict live checkers, 17 ARA claims,
  and all 109 regressions passed before merge.

## Accepted Follow-up

One bounded test fix remains after owner-authorized merge: count `run` mapping
keys that follow a named step and add named scalar and named block mutation
regressions. It is preserved in `.agents/state/backlog.md`; acceptance does
not claim those mutations are currently detected.

## Optional Improvements

- Validate Markdown heading fragments only after a concrete broken-anchor
  failure justifies the additional parser surface.
- Add HTML-link and autolink scanning only if those forms become common in a
  target corpus.
- Add an automatic CI base-selection convention only after a target supplies a
  stable branch/event contract. The generic checker deliberately requires
  `--files` or `--base` once rules exist.

## Residual Risks

- Markdown scanning is intentionally bounded to same-line inline links,
  images, and reference definitions outside fenced and same-line inline code.
  It does not implement all of CommonMark, validate anchors, inspect raw HTML,
  or model code spans that cross lines.
- `--base` evaluates committed paths between the merge base and `HEAD`.
  Working-tree and untracked changes require explicit `--files`.
- Warning mode intentionally returns success for findings. The target gate
  selects strict authority and link checks, while docs-sync remains warning
  mode because its shipped policy is empty and target-owned.
- Filesystem checks are not an adversarial transaction. Concurrent path
  mutation, Windows behavior, and non-UTF-8 repository paths remain outside the
  accepted evidence boundary.

## Verdict

Accepted with follow-up by repository-owner promotion on 2026-07-29 after two
independent `Revision required` rounds. The opt-in validator profile, installed
gate, clean workflow template, and four closed correction groups are accepted
for merge. Named-step mutation-test coverage remains a documented medium
follow-up and is not represented as complete.
