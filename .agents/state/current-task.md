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

Revision required

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

### Handoff (codex-b, Driver)

#### Objective

Independently falsify the generic validator pack at fixed implementation tip
`a14d5547cec70e4de7799cd63b1dda3eb917ee0c`: checker correctness and exit
semantics, the unchanged 22-file `core`, the six-file opt-in `verify` profile,
receipt ownership, the installed four-stage gate, and the target workflow's
single-command anti-drift property.

#### Changes

- Added standard-library `check_authority.py`, `check_doc_links.py`, and
  `check_docs_sync.py` with `--root`, warning/strict behavior, and the accepted
  0/1/2 exit convention.
- Expanded the source gate from five to seven stages by adding strict authority
  and document-link checks.
- Added the six-file `verify` manifest group: three immutable checker sources
  plus user-owned rules, target-gate, and `agent-workflow.yml` templates.
- Added live-tree, induced-failure, TOML schema, safe-path, merge-base,
  glob/parser, installed-gate, receipt, executable-mode, and CI anti-drift
  regressions.
- Updated README installation and CI guidance and recorded the Driver audit in
  `docs/audits/validator-pack.md`.

#### Evidence

- `./scripts/verify.sh`: pass at the implementation tip; Ruff lint/format,
  workflow validation, strict live authority and link checks, 14-claim ARA
  validation, and all 105 regressions pass.
- Focused suites: 15 validator-pack, 30 distribution, and seven verification
  tests pass.
- Disposable Git probe: slugged `core` + `verify` installed 28 payload files;
  the target gate passed all four stages; doctor reported 16 immutable files
  `OK`, 12 templates `PRESENT`, and zero findings.
- Induced fixtures prove warning/strict distinctions: authority and link
  findings return 0/1; docs-sync findings return 0/1; unavailable change sets
  return 0/2; malformed TOML, unsafe paths, option-like bases, and invalid
  roots return 2.
- GitHub Actions run `30448167432` passed the verbatim source gate on Python
  3.11, 3.12, and 3.13 at the implementation tip.

#### Assumptions

- `AGENTS.md` is the physical canonical contract. `CLAUDE.md` is optional and
  may either symlink to it or contain the exact documented redirect marker.
- Docs-sync policy is target-owned and empty by default. Once rules exist,
  callers supply either explicit files or a Git base; inability to establish a
  change set is warning-only outside strict mode and an environment error in
  strict mode.
- A Git-base comparison covers committed paths from merge base through `HEAD`;
  working-tree and untracked paths use `--files`.

#### Uncertainties

- The Markdown scanner intentionally does not implement all CommonMark, raw
  HTML links, autolinks, or heading-fragment validation.
- The evidence remains POSIX/Linux and UTF-8 bounded; Windows, concurrent
  adversarial mutation, and non-UTF-8 Git paths are not approved.
- No target-specific docs-sync rule has been promoted, so the mechanism is
  tested but the shipped policy deliberately makes no behavioral claim.

#### Review Focus

- Try to bypass single-authority detection with dangling, chained, external,
  or dual symlinks and malformed skill frontmatter.
- Challenge Markdown containment, balanced/escaped destinations, fenced code,
  reference definitions, and scan-root coverage.
- Challenge TOML type/schema handling, `*`/`**`/`?`/character-class matching,
  rename accounting, unsafe refs and paths, no-Git behavior, and merge-base
  completeness.
- Confirm manifest ownership and modes, `core` count, installed slug rendering,
  clean doctor output, and that target CI contains exactly one
  `./scripts/verify.sh` invocation with no relisted gates.

#### Recommended Next Action

Reviewer `codex-a` checks out the handoff commit, reproduces the fixed
implementation tip and disposable install independently, adds adversarial
probes beyond the Driver fixtures, and records an evidence-based verdict.

### Review (codex-a, Reviewer, Round 1)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

