# Audit: Verification foundation

## Scope

Task 006's Ruff pin and configuration, five-stage verification entry point,
ARA ledger checker and fixtures, GitHub Actions matrix, documentation, and
maturity-plan corrections.

## Findings

1. The plan's first indicative task ID was already occupied by the accepted
   cross-repository revalidation. The verification foundation therefore binds
   to actual task 006.
2. The proposed claim-heading rule rejected the live ledger's
   `## Scope and remediation` heading. The heading is now level three, leaving
   every level-two heading available for claims.
3. The live `ara/PAPER.md` advertises layers with Markdown links, while donor
   checkers scan backticked paths. The implementation validates the actual
   Markdown link destinations, including image destinations.
4. The live environment used to reproduce and clear the format debt is Ruff
   0.15.20, not the plan author's 0.15.8 probe. The implemented toolchain pins
   0.15.20.
5. Round 1 independent review found four bypasses: inconsistent punctuated
   status handling, proof paths escaping through traversal or symlinks,
   punctuated unknown fields being ignored, and duplicate gate commands
   escaping the stage-list regression. Commit `04322dc` closes each bypass
   with a focused regression.
6. No further correctness, API, or maintainability defect was found in the
   Driver's revision audit after 21 checker fixtures, four verification tests,
   the full suite, and disposable counterexample probes.

## Severity

The four plan mismatches and four Round 1 review findings were blocking but are
corrected in the reviewed branch history. No unresolved Driver-audit finding
remains; independent Round 2 review is still required.

## Evidence

- `./scripts/verify.sh`: pass with 61 tests after the Round 1 revision.
- `scripts/check_ara.py`: pass on 13 live claims.
- `tests/test_check_ara.py`: valid fixture plus one or more negative fixtures
  for every documented checker invariant, including punctuated status/fields
  and traversal/symlink proof escapes.
- Disposable archive probes: lint, format, workflow-state, ARA-proof, and unit
  test mutations each stop the corresponding stage with exit 1.
- GitHub Actions runs `30438019981` (initial) and `30439177610` (Round 1
  revision): success on Python 3.11, 3.12, and 3.13.
- `distribution/manifest.json` is unchanged from `main`.

## Required Fixes

Round 1's four required fixes are implemented at `04322dc`. No Driver-identified
fix remains before Round 2 independent review.

## Optional Improvements

Reference-style Markdown links could be added if `ara/PAPER.md` starts using
them. Git commit proof references could be resolved if a future requirement
permits a Git dependency.

## Residual Risks

- Local paths are recognized only under the repository roots enumerated in
  `scripts/check_ara.py`; other proof text is deliberately treated as context.
- Commit-shaped proof entries are accepted syntactically and are not resolved
  through Git, as required by the task constraint.
- `scripts/verify.sh` is POSIX-only.
- CI action dependencies use current major tags rather than immutable commit
  hashes, matching the scoped plan but leaving the usual mutable-tag
  supply-chain risk.

## Verdict

Ready for independent falsification; this Driver audit is not acceptance.
