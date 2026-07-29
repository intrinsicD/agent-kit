# Current Task

## Title

Implement generic validator pack and target CI template

## Task ID

008

## Role Assignment

- Driver: codex-b
- Reviewer: codex-a
- Turn: none

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

Accepted with follow-up

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

After two complete non-accepting review rounds, should Task 008 receive one
bounded third correction/review cycle for the sole remaining anti-drift test
gap, or close without merging?

### Options

1. **Authorize one bounded exception cycle.** Change only the workflow-test
   run-key detector so it recognizes `run:` both at the start of a sequence
   item and after `name:`, and add named scalar plus named `run: |` mutation
   regressions. Re-run focused/full/CI and one final independent review. This
   changes no shipped file or runtime behavior.
2. **Stop and close Task 008 as Inconclusive.** Do not merge the task branch;
   preserve the evidence and metadata-only closeout. Main remains at the
   accepted Task 007 baseline, so the entire validator profile stays
   unavailable despite the four accepted correction groups and green install
   path.

### Recommendation

Option 1. The remaining defect is isolated to one test helper: its regex
requires `run` to begin a YAML sequence item. Making that leading sequence
marker optional and adding the two exact named-step regressions is a bounded,
test-only correction with no product, dependency, manifest, or installer
impact. If the authorized final review still does not accept, close or
escalate rather than extend again.

### Decision

On 2026-07-29, the repository owner directed: “commit all changes. merge into
main and push to remote.” This accepts Task 008 with follow-up and authorizes
the Driver to merge the reviewed branch despite the known named-step
anti-drift mutation-test gap. The gap must remain recorded as validated
follow-up work; this decision does not claim that the missing regression was
implemented.

### Date

Escalated and decided 2026-07-29.

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

### Handoff (codex-b, Driver, Round 2)

#### Objective

Re-test all five Round 1 correction groups at fixed revision tip
`74e05f91a5dbaf5e4f0dd91e1a1bbcb25d987e89`, then independently decide whether
the authority, Markdown, docs-sync, and CI anti-drift contracts are now
acceptable without broadening the Task 008 scope.

#### Changes

1. `.codex/config.yaml` contract matching now removes YAML comments while
   preserving quoted `#` characters, so comment-only `AGENTS.md` text fails
   and a visible configuration value passes.
2. Each present Markdown directory scan root is resolved and containment
   checked before enumeration, closing both empty and populated external
   symlink cases.
3. Inline link text now recognizes balanced and backslash-escaped brackets,
   while same-line inline code is masked so Markdown-like examples do not
   become false links. Balanced destination parentheses remain supported.
4. Every docs-sync glob is compiled while TOML rules load; malformed or
   unterminated character classes become deterministic configuration exit 2
   before explicit-file or Git-diff evaluation.
5. Target-workflow tests now admit exactly one detected `run` directive and
   reject relisted checker stages with normal, spaced, or quoted YAML keys.

#### Evidence

- `./scripts/verify.sh` passes at the revision tip: Ruff, workflow validation,
  live strict authority and link checks, 15 ARA claims, and 109/109
  regressions.
- Focused revision suites pass 19/19 validator-pack, 30/30 distribution, and
  7/7 verification tests.
- The four new validator test methods reproduce comment-only configuration,
  empty/populated external roots, balanced/escaped labels, and malformed glob
  behavior under both explicit-file and empty Git-diff inputs. The tightened
  existing workflow test exercises three alternate relisting spellings.
- The disposable `core` + `verify` test still passes its installed four-stage
  gate, receipt ownership counts, executable-mode check, and clean doctor.
- GitHub Actions runs `30450434885` (implementation correction) and
  `30450478327` (final revision tip) both passed the verbatim gate on Python
  3.11, 3.12, and 3.13.
- `docs/audits/validator-pack.md` maps each Round 1 finding to its bounded
  disposition and retains the unchanged residual-risk boundary.

#### Assumptions

- Comment-aware text filtering is intentionally not a general YAML parser; the
  contract is the visible repository-relative `AGENTS.md` token.
- Inline-link parsing remains line-bounded and does not claim full CommonMark.
- Docs-sync glob syntax remains the documented repository-path subset, with
  invalid syntax rejected before change-set availability matters.

#### Uncertainties

- Cross-line code spans and link text, raw HTML, autolinks, and fragment
  validation remain outside the accepted scanner scope.
- The POSIX/Linux, UTF-8, committed-`--base`, and non-adversarial filesystem
  boundaries are unchanged.

#### Review Focus

