# Maturity Program Plan

Date: 2026-07-29

Status: **Active planning reference.** The verification foundation, Installer
v2, and generic validator pack were merged as actual tasks 006–008. Task 008
was accepted by repository-owner promotion with one bounded test follow-up;
later slices remain validated backlog, not accepted implementation. The
task-tree profile is next as actual task 009. A decision in this document
becomes accepted only when a Driver lifts it into
`.agents/state/current-task.md` under the two-agent workflow and it survives
review. Task IDs are indicative; real IDs bind at initialization ("next unused
number in `docs/tasks/`").

Provenance: requested by the repository owner. Evidence sources are the
independently reviewed cross-repository assessment
(`docs/research/cross-repository-agent-workflow-adoption.md`, task 003), a
same-day four-repository workflow inventory of `IntrinsicEngine`,
`structsplat`, `realtime-gs`, and `prospect`, and direct probes of this
repository at the plan date: validator pass, 36/36 regression tests pass,
`ruff format --check` (ruff 0.15.8) fails on the two files recorded in claim
C13, the manifest holds 22 unprefixed entries, the validator parses the
`## Skill routing` section dynamically rather than hardcoding skill names
(`scripts/validate_agent_workflow.py:171`, `:522-526`), and neither
`AGENTS.md` nor `README.md` mentions `ara/`.

Amendment (2026-07-29, task 006 initialization): proposed plan 005 binds to
actual task 006 because task 005 was already assigned to the accepted
cross-repository revalidation. The baseline was reproduced before
implementation: 36/36 tests and the workflow validator passed; the only Ruff
format failures were the two recorded files. The active environment is Ruff
0.15.20 rather than the plan author's 0.15.8 probe, so task 006 pins 0.15.20.
The live claims file also contained a non-claim level-two heading that
contradicted D5.3; task 006 normalizes it to level three. Because `ara/PAPER.md`
uses Markdown links rather than backticked layer paths, the checker validates
those actual link destinations. The owner's instruction to check, fix, and
implement this plan authorizes the proposed dependency order and Python
3.11–3.13 floor. D1 remains proposed because it affects another repository;
later interface decisions bind in their own tasks.

Amendment (2026-07-29, task 006 acceptance): after two required revision
rounds, the owner authorized one final bounded correction. Commit `2a77376`
rejects empty or punctuation-only claim statuses and detects repeated gate
commands hidden by trailing shell comments. Independent final review accepted
the slice with 64/64 local tests, green CI on Python 3.11–3.13, and no
distribution change. The complete record is
`docs/tasks/006-verification-foundation.md`.

Amendment (2026-07-29, task 007 acceptance): proposed plan 006 bound to
actual task 007. The recorded human decisions require exactly one of `--slug`
and `--no-prefix`, plus a local generated receipt for read-only doctor
diagnostics. The accepted implementation keeps the `core` mapping at exactly
22 files, adds manifest groups, dry-run, rollback-safe exclusive installation,
receipts, and doctor, and resolves all three Round 1 review findings.
Independent Round 2 review accepted implementation tip `337e5b9` at
`43845cd`; 28 focused tests and the 86-test gate passed locally, and CI passed
on Python 3.11–3.13. The accepted branch merged at `b45d101`. Plan 007 is next
and binds as actual task 008.

Amendment (2026-07-29, task 008 acceptance with follow-up): proposed plan 007
bound to actual task 008. The six-file opt-in `verify` group keeps `core` at
22 files and adds the three standard-library checkers, empty target-owned
docs-sync policy, four-stage target gate, and verbatim CI template. Two
independent review rounds closed four of five correction groups; the shipped
workflow is clean, but the mutation-test helper still misses named steps whose
`run:` key follows `name:`. The repository owner explicitly directed merge
with that gap preserved as follow-up. The 109-test source gate and disposable
`core` + `verify` install/gate/doctor path pass; the branch merged at
`c38abb5`. Plan 008 is next and would bind as actual task 009.

---

## Program goal

Evolve agent-kit from a validated two-agent coordination kernel into a
complete, installable, self-enforcing agentic workflow product of
IntrinsicEngine-grade maturity — one that can be added to a repository and
immediately gives its agents: a single cross-harness authority, durable
coordination state with enforced independent review, executable gates run by
one command and mirrored verbatim in CI, an optional evidence ledger, an
optional scalable backlog, and a documented growth loop through which the
target repository accumulates its own domain discipline.

The program deliberately does **not** copy IntrinsicEngine. It merges the two
existing halves of the ecosystem — agent-kit's coordination kernel and the
distribution/validator mechanics of IntrinsicEngine's embedded
`tools/agentkit` generator — and adds only the generic parts of the four
repositories' machinery, each gated by evidence.

## Program principles (evidence-derived)

1. **Enforced structure.** Every artifact class the kit installs gets a
   validator; one command runs all gates; CI runs that command verbatim.
   Evidence: all four repositories converge on this; the two that re-list CI
   steps instead of calling the script (realtime-gs, prospect) have measurably
   drifted, the one that calls the script verbatim (structsplat) has not.
2. **Proportionality via profiles.** The core stays small (coordination kernel
   plus verification). Task-tree, evidence-ledger, and audit layers are opt-in
   manifest groups. A near-empty repository must not inherit machinery scaled
   for 838 task files.
3. **The growth loop is the product.** IntrinsicEngine's maturity is a loop,
   not a file set: recurring failures become skills/validators that cite their
   motivating incident; new checks ratchet warning→strict under a named owner;
   a periodic rent audit retires machinery that stops earning its keep
   (their 2026-07-17 audit: keep 53, warn 2, retire 2 of 57 validators). The
   kit ships the loop as procedure; targets grow their own content.
4. **Maturity is not mass.** Cautionary evidence: IntrinsicEngine's two human
   audit cadences are lapsed ~62/~53 days against 14/42-day limits; 5 of its 6
   docs-sync rules are satisfiable by any task-file edit; realtime-gs's
   1,252-line experiment contract has never gated a real run. Every plan below
   must justify each moving part against a failure it prevents.
5. **Dogfooding is the credibility evidence.** Every program task runs through
   agent-kit's own Driver/Reviewer workflow, and every capability claim the
   kit makes about itself gets an `ara/` row bound to on-disk proof.

## Sequencing and dependencies

```
005 verification foundation ──► 006 installer v2 ──► 007 validator pack + CI template
                                        │
                                        ├──► 008 task-tree profile   (parallel with 009)
                                        ├──► 009 evidence profile    (parallel with 008)
                                        └──► 010 growth loop + process-audit skill

micro-slice M1 (skill-text hardening, part of 009) — can be pulled forward
any time after 005.
Decision D1 (single-product convergence) — human decision, needed before 006
finishes only for its IntrinsicEngine-facing consequence; 006 itself is
justified independently.
```

Rationale: 005 creates the gate that protects everything after it. 006 creates
the profile mechanism (manifest schema v2) and the slug renderer that 007–009
payload additions depend on. 008 and 009 are independent of each other. 010 is
last because its audit skill should reference the validators that exist by
then.

## Program definition of done

- [x] One command (`scripts/verify.sh`) runs every agent-kit gate; CI runs it
      verbatim on 3.11/3.12/3.13. (bound as actual task 006)
- [x] The installer is dry-runnable, doctorable, collision-refusing, and
      slug-prefix-aware; the distribution regression suite covers all of it.
      (bound as actual task 007)
- [x] A fresh install is self-enforcing on day one: authority-redirect,
      doc-link, and docs-sync checks plus a verify entry point and a CI
      workflow template ship as an opt-in profile. (actual task 008, accepted
      with a named-step mutation-test follow-up)
- [ ] A target whose backlog outgrows one file can adopt a validated,
      dependency-aware backlog directory with a generated unblocked view,
      without creating a second active-task authority. (008)
- [ ] A target can adopt a blank, checker-enforced `ara/` ledger; the claim
      schema includes the optional `Boundary` field; preregistration and
      untrusted-handoff hardening are in the skills. (009)
- [ ] The payload `AGENTS.md` documents the executable-memory growth loop and
      routes an optional `process-audit` skill. (010)
- [ ] Every gate above is covered by tests in this repository, and every
      capability claim has a ledger row.

## Program anti-goals

- No update, uninstall, or overwrite installer modes (standing decision in
  `.agents/state/state.md` — refuse-on-collision stays).
- No port of scale-bound IntrinsicEngine machinery: touched-scope CI planner,
  knowledge graph, nightly matrix, generated 14.6 KB session brief.
- No maturity-taxonomy vocabulary yet (trigger from task 003 P2 unobserved; the
  IE wording is C++/backend-flavored and needs de-domaining first).
- No skill evals harness yet (nothing runs them even in the source repos).
- No domain machinery: results-bundle/viewer gates, sealed-protocol digests,
  input-policy firewalls, benchmark manifests. These remain local extensions,
  per task 003's boundary.
- No cadence checker in 010 (see plan 010, D10.2).

## Program-level risks

| Risk | Mitigation | Where handled |
| --- | --- | --- |
| Dual authority in targets (task 003 failure mode 1) | Profiles default off; task-tree profile reuses existing active/done authorities; installer preflight refuses collisions | 006, 008 |
| Payload bloat / ceremony | Manifest groups reviewed per task; core group stays a deliberate small set; rent-audit procedure in 010 applies to the kit itself | 006–010 |
| Verify/CI mirror drift inside agent-kit | CI calls `verify.sh` verbatim; a regression test pins the stage list | 005 |
| Slug rewrite corrupts skill cross-references | Explicit token list, backtick-scoped word-boundary rewrite, snapshot tests, installed-validator-must-pass test | 006 |
| Docs-sync false positives poison trust in the gate | Ship the mechanism nearly empty of rules; warning-mode default; strict only when a target opts in | 007 |
| Plans drift from executed reality | This document is reference, not authority; the task record supersedes it, and contradictions get a dated amendment here | all |

---

## Plan 005 — Verification foundation (bound as actual task 006)

### Goal

One command runs every agent-kit gate; a GitHub workflow runs that command
verbatim; the repository's own `ara/` ledger becomes structurally enforced;
the recorded Ruff format debt is cleared and the toolchain pinned.

### Motivation and evidence

- agent-kit documents two separate verification commands (`README.md:67-86`),
  has no `.github/workflows/`, and mentions CI nowhere in authority or skills.
- Claim C13 records two files failing `ruff format --check`; reproduced at
  plan date with ruff 0.15.8. No lint config or version pin exists, so the
  acceptance evidence of task 004 depended on an ambient tool version.
- The ledger (13 claims, 31 path proofs) is clean at plan date — verified by an
  ad-hoc probe — but nothing enforces it. IntrinsicEngine's
  `check_ara_claims.py` docstring describes the situation exactly: "Every
  other agent-process artifact in this repository has a validator; this one
  did not." structsplat and realtime-gs enforce the same nine-check pattern in
  CI.
- Neither `AGENTS.md` nor `README.md` mentions `ara/` (verified at plan date),
  so agents can operate here without discovering the ledger. structsplat and
  realtime-gs both make "the authority mentions the ledger" a checked
  property.

### Mode

Implement.

### Success criteria

1. `./scripts/verify.sh` exits 0 on the clean tree and nonzero when any single
   gate is broken (demonstrated during review with one induced failure per
   gate: a lint error, a format error, an invalid state file, a broken claim
   proof path, a failing unit test).
2. `ruff format --check` passes repo-wide with the pinned version; the
   reformat of `scripts/validate_agent_workflow.py` and
   `tests/test_agent_workflow.py` lands as a mechanical-only commit separate
   from any semantic change, and all existing tests pass unchanged.
3. `scripts/check_ara.py` passes on the live ledger and fails each fixture in
   its new test module.
4. The GitHub workflow runs `./scripts/verify.sh` verbatim (no re-listed
   steps) on Python 3.11, 3.12, and 3.13 and is green on the task branch.
5. `README.md` documents the single command and mentions `ara/` as the claim
   ledger; the validator and 36 existing tests still pass.

### Constraints

- Stdlib-only Python; the only new dev dependency is the pinned `ruff`.
- Do not edit claim C13 — it is bound to archived checkouts of fixed commits
  and remains true after the reformat.
- Do not add anything to the distribution manifest in this task. `check_ara.py`
  and `verify.sh` are source-repository tooling here; generalizing them for
  targets is plans 007/009.
- Mechanical and semantic changes in separate commits (discipline adopted from
  IntrinsicEngine `AGENTS.md` §5).

### Non-goals

Target-facing verify/CI templates (007); ara templates for targets (009);
any change to skills or `AGENTS.md` payload text.

### Selected skills

`task-orchestration`, `implementation`, `code-audit` (validator/test edits),
`repo-organization` (completion), `handoff`.

### Design decisions

- **D5.1 Entry-point form.** POSIX `sh` script (`scripts/verify.sh`) with
  numbered stage banners, `set -eu`, stages ordered cheap-first:
  `ruff check` → `ruff format --check` → `validate_agent_workflow.py` →
  `check_ara.py` → `unittest discover`. Rationale: matches
  structsplat/realtime-gs convention; the suite (~5 s) runs last.
  Windows is out of scope (agent sandboxes are POSIX); note in the header.
- **D5.2 Pinning.** `requirements-dev.txt` with an exact `ruff==` pin (the
  version used to clear the debt), plus a minimal `pyproject.toml` carrying
  only `[tool.ruff] target-version = "py311"`. No other config, to keep
  reformat churn near zero. `verify.sh` fails closed with an install hint if
  `ruff` is absent.
- **D5.3 `check_ara.py` scope.** Nine checks, adapted from the
  structsplat/realtime-gs design, sized to this ledger:
  1. required files exist: `ara/PAPER.md`, `ara/logic/claims.md`,
     `ara/logic/problem.md`, `ara/logic/solution/heuristics.md`,
     `ara/staging/observations.yaml`, `ara/trace/exploration_tree.yaml`,
     `ara/trace/pm_reasoning_log.yaml`,
     `ara/trace/sessions/session_index.yaml`, `ara/evidence/README.md`;
  2. every path referenced in `PAPER.md` resolves;
  3. claim headings match `^## (C\d+): ` and IDs are unique; any other `## `
     heading in `claims.md` is an error;
  4. the nine required fields are present per claim; `Boundary` is accepted as
     a known optional field (forward compatibility with plan 009);
  5. `Status` first word ∈ {supported, refuted, untested, unavailable,
     hypothesis, superseded, withdrawn};
  6. `Dependencies` resolve to existing claim IDs, no self-dependency;
  7. `Proof` entries that look like repository paths (roots `ara/`, `docs/`,
     `scripts/`, `tests/`, `.agents/`, `distribution/`) must exist; entries
     matching `^[0-9a-f]{7,40}$` are treated as commit references and not
     resolved (documented limitation — no git dependency); a `supported` or
     `refuted` claim must cite at least one existing path;
  8. every `From staging` `O<NN>` is defined in `observations.yaml`;
  9. `README.md` mentions `ara/logic/claims.md`. The mention goes in
     `README.md`, **not** `AGENTS.md`, because `AGENTS.md` is payload and
     default targets have no `ara/`; this asymmetry is the reason the check
     targets README.
- **D5.4 CI shape.** One job, matrix `python-version: [3.11, 3.12, 3.13]`,
  steps: checkout → setup-python → `pip install -r requirements-dev.txt` →
  `./scripts/verify.sh`. Trigger: `push` and `pull_request`. No separate
  structural job (structsplat's rationale — heavy-dependency logs — does not
  apply to a stdlib repo).
- **D5.5 Prose-drift guard.** A unit test asserts `verify.sh` invokes exactly
  the five gates (string match on the script). Motivated by structsplat's live
  defect where `CLAUDE.md` claims a `ruff format --check` stage that
  `verify.sh` does not run.

### Implementation plan

1. Commit A (mechanical only): run pinned `ruff format` on the two debt files;
   run full suite; no other edits.
2. Commit B: add `requirements-dev.txt`, `pyproject.toml`, `scripts/verify.sh`.
3. Commit C: add `scripts/check_ara.py` + `tests/test_check_ara.py`
   (fixture-driven: valid ledger passes; broken proof path, unknown status,
   unresolved dependency, undefined staging ID, duplicate claim ID, stray
   heading each fail; live-tree pass test).
4. Commit D: add `.github/workflows/ci.yml`; add the verify stage-list test;
   update `README.md` (verification section, `ara/` mention).
5. Handoff with induced-failure evidence per gate; Reviewer reproduces from
   the branch.

### Validation and evidence plan

Recorded in the handoff: exit codes for clean and each induced failure;
`ruff --version`; full suite output; CI run URL. Post-acceptance ledger row
(indicative C14): "agent-kit's gates run as one command mirrored verbatim in
CI", proof = `scripts/verify.sh`, `.github/workflows/ci.yml`,
`tests/test_check_ara.py`, the task archive.

### Distribution impact

None. Manifest untouched; distribution tests must show zero diff in expected
payload.

### Risks

Reformat churn conflicting with parallel branches (none open); ruff pin going
stale (rent-audited like everything else); `unittest discover` runtime growth
(currently ~5 s, acceptable).

### Size

S–M (one session, four commits).

---

## Plan 006 — Installer v2: slug prefixing, dry-run, doctor, manifest groups (bound as actual task 007)

### Goal

Make installation configurable and diagnosable — slug-prefixed skill names,
`--dry-run`, a `doctor` subcommand, and a grouped manifest (the profile
mechanism plans 007–009 build on) — while preserving the fixed-allowlist,
refuse-on-collision, no-overwrite semantics.

### Motivation and evidence

- All four sibling repositories prefix their skills specifically to survive
  multi-repository agent sessions; structsplat and realtime-gs enforce the
  prefix by test, and structsplat's `install_skills.sh` fails closed on
  unprefixed names. The owner's sessions demonstrably open five repositories
  in one skill-discovery surface, so task 003's "target-conditioned"
  prefixing trigger is now observed. agent-kit currently installs eleven
  unprefixed generic names (`implementation`, `handoff`, …), which would
  shadow across any two kit-equipped repositories — including the planned
  realtime-gs/prospect pilots.
- IntrinsicEngine's `tools/agentkit` demonstrates the target mechanics:
  slug-driven prefixing via `[project]` config, idempotent `init`,
  `--dry-run`, and a `doctor` that reports present/missing/drifted files
  (`tools/agentkit/README.md`). Those mechanics are the donor material; its
  overwrite-capable `--force` is explicitly **not** adopted.
- Feasibility verified: `validate_agent_workflow.py` derives the routed skill
  set by parsing `AGENTS.md`'s `## Skill routing` section and comparing to
  directories on disk — no hardcoded names — so consistently rewriting both
  surfaces keeps installed validation working unmodified.

### Mode

Decide (D6.2, D6.4a) then Implement.

### Success criteria

1. `install_agent_workflow.py install <target> --slug acme` produces
   `.agents/skills/acme-<name>/` directories whose frontmatter `name:` equals
   the directory name, an `AGENTS.md` whose routing section lists the
   prefixed names, and zero occurrences of the unprefixed names anywhere in
   the installed tree; the installed validator exits 0.
2. `--dry-run` prints the full write plan and collision report and provably
   writes nothing (filesystem snapshot comparison in tests).
3. `doctor <target>` classifies every manifest entry as OK / MODIFIED /
   MISSING (state templates: PRESENT / MISSING only), reads the install
   receipt, and exits 0 clean / 1 findings — without writing anything.
4. Manifest schema v2 (named groups) validates; the current 22 files form
   group `core`; group selection unions correctly in the collision preflight;
   all existing distribution guarantees (exact-collision refusal, ancestor
   blocking, exclusive creation, rollback) hold under the new CLI and are
   re-proven by the extended test suite.
5. `./scripts/verify.sh` passes; README installation docs updated.

### Constraints

- No overwrite, update, or uninstall modes. Doctor diagnoses; it never
  repairs.
- Exit-code convention adopted kit-wide: 0 pass, 1 failure/findings, 2
  usage or environment error (IntrinsicEngine's checker convention).
- The rewrite must touch only the eleven known skill-name tokens, only in
  backtick-quoted occurrences, frontmatter `name:` lines, and directory
  names — never prose words like "implementation" outside backticks.

### Non-goals

New payload content (007–009); any target-repo pilot; vendoring
`tools/agentkit` code (mechanics are reimplemented in agent-kit's tested
style, not copied).

### Selected skills

`task-orchestration`, `implementation`, `code-audit`,
`review-and-falsification`, `handoff`, `repo-organization`.

### Design decisions

- **D6.1 Rendering model.** Install-time token rewrite. Token list = the
  eleven skill names from the manifest. Rewrite rule: occurrences inside
  backticks with word boundaries, frontmatter `name:` values, and destination
  directory names. Applied to `AGENTS.md` and every `SKILL.md`. Snapshot
  tests pin the rendered output for one slug.
- **D6.2 Prefix policy (needs a recorded decision).** Recommendation:
  `--slug` is **required**, with `--no-prefix` as the explicit escape hatch
  for a deliberately single-repo user. Rationale: the observed operating mode
  is multi-repo; a defaulted-off prefix reproduces the collision hazard
  silently. Slug validation: `^[a-z][a-z0-9-]*$`, ≤ 24 chars.
- **D6.3 Manifest schema v2.** `{"version": 2, "groups": {"core": [ {source,
  destination}, … ]}}`. Installer installs `core` by default; `--profile
  <name>` (repeatable) adds groups (introduced empty here; populated by
  007–009). Preflight computes the union of selected groups before any write.
  Schema validation errors are exit 2.
- **D6.4 Doctor + receipt (needs a recorded decision, D6.4a).**
  Recommendation: on install, write `.agents/kit-install.json` (manifest
  version + SHA-256, slug, selected groups, per-file payload hashes,
  ISO-8601 UTC timestamp). Doctor compares non-template files by hash;
  template files (state, docs READMEs) are user-owned after install, so
  presence-only. A missing receipt reports "unknown installation" and falls
  back to presence checks. The receipt path joins the collision preflight.
- **D6.5 CLI shape.** `argparse` subcommands `install` and `doctor`. The old
  positional form is removed (no external users; breaking change noted in
  README and the task record).

### Implementation plan

1. Decision slice: record D6.2 and D6.4a outcomes in the task file (and
   `docs/decisions/` if the Reviewer judges them consequential).
2. Manifest v2 + loader/validation + migrate `distribution/manifest.json`;
   update every distribution test to the new schema.
3. Renderer (token rewrite) + `--slug`/`--no-prefix` + snapshot tests +
   "installed validator passes" test + "no unprefixed leakage" grep test.
4. `--dry-run` + snapshot-untouched test.
5. Receipt + `doctor` + four scenario tests (clean / tampered file / missing
   file / no receipt).
6. README rewrite of the installation section; expected-layout tree updated
   to show prefixed names and the receipt.

### Validation and evidence plan

Extended `tests/test_distribution.py` (expected growth: +10–14 tests) plus a
disposable-target end-to-end in the handoff: fresh git repo → install with
slug → installed validator run → doctor clean → tamper → doctor findings.
Post-acceptance ledger rows (indicative): C15 slug-rendered installs validate
with zero name leakage; C16 doctor distinguishes the three states without
writes.

### Distribution impact

Manifest format change (v2), same 22 payload files in `core`. The receipt is
generated, not copied — documented in README's expected layout.

### Risks

Token over/under-matching (mitigated by backtick scoping + snapshot tests +
leakage grep); receipt as an unexpected file for target tooling (documented;
lives under `.agents/`); schema churn (v2 is additive-only for future groups).

### Size

M (likely two sessions: decisions+manifest+renderer, then dry-run+doctor).

---

## Plan 007 — Generic validator pack and target CI template (actual task 008; accepted with follow-up)

### Goal

A fresh install is self-enforcing on day one: authority-redirect, doc-link,
and docs-sync checks, a target `verify.sh` entry point with a marked
extension section, and a CI workflow template that runs it verbatim — shipped
as an opt-in `verify` profile group.

### Motivation and evidence

- Installed repos currently get one validator and no way to run "everything"
  or wire CI. All four sibling repos treat that as the core of their
  discipline.
- Specific donor checks with proven value: doc-link resolution
  (IntrinsicEngine `check_doc_links.py`, CI-strict), authority-surface
  agreement (IntrinsicEngine `check_codex_config.py`; realtime-gs's *missing*
  symlink-sync checker is a recorded gap this closes generically), and
  diff-triggered docs-sync rules (IntrinsicEngine, structsplat, realtime-gs).
- Negative evidence shapes the docs-sync design: IntrinsicEngine's rule set is
  near-vacuous (5 of 6 rules satisfiable by any task-file edit), and
  realtime-gs's extension rule states checks "must not produce false
  positives on prose edits". Ship the mechanism nearly empty.

### Mode

Implement (two slices).

### Success criteria

1. Slice 007a: `scripts/check_doc_links.py` and `scripts/check_authority.py`
   exist, are stdlib-only with `--root`/`--strict` and the 0/1/2 exit
   convention, pass on this repository, fail their fixtures, and run inside
   agent-kit's own `verify.sh`.
2. Slice 007b: `check_docs_sync.py` + `docs-sync-rules.toml` (tomllib,
   warning-mode default), a target `verify.sh` template with a marked
   `# TODO: repository-specific gates` section, and
   `.github/workflows/agent-workflow.yml` template that runs
   `./scripts/verify.sh` verbatim — all in a new manifest group `verify`.
3. A distribution test installs `core` + `verify` into a disposable git repo
   and the installed `verify.sh` exits 0 immediately.
4. A regression test pins that the target CI template contains exactly the
   verbatim `verify.sh` invocation (no step re-listing) — the anti-drift
   property itself is tested.

### Constraints

- Checkers must run without git when necessary: `check_docs_sync.py` degrades
  to a no-op with a warning outside a git work tree or when no base is
  resolvable (exit 0 non-strict).
- The target CI template's filename must not collide with common existing
  workflows (`ci.yml` exists in all four repos) — hence
  `agent-workflow.yml`.
- Rules file format is TOML read via stdlib `tomllib` (Python ≥ 3.11). No
  hand-rolled parsers (an IntrinsicEngine weakness on record).

### Non-goals

Shipping opinionated docs-sync rules (targets add their own; the file ships
with commented examples and at most one conservative rule); root-hygiene and
workflow-name checks (revisit only on observed need); PR-contract checks
(GitHub-specific; candidate for a later `ci` extension).

### Selected skills

`task-orchestration`, `implementation`, `code-audit`, `handoff`,
`repo-organization`.

### Design decisions

- **D7.1 `check_authority.py` rules.** (a) If `CLAUDE.md` exists it must be a
  symlink to `AGENTS.md` or contain a redirect marker line; a long CLAUDE.md
  without the marker fails (policy-fork detector, generalizing
  IntrinsicEngine's `check_codex_config.py`). (b) Exactly one physical skills
  root; if both `.agents/skills` and `.claude/skills` exist, one must be a
  symlink to the other, and every skill directory's frontmatter `name:` must
  equal its directory name. (c) `.codex/config.yaml`, if present, must
  reference the contract file. Warning-mode default, strict flag.
- **D7.2 `check_doc_links.py` scope.** All `*.md` under `AGENTS.md`,
  `README.md`, `docs/**`, `.agents/state/**`, `.agents/skills/**`; relative
  and root-relative link resolution; fenced code ignored; schemes and
  anchors skipped.
- **D7.3 docs-sync rule schema.** `[[rule]]` with `trigger = [globs]`,
  `one_of = [globs]`, `reason = "…"`. Changed files from `--files …` or
  `--base <ref>` (merge-base). Every rule must carry a non-empty `reason`
  (the structsplat allowlist-with-reasons pattern).
- **D7.4 Dual-use vs divergence.** `check_doc_links.py`,
  `check_authority.py`, `check_docs_sync.py` are the *same files* used by
  agent-kit and shipped to targets (single source). The two `verify.sh`
  scripts differ (agent-kit's runs its own suite; the target template has the
  TODO section) — a unit test asserts the template contains the required
  stage invocations so the two cannot silently diverge in gate coverage.

### Implementation plan

007a: authority + doc-links checkers, fixtures, wire into agent-kit's
`verify.sh`, add both to manifest group `verify`.
007b: docs-sync checker + rules template, target `verify.sh` template, CI
workflow template, disposable-target install test, README "wiring up CI"
section.

### Validation and evidence plan

Per-checker fixture tests + live-tree pass tests (the realtime-gs pattern);
the disposable-target end-to-end; induced-failure demos in the handoff.
Post-acceptance ledger row (indicative C17): "a fresh `core+verify` install
self-enforces with one command and a verbatim CI template."

### Distribution impact

New manifest group `verify` (~6 files: 3 checkers, rules template, verify
template, workflow template). `core` unchanged.

### Risks

False-positive docs-sync erodes trust (mitigated: near-empty default rules,
warning mode); target CI YAML bit-rot (template is minimal: checkout,
setup-python, run script); link-checker performance on huge doc trees
(bounded scan roots).

### Size

M–L (two slices, one session each).

---

## Plan 008 — Task-tree profile (next as actual task 009)

### Goal

An opt-in, validated, dependency-aware backlog for targets whose work
outgrows one file — with a generated unblocked view — without ever creating a
second active-task or archive authority.

### Motivation and evidence

- agent-kit's single `backlog.md` does not scale to the observed sibling
  reality (structsplat: 116 task files; IntrinsicEngine: 838). The planned
  program itself (six tasks) already strains one file.
- IntrinsicEngine's decisive features are the generated unblocked view
  (`SESSION-BRIEF.md`, CI-checked freshness) and front-matter dependency
  edges. Its recorded weaknesses steer the design: no cycle detection in
  `validate_tasks.py`, and a single unretired task (`REVIEW-003`) silently
  bottlenecking 12+ backlog items — this plan includes both cycle detection
  and a top-blocker report.
- Task 003 failure mode 1 (dual authority) is the governing constraint:
  agent-kit already has an active authority (`current-task.md`) and an
  archive authority (`docs/tasks/`). Only the backlog layer scales.

### Mode

Decide, then Implement. The design decision is consequential enough for a
`docs/decisions/` record.

### Success criteria

1. A decision record chooses the layout (D8.1) with alternatives and a
   reversal condition.
2. With the profile installed: `.agents/state/backlog/` holds one file per
   item (`<slug>.md` with TOML/YAML-lite front-matter: `slug`, `depends_on`,
   optional `theme`); `scripts/check_backlog.py` validates front-matter,
   dependency resolution (to backlog slugs or archived task IDs in
   `docs/tasks/`), acyclicity (DFS), and slug uniqueness;
   `scripts/generate_backlog_brief.py` writes an Unblocked/Blocked view into
   `.agents/state/backlog/README.md` and `--check` fails on staleness; both
   are wired into the installed `verify.sh`.
3. `current-task.md` remains the only active authority: promotion is
   documented as "move the item's content into `current-task.md`, delete the
   backlog file, regenerate the brief" — one commit.
4. The profile replaces `backlog.md`; installer refuses to install the
   profile when `backlog.md` has non-template content; doctor flags
   both-present as a finding.
5. agent-kit itself adopts the profile for the remaining program backlog
   (dogfood), migrating this plan's entries.

### Constraints

- Numbers stay archive-assigned (the existing "next unused number in
  `docs/tasks/`" rule); backlog items are identified by slug only, so
  parallel branches cannot race on numbers (IntrinsicEngine's duplicate-ID
  history is the cautionary evidence).
- The generated brief must be deterministic (no timestamps) so `--check` is a
  pure content comparison — the IntrinsicEngine `generate_session_brief.py`
  property.

### Non-goals

Multi-state task trees (`tasks/active|done` directories), themes/convergence
maps, retirement logs, maturity sections — all remain out until a target
demonstrates the need.

### Selected skills

`task-orchestration`, `repo-organization`, `implementation`,
`review-and-falsification`, `handoff`.

### Design decisions

- **D8.1 Layout (the decision record).** Options: (A) `.agents/state/backlog/`
  directory profile, keep `current-task.md` + `docs/tasks/` as-is —
  **recommended**: smallest delta, zero dual authority, coordination state
  stays under `.agents/state/`; (B) top-level `tasks/` tree
  (IntrinsicEngine/structsplat convention) — rejected for the kit default:
  collides with every sibling's existing tree and duplicates the archive
  authority; (C) status quo — rejected by the program's own backlog size.
- **D8.2 Front-matter format.** Minimal `key: value` + list lines parsed by a
  small strict parser shared with nothing else (or TOML blocks via
  `tomllib`); decide in-task with a bias to whichever needs less code.
- **D8.3 Blocked-report shape.** The brief lists each blocked item with its
  first unmet dependency, plus a "top blocker" line (the dependency blocking
  the most items) — the direct answer to IntrinsicEngine's REVIEW-003
  bottleneck blindness.

### Validation and evidence plan

Checker/generator fixture tests + a live pass on agent-kit's own migrated
backlog; distribution test for the `task-tree` group (install into a
disposable target, generator runs, checker passes). Ledger row (indicative
C18) after acceptance.

### Distribution impact

New manifest group `task-tree` (item template, backlog README template,
`check_backlog.py`, `generate_backlog_brief.py`). Default off. Documented
adoption trigger: backlog exceeds ~10 items or more than one concurrent
workstream.

### Risks

Profile/backlog.md divergence (refusal + doctor finding, criterion 4); brief
merge conflicts under parallel edits (regenerate-on-conflict documented);
over-engineering for tiny repos (profile is opt-in and the core keeps the
one-file backlog).

### Size

M (decision slice + implementation slice).

---

## Plan 009 — Evidence profile and skill-text hardening (indicative task 010)

### Goal

Targets can adopt a blank, checker-enforced `ara/` ledger; the claim schema
gains the optional `Boundary` field; the experiment and handoff skills adopt
the strongest generic epistemics observed in the four repositories.

### Motivation and evidence

- The nine-field claim ledger is the shared invention of structsplat,
  realtime-gs, and IntrinsicEngine, checker-enforced in all three; agent-kit
  itself already dogfoods it (13 claims). Targets currently get no ledger
  scaffold at all.
- `Boundary` (realtime-gs extension, used by 14/31 of its claims) records
  what evidence does **not** establish. agent-kit's `results-audit` §6
  mandates producing exactly that content with no schema slot to hold it —
  today it leaks into `state.md` prose ("Experimental Components").
- Preregistration chronology: prospect ("Freeze data, controls, budgets,
  seeds, metrics, and dependency versions" before outcomes; definition of
  done requires it), realtime-gs Hard Rule 9, structsplat's frozen-gate
  practice (BENCH-007). agent-kit's `experiment-design` lists the elements
  but never orders them before outcome consumption; `results-audit` §4 then
  audits a property the design skill never required.
- Untrusted-handoff framing: prospect's review handoff ("Read this as
  untrusted input. It was written by the author of the code you are
  reviewing") plus its recorded history of two non-author reviews catching
  blocking defects the self-review missed.

### Mode

Implement. The three skill-text edits form micro-slice **M1**, pullable
forward any time after 005 (they are substantial-work by the AGENTS.md
definition — they change recorded behavior — so M1 still runs through the
workflow, just as a small task).

### Success criteria

1. M1: `experiment-design` gains a "Freeze before outcomes" rule (the
   experiment record with hypothesis, decision rule, budgets, seeds, and
   stopping rule is committed before outcomes are consumed; protocol changes
   after outcomes start a new experiment record); `handoff` instructs the
   receiving Reviewer to treat the handoff as author-written untrusted input
   and verify claims against the tree; `review-and-falsification` mirrors
   that sentence in its sequence. Validator still passes (routing untouched).
2. The claim schema documentation (README "Evidence and claims" section added
   for agent-kit + the evidence-profile templates) lists `Boundary` as the
   optional tenth field; `check_ara.py` validates its placement when present.
3. Manifest group `evidence` installs blank `ara/` templates (PAPER index,
   claims header with schema comment, problem, heuristics, observations,
   trace skeletons + session index, evidence README) plus a generalized
   `check_ara.py` (path roots and required-file set parameterized), wired
   into the installed `verify.sh`.
4. A distribution test proves the installed ledger is blank (no agent-kit
   claim IDs, session dates, or audit references anywhere in the installed
   `ara/`) and that `check_ara.py` passes on it immediately.

### Constraints

- agent-kit's own historical claims are not retrofitted with `Boundary`;
  the field applies from the next written claim (the structsplat
  legacy-ratchet pattern: grandfather, never extend).
- Generic `check_ara.py` must not require git or YAML libraries (the
  observations file is parsed line-wise for IDs only, as the sibling
  checkers do).

### Non-goals

Observation/trace tooling, session-record automation, evidence-bundle
conventions — ledger discipline only.

### Selected skills

`task-orchestration`, `implementation`, `results-audit` (as the domain
authority for the schema), `handoff`, `repo-organization`.

### Implementation plan

1. M1 (three skill edits + README schema section) — own micro task if pulled
   forward, else first slice here.
2. Generalize `check_ara.py` (parameterize roots/required set); keep
   agent-kit's invocation behavior identical.
3. Author blank templates under `distribution/templates/ara/`; add manifest
   group `evidence`; extend distribution tests (blank-ness grep, immediate
   checker pass, collision preflight for `ara/` paths — all four sibling
   repos have an `ara/`, so the preflight will correctly refuse there; that
   is desired behavior and gets a test).
4. README: document the profile and the adoption guidance ("a repo with an
   existing ledger keeps it; this profile is for repos without one").

### Validation and evidence plan

Fixture tests for `Boundary` handling; disposable-target install + checker
pass; collision-refusal test against a fake existing `ara/`. Ledger rows
(indicative C19/C20) after acceptance.

### Distribution impact

New manifest group `evidence` (~10 files). `core` unchanged except the three
skill-text files (already in `core`).

### Risks

Schema drift between agent-kit's ledger and target templates (single
`check_ara.py` source prevents divergence); templates accidentally carrying
source history (blank-ness grep test).

### Size

M. M1 alone: XS.

---

## Plan 010 — Growth loop and process-audit skill (indicative task 011)

### Goal

Ship the mechanism that makes installed workflows improve instead of rot: an
"executable memory" section in the payload `AGENTS.md` and an optional,
generic `process-audit` skill bundling the domain-neutral audit procedures
observed across the four repositories.

### Motivation and evidence

- The growth loop is the actual engine of IntrinsicEngine's maturity:
  incident → skill/validator citing the incident (its triage skills name
  their motivating regressions; structsplat's benchmark skill embeds the
  measured numbers justifying its rules; realtime-gs's results-audit lists
  the five audit failures it distills); warning→strict ratchet owned by a
  task (`AGENTS.md` §10: "an untracked warning-mode check is a policy
  violation"); periodic rent audit (keep 53 / warn 2 / retire 2 of 57).
- The failure-mode catalog of IntrinsicEngine's weekly audit is almost
  entirely domain-neutral and maps directly onto agent-kit's universal
  constraints: silent scope creep, decorative comments, premature
  abstraction, documented-but-not-tested claims, defensive ceremony at
  internal boundaries, untracked compatibility shims, ceremony without
  shipped value, half-finished implementations, aspirational docs without a
  "(planned)" marker.

### Mode

Implement.

### Success criteria

1. Payload `AGENTS.md` gains a compact "Executable memory" section (~12–15
   lines): (a) a failure that recurs becomes a repository skill or validator
   that cites the incident; (b) a new check enters in warning mode owned by a
   named backlog item and is ratcheted to strict deliberately; (c) machinery
   is periodically rent-audited via `process-audit` and retired when it stops
   producing findings; (d) a validator that never ran is not evidence its
   subject is healthy.
2. New optional skill `process-audit` routed from `AGENTS.md`, containing
   three procedures with report templates targeting `docs/audits/`:
   agent-output audit (the nine generalized failure modes), state-drift audit
   (recorded state vs. tree reality), and validator rent audit (per check:
   protective finding / load-bearing producer / no unique evidence → keep /
   warn / retire). The skill's own frontmatter carries a provenance block
   citing its source incidents — serving as the exemplar of the convention it
   establishes.
3. Validator passes (routing agreement picks up the new skill); distribution
   tests updated for the +1 core file; agent-kit runs one rent audit on
   itself as the acceptance demonstration and records the report under
   `docs/audits/`.

### Constraints

- **D10.1** The skill is optional in routing language, like `results-audit` —
  substantial tasks are not gated on it.
- **D10.2 No cadence checker.** IntrinsicEngine's own cadences are lapsed
  ~62/~53 days *with* a checker (report-only, nightly) — the checker did not
  prevent the lapse, and agent-kit has no nightly surface to host one.
  Instead, `repo-organization`'s completion update gains one line: "consider
  `process-audit` roughly every fifth completed task or after any incident."
  Revisit a checker only if audits demonstrably lapse here too.

### Non-goals

Mandatory audit cadences; audit tooling/automation; applying the audit to
target repositories (they self-serve via the installed skill).

### Selected skills

`task-orchestration`, `implementation`, `review-and-falsification`,
`handoff`, `repo-organization`.

### Validation and evidence plan

Routing/validator pass; the self-run rent-audit report as the worked example;
distribution test count update. Ledger row (indicative C21) after acceptance.

### Distribution impact

+1 skill directory in `core`; `AGENTS.md` text change (already `core`).

### Size

S–M.

---

## Decision draft D1 — Single-product convergence (for `docs/decisions/`, status: Proposed)

**Context.** Two workflow kits exist in this ecosystem: agent-kit (standalone;
two-agent coordination kernel, evidence skills, collision-safe manifest
distribution, 36-test regression suite) and IntrinsicEngine's embedded
`tools/agentkit` (single-agent repo-discipline generator: config-driven
validators, task tree, CI templates, doctor/resync, slug prefixing; no
coordination kernel, no verdict enforcement, no ledger checker). Maintaining
both means duplicated mechanics and two competing sources of truth — the
exact hazard IntrinsicEngine's own skills README warns about.

**Decision (proposed).** agent-kit is the single distributable workflow
product. `tools/agentkit` is treated as donor material: its mechanics
(prefixing, dry-run, doctor, config-driven checks, CI templates) are
reimplemented in agent-kit under plans 006–007 with agent-kit's stricter
collision semantics and test discipline. After 007 lands, propose to
IntrinsicEngine — as that repository's own decision, through its own task
system — whether to retire its embedded generator or keep it as an internal
tool; agent-kit assumes no outcome.

**Alternatives.** (a) Keep both indefinitely — rejected: guaranteed drift,
split effort. (b) Rebase on `tools/agentkit` and add the kernel to it —
rejected: it lives inside another repository, lacks the validated
coordination/verdict machinery (agent-kit's genuine differentiator), and its
`--force` overwrite mode contradicts agent-kit's distribution guarantees.

**Consequences.** Plans 006–007 carry the reimplementation cost; agent-kit's
scope statement in `README.md` widens from "two-agent skills" to "installable
agentic workflow (two-agent kernel + verification + optional profiles)".

**Risks.** IntrinsicEngine declines retirement and the kits coexist — the
donor relationship still holds and nothing in agent-kit breaks.

**Reversal condition.** If pilots show targets need the generator-style
`agentkit.toml` re-render model (regenerate-on-config-change) rather than
install-once-then-own, revisit (b) with that evidence.

**Requires:** human sign-off (product-priority decision per `AGENTS.md`
escalation rules). Until then, plans 006–007 stand on their own evidence.

---

## Open questions for the human

1. **D6.2.** Is `--slug` required-with-escape-hatch the right prefix policy,
   or should unprefixed remain the default?
2. **D1.** Approve the single-product convergence direction now, or defer
   until after 007?

Resolved at task 006 initialization: the owner authorized execution of the
proposed sequence and Python 3.11–3.13 support. The repository rotation record
assigns task 006 Driver `codex-b` and Reviewer `codex-a`.

## Execution protocol

Each plan lifts into `.agents/state/current-task.md` at initialization: the
plan's Goal/Success criteria/Constraints/Non-goals/Selected skills map
one-to-one onto the template's sections, and the implementation plan becomes
the Minimal Plan. Work happens on a task branch; the Reviewer reproduces from
the branch; completion follows `repo-organization` (archive, state update,
role record). This document is reference material, not authority: where an
executed task's record contradicts it, the task record wins and this file
receives a dated amendment noting the divergence. Backlog registration of
plans 006–010 happens as part of initializing 005 (or, after 008, by
migrating into the task-tree profile).