Implementation tip `a14d5547cec70e4de7799cd63b1dda3eb917ee0c`
provides a working opt-in profile and preserves the accepted Installer v2
contracts, but five bounded counterexamples prevent acceptance:

1. `.codex/config.yaml` is searched as raw text. A file containing only
   `# AGENTS.md` plus unrelated configuration passes strict authority checking,
   although a YAML comment is not an effective reference to the contract.
2. `check_doc_links.py` verifies containment only after discovering a Markdown
   file. A `docs` scan root symlinked to an empty directory outside the
   repository therefore exits 0 with two scanned files and zero findings,
   violating the bounded-root contract.
3. The flat link-start expression silently skips valid Markdown link text with
   balanced or escaped brackets. Both
   `[outer [inner]](missing.md)` and
   `[outer \[inner\]](missing.md)` exit 0 with zero links rather than reporting
   the missing destination. These are standard link-text forms under the
   [CommonMark link rules](https://spec.commonmark.org/spec#links); supporting
   them does not require a full CommonMark implementation.
4. Docs-sync glob syntax is not validated when rules load. Trigger patterns
   `[z-a]` and `[!]` raise uncaught `re.error` tracebacks and exit 1 when a
   changed path is evaluated, rather than returning configuration/schema exit
   2. The same malformed `[z-a]` rule exits 0 when a Git comparison has no
   changed paths, so configuration validity incorrectly depends on input data.
5. The target-workflow anti-drift regression rejects only exact, fully spelled
   stage command strings. Adding
   `- run: python3 scripts/check_authority.py --root . --strict` alongside the
   required gate still satisfies the current test, even though it relists a
   delegated stage and violates Success Criterion 4.

The current target workflow itself contains exactly one
`./scripts/verify.sh` invocation and no duplicated stage; finding 5 concerns
the required regression guarantee.

#### Evidence Quality

- Independent `./scripts/verify.sh` passed all seven source stages at handoff
  `a4a2acc`: Ruff lint/format, workflow validation, strict live authority and
  document-link checks, 14 ARA claims, and 105/105 regressions.
- Independent focused runs passed 15/15 validator-pack, 30/30 distribution,
  and 7/7 verification tests.
- GitHub Actions run `30448167432` was inspected directly: it is tied to
  implementation tip `a14d554`, completed successfully, and ran the verbatim
  gate on Python 3.11, 3.12, and 3.13.
- A fresh committed disposable Git target received the unchanged 22-file
  `core` plus six-file `verify` payload. Installation wrote 28 payload files
  plus the receipt; the installed four-stage gate exited 0, doctor reported
  16 immutable files `OK` and 12 templates `PRESENT`, executable modes were
  preserved, and Git HEAD/branch stayed unchanged. A separate dry-run left its
  target byte-for-byte unchanged. Editing the user-owned target gate remained
  `PRESENT`; editing an immutable checker became `MODIFIED` and exit 1.
- Authority controls passed for chained `CLAUDE.md` aliases ending at
  `AGENTS.md`; external/dangling `CLAUDE.md` and skills-root aliases, a
  symlinked skill directory, a symlinked canonical contract, and ambiguous
  duplicate frontmatter names were all rejected. The comment-only Codex
  configuration above was the sole authority bypass reproduced.
- Document-link controls correctly handled balanced and escaped destination
  parentheses, angle destinations with spaces, reference definitions,
  root-relative paths, external schemes, fenced examples, external Markdown
  file symlinks, percent-encoded escapes, and non-directory scan roots. An
  escaped ASCII-space destination outside angle brackets produced a finding
  and was not promoted as a defect because that form is not a valid CommonMark
  destination.
- Docs-sync controls passed for `*`, `**`, `?`, negated character classes,
  warning/strict dispositions, unsafe explicit paths and rule paths, missing
  refs, nested Git roots, no-Git behavior, rename source/destination
  accounting, and divergent-branch merge-base semantics. Only the malformed
  character-class validation defect above failed.
- Baseline Task 007 and current `core` manifest rows compare exactly at 22;
  `verify` contains the intended six physical sources with modes `0755` for
  checkers/target gate and `0664` for rules/workflow templates.
- `git diff --check 40d0b99..a14d554` passed, and the handoff commit changes
  only `.agents/state/current-task.md`.

#### Simplicity

The profile remains bounded: three direct checkers, three target-owned
templates, no dependency, no core expansion, and no target-specific policy.
The required corrections fit the existing design: meaningful comment-aware
contract detection, scan-root containment before enumeration, balanced link
text recognition, eager glob compilation/validation, and a stronger
workflow-mutation assertion. No parser framework, profile abstraction, or
additional interface is justified.

#### Missing Cases

The documented exclusions remain acceptable: raw HTML, autolinks, heading
fragment validation, working-tree inference for `--base`, Windows/non-POSIX
behavior, non-UTF-8 Git paths, concurrent mutation, and target-specific
docs-sync policy. None explains the five reproduced cases, which occur on
ordinary Linux/UTF-8 inputs inside the approved interfaces.

#### Required Changes

1. Make `.codex/config.yaml` contract detection ignore comments (or enforce a
   comparably meaningful configuration reference) and add comment-only
   bypass/valid-reference regressions.
2. Reject or configuration-error every present Markdown scan root that
   resolves outside the repository, even when it contains no Markdown files;
   add empty and populated external-root controls.
3. Scan valid inline-link text containing balanced and backslash-escaped
   brackets, with missing/existing destination regressions. Keep the parser
   bounded to the accepted link forms.
4. Validate or compile every `trigger` and `one_of` glob while loading rules,
   translate malformed patterns to
   `DocumentationSyncConfigurationError`, and prove exit 2 independent of the
   changed-file set.
5. Harden the target CI anti-drift test so semantically equivalent relisted
   checker invocations fail, not only exact copies of the target-gate command
   strings.

#### Optional Improvements

None recommended in this round. Do not expand into full CommonMark, YAML
configuration modeling, target policy, or additional installer modes while
closing these counterexamples.

### Session Completion (codex-a, Reviewer, Round 1)

#### Work completed

Independently audited all three checkers, manifest and ownership behavior,
source/target gates, workflow template, test assertions, README contract, and
Driver audit at fixed implementation tip `a14d554`; reproduced the recorded
source, focused, CI, and disposable-target evidence; then ran adversarial
authority, Markdown, docs-sync, distribution, and anti-drift probes.

#### Evidence

The passing controls and five required correction groups are recorded in the
Review above. The full gate remains green at 105 tests, but eight exact probe
expectations fail across those five underlying defects.

#### Files changed

- `.agents/state/current-task.md`
- `docs/audits/validator-pack.md`

No implementation or test file was changed.

#### Tests or experiments run

- `./scripts/verify.sh`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_validator_pack.py -q`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_distribution.py -q`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_verification.py -q`
- Independent disposable dry-run/install/gate/doctor/mode/ownership/Git probe
- Independent authority symlink, frontmatter, and Codex-comment probes
- Independent Markdown parsing, fence, containment, and scan-root probes
- Independent TOML/glob/path/ref/no-Git/rename/merge-base probes
- Target-workflow mutation probe and GitHub Actions run `30448167432`
  inspection
- Manifest baseline mapping, implementation/handoff scope, and whitespace
  checks

#### Known limitations

The accepted out-of-scope boundaries listed in the Review remain unchanged.

#### Unresolved questions

None. The five correction groups are reproducible and do not require a human
product decision.

#### Repository state updated

Yes

#### Recommended next action

Driver `codex-b` implements only the five required correction groups, adds the
reproducing regressions, updates the durable audit, reruns focused/full/CI and
disposable-target evidence, and hands back a fixed implementation tip for
Round 2 independent review.