- Re-run the exact five Round 1 counterexamples and nearby positive controls,
  especially quoted YAML `#`, internal scan-root aliases, bracket nesting and
  inline code, valid negated/ranged glob classes, and empty diffs.
- Mutate the workflow with alternate `run` key spacing/quoting or block
  commands and confirm the assertion rejects every extra executable step.
- Reconfirm the final manifest, installed gate, doctor ownership/modes, live
  source gate, and absence of scope expansion.

#### Recommended Next Action

Reviewer `codex-a` reproduces the fixed tip independently and records a Round 2
structured verdict. If any correction group still fails, return only the exact
remaining counterexample; otherwise accept and return `Turn: driver` for
merge/closeout.

### Review (codex-a, Reviewer, Round 2)

#### Verdict

Revision required

#### Self-reviewed

No

#### Correctness

Revision tip `74e05f91a5dbaf5e4f0dd91e1a1bbcb25d987e89` closes the
authority-comment, scan-root containment, balanced-link-label, and eager-glob
validation findings from Round 1. It also catches compact, spaced, quoted, and
compact block-form relisted `run` directives. One bounded counterexample keeps
Success Criterion 4 unproved:

```yaml
- name: Relisted authority
  run: python3 scripts/check_authority.py --root . --strict
```

The equally valid block form is also missed:

```yaml
- name: Relisted authority
  run: |
    python3 scripts/check_authority.py --root . --strict
```

`workflow_run_directives()` anchors every detected key at `^-`, so a `run` key
is counted only when it is the first key of the sequence-item mapping.
Appending either named step above leaves its result exactly
`("- run: ./scripts/verify.sh",)`. The assertion in
`test_target_ci_invokes_only_the_target_verify_entry_point` therefore still
passes while the workflow relists a delegated checker stage. The shipped
workflow itself remains clean; the defect is in the required anti-drift
regression guarantee.

#### Evidence Quality

- Independent `./scripts/verify.sh` passed Ruff, workflow validation, strict
  live authority and link checks, all 15 ARA claims, and all 109 regressions.
  Focused suites independently passed 19/19 validator-pack, 30/30
  distribution, and 7/7 verification tests.
- Exact Round 1 probes now reject a comment-only Codex contract reference,
  empty and populated external `docs` symlinks, nested and escaped missing-link
  labels, and malformed `[z-a]`, `[!]`, and `[unterminated` classes in both
  `trigger` and `one_of` before explicit-file or empty-Git-diff evaluation.
- Nearby positive controls pass for plain, quoted, and quoted-`#` visible YAML
  references; empty and populated internal scan-root aliases; inline-code
  masking; existing balanced and escaped destinations; and valid ranged and
  negated character classes under explicit files and an empty Git diff.
- Workflow mutations with compact, spaced, quoted, and compact block-form
  `run` keys are detected. Named scalar and named block-form steps reproduce
  the sole remaining bypass above.
- A fresh committed disposable Git target received 28 `core` + `verify`
  payload files and a receipt. Its installed four-stage gate and doctor exited
  0; the receipt classified 16 immutable files and 12 user-owned templates;
  `0755`/`0664` modes were exact; and target HEAD, branch, and seed content
  remained unchanged.
- The Task 007 `core` mapping remains byte-for-byte equal at 22 rows, and the
  `verify` group remains the intended six physical sources. Revision scope is
  limited to the three checker fixes, two test files, README, and the validator
  audit; `git diff --check e57d88e..74e05f9` passes. The handoff commit changes
  only this task record.
- The two recorded green Python 3.11–3.13 CI runs could not be independently
  re-opened during this review because the GitHub API was unreachable. This
  does not change the local counterexample or verdict.

#### Simplicity

The implementation remains bounded to three standard-library checkers and
three target-owned templates, with no dependency, core, or policy expansion.
The remaining correction belongs only in the existing workflow assertion; it
does not justify a YAML framework or a new validation interface.

#### Missing Cases

The documented exclusions for cross-line Markdown constructs, raw HTML,
autolinks, fragments, non-POSIX/non-UTF-8 behavior, working-tree inference, and
concurrent filesystem mutation remain acceptable. Named workflow steps are
ordinary syntax inside the claimed interface and are not covered by those
exclusions.

#### Required Changes

1. Make the target-workflow anti-drift assertion count executable `run` mapping
   keys when they follow another step key, not only when `run` begins the
   sequence item. Add both named scalar and named `run: |` block regressions,
   retain the existing spelling controls, and update the audit disposition
   after the complete mutation set passes.

#### Optional Improvements

None. Keep the correction within the existing test surface.

### Session Completion (codex-a, Reviewer, Round 2)

#### Work completed

Independently reviewed the fixed revision and Driver handoff, reran every Round
1 failure plus adjacent positive controls, audited the changed implementations
and regressions, reproduced the source/focused/disposable evidence, and
falsified the remaining target-workflow anti-drift claim without changing
implementation or tests.

#### Evidence

Four Round 1 correction groups now pass completely. The fifth catches four
alternate `run` spellings but misses both ordinary named scalar and named block
steps. Full and focused gates remain green, so the structured Review above
separates the passing implementation evidence from the one unclosed regression
guarantee.

#### Files changed

- `.agents/state/current-task.md`

No implementation, test, manifest, template, README, or audit file was changed.

#### Tests or experiments run

- `./scripts/verify.sh`
- Focused validator-pack, distribution, and verification unittest discovery
- Authority comment/visible/quoted-reference probes
- Empty/populated internal and external scan-root symlink probes
- Nested/escaped label, inline-code, and balanced-destination probes
- Malformed and valid ranged/negated glob probes under explicit files and
  empty Git diffs
- Compact, spaced, quoted, compact-block, named-scalar, and named-block
  workflow mutation probes
- Independent manifest baseline/mode and disposable
  install/gate/doctor/ownership/Git probe
- Revision/handoff scope and whitespace checks

#### Known limitations

The accepted residual boundaries listed in the Review are unchanged. GitHub
Actions run metadata was unavailable for independent reinspection because the
API connection failed.

#### Unresolved questions

None. The remaining counterexample has a bounded, test-only disposition and
does not require a product or architecture decision.

#### Repository state updated

Yes

#### Recommended next action

Driver `codex-b` closes only the named-step detection gap, adds the two
regressions above, reconciles the durable audit, reruns focused/full/CI and
disposable evidence, and returns the fixed commit for the next independent
review.

### Escalation (codex-b, Driver, after Round 2)

#### Trigger

Task 008 has received two complete independent `Revision required` verdicts.
Repository policy requires human authorization rather than beginning a third
cycle automatically.

#### Evidence

Round 2 independently accepted the authority-comment, external scan-root,
balanced/escaped label, and eager-glob corrections. All 109 regressions,
focused suites, and the disposable 22+6 install/gate/doctor controls pass.
The sole remaining failure is that `workflow_run_directives()` recognizes
`- run: ...` but misses ordinary named steps whose following line is
`run: ...` or `run: |`. The shipped workflow itself is clean; the gap is only
in the mutation-resistance regression required by Success Criterion 4.

#### Options and recommendation

The full alternatives and consequences are recorded under Human Decisions.
Recommend one explicitly authorized, test-only correction and final
independent review.

#### Recommended next action

The repository owner selects option 1 or 2. The receiving Driver records the
answer and date, restores the paired role/status fields, commits that decision,
and only then either performs the bounded correction or executes the
metadata-only Inconclusive closeout.

### Review (repository owner, Human promotion)

#### Verdict

Accepted with follow-up

#### Self-reviewed

No

#### Correctness

The repository owner accepts the Task 008 implementation for merge. The
shipped target workflow contains only the delegated `./scripts/verify.sh`
entry point, all checker and installer behavior passed the recorded review
controls, and four of the five Round 1 correction groups were independently
closed. This promotion does not overrule the factual Round 2 counterexample:
the test helper still misses a relisted checker when `run:` follows `name:`.

#### Evidence Quality

The acceptance is bounded by the evidence already reproduced independently:
109/109 unified regressions, 19/19 validator-pack tests, 30/30 distribution
tests, 7/7 verification tests, a clean disposable 22+6 install/gate/doctor
probe, and green Python 3.11–3.13 CI at revision tip
`74e05f91a5dbaf5e4f0dd91e1a1bbcb25d987e89`. The known named-step mutation
counterexamples remain preserved in the Round 2 Review.

#### Simplicity

The accepted implementation remains the smallest opt-in validator profile:
three standard-library checkers and three target-owned templates, with no
dependency, `core`, or policy expansion.

#### Missing Cases

Named scalar and named block-form workflow steps are not covered by the
current anti-drift mutation-test helper. The shipped workflow is clean, but
the regression guarantee in Success Criterion 4 is incomplete for those two
ordinary YAML forms.

#### Required Changes

None before the owner-authorized merge. Preserve the named-step detector and
two exact mutation regressions as a validated follow-up item.

#### Optional Improvements

When prioritized, make the run-key detector recognize `run:` after another
step key and add named scalar plus named block-form mutation regressions
without changing shipped runtime behavior.
