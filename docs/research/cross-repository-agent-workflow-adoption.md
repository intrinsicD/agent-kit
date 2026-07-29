# Research Note: Cross-Repository Agent Workflow Adoption

Date: 2026-07-29

## Research Question

Should the two-agent workflow in `agent-kit` be added to, or replace the
agentic workflows in `prospect`, `structsplat`, `realtime-gs`, and
`IntrinsicEngine`? Conversely, which workflow mechanisms in those repositories
should be integrated into `agent-kit` or replace part of it?

## Decision Summary

Do not replace any target repository's workflow wholesale, and do not install
the full agent-kit workflow into any of them as default policy. Task 004
replaced the unsafe tracked-tree export with a fixed, collision-refusing
22-file payload, but safe distribution is an enabler for evaluation rather
than evidence that adoption will help. The evidence supports two bounded
pilots, not an adoption decision.

The useful part of `agent-kit` is its independently validated coordination
kernel: explicit Driver and Reviewer labels, a turn marker, repository-persisted
handoffs, a terminal verdict, role rotation, and safe merge versus non-merge
closeout. All four targets have meaningful review norms, and recent history in
each records reviewer or independent-audit practice. None of their general task
workflows mechanically enforces distinct proposer/reviewer labels and a
terminal verdict the way agent-kit's validator does. Agent-kit labels remain a
cooperative protocol, not authenticated identity.

Their repository-specific experiment, task, evidence, validation, and CI
systems are stronger than the corresponding generic parts of `agent-kit` and
must remain authoritative.

| Repository | Evidence-backed disposition | Minimal invariant to test |
| --- | --- | --- |
| `prospect` | Eligible for a bounded pilot after explicit prioritization; no adoption decision yet | Bind one task Driver label, final Reviewer label, turn, and verdict in repository state without replacing the existing multi-pass non-author evidence reviews. |
| `realtime-gs` | Preferred first bounded pilot after explicit prioritization; no adoption decision yet | Add one durable current-task/handoff record with a distinct final Reviewer label; preserve all experiment and result-bundle gates. |
| `structsplat` | Do not install a parallel workflow; consider a schema/checker experiment | Test distinct proposer/reviewer labels and a terminal verdict inside the existing task authority. |
| `IntrinsicEngine` | Do not install or replace; consider a high-risk-only enforcement experiment | For research claims, architecture decisions, and critical implementations, test persisted proposer/reviewer labels and a verdict in the existing task/PR record. |

Task 004 completed the two repository-level imports justified by this
assessment: the clean fixed distribution boundary and the optional generic
results-audit procedure distilled from Prospect, StructSplat, and realtime-gs.
No further target mechanism currently justifies replacing agent-kit's core.
If a pilot is prioritized, a read-only installer plan or `--dry-run` mode is a
small useful safety improvement borrowed from IntrinsicEngine; it does not
justify importing IntrinsicEngine's generator, overwrite mode, task graph, or
CI platform.

## Evidence Classification

- **Repository observation**: directly read from the named file or produced by
  a command against the recorded checkout.
- **Established result**: an executable check reproduced in this assessment.
- **Agent inference**: a recommendation derived from the observations; it is
  not a property enforced by the target repository.
- **Unverified hypothesis**: a predicted operational effect that needs a pilot.

## Key Sources

### `agent-kit`

- `README.md`
- `AGENTS.md`
- `.agents/state/current-task.md`
- `.agents/skills/handoff/SKILL.md`
- `.agents/skills/repo-organization/SKILL.md`
- `.agents/skills/review-and-falsification/SKILL.md`
- `scripts/validate_agent_workflow.py`
- `tests/test_agent_workflow.py`

### `prospect`

- `CLAUDE.md`
- `.agents/skills/prospect-research-ideation/SKILL.md`
- `.agents/skills/prospect-results-audit/SKILL.md`
- `docs/wm002-q1-review-handoff.md`
- `.github/workflows/ci.yml`

### `structsplat`

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/skills/structsplat-task-workflow/SKILL.md`
- `.claude/skills/structsplat-review/SKILL.md`
- `.claude/skills/structsplat-results-audit/SKILL.md`
- `tasks/INDEX.md`
- `scripts/check_task_policy.py`
- `tests/test_agent_workflow_checkers.py`
- `.github/workflows/ci.yml`

### `realtime-gs`

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/skills/rtgs-experiment/SKILL.md`
- `.claude/skills/rtgs-review/SKILL.md`
- `.claude/skills/realtime-gs-results-audit/SKILL.md`
- `scripts/check_results_bundle.py`
- `tests/test_agent_workflow_checkers.py`
- `.github/workflows/ci.yml`

### `IntrinsicEngine`

- `AGENTS.md`
- `docs/agent/task-format.md`
- `docs/agent/task-maturity.md`
- `docs/agent/roles.md`
- `docs/agent/review-checklist.md`
- `docs/agent/agent-output-review-checklist.md`
- `tasks/SESSION-BRIEF.md`
- `tools/agents/validate_tasks.py`
- `tools/agents/generate_session_brief.py`
- `tools/agentkit/`
- `.github/workflows/ci-docs.yml`

## Inspected Snapshots

| Repository | Inspected commit | Working-tree note |
| --- | --- | --- |
| `agent-kit` | `d8d649512f454c219dba55dd12f4d0398cb742e9` plus task-003 state | Clean at task start. |
| `prospect` | `537966bf88c0ca9ecc89af10b6d7dbebef3872bd` | `main` was three commits ahead of `origin/main`; untracked `discuss/` was preserved and not inspected as authority. |
| `structsplat` | `ebf860bcf29d15e33d1be32315c6856baa30abb5` | Clean. |
| `realtime-gs` | `dd84c28deb3378d57992cd10b20f08bb594f102a` | Clean. |
| `IntrinsicEngine` | `5f7843c99be6f978b2939b463f48abfb39348c66` | Clean. |

The assessment covers checked-in local workflow behavior. It does not inspect
private issue trackers, branch-protection settings, remote-only branches, or
human practices not represented in the repositories.

## Revalidation After Task 004

### Repository observations

On 2026-07-29, Task 005 compared every target's current `HEAD` with the Task 003
snapshot. All four commit distances are zero:

| Repository | Current commit | Commits since Task 003 |
| --- | --- | ---: |
| `prospect` | `537966bf88c0ca9ecc89af10b6d7dbebef3872bd` | 0 |
| `structsplat` | `ebf860bcf29d15e33d1be32315c6856baa30abb5` | 0 |
| `realtime-gs` | `dd84c28deb3378d57992cd10b20f08bb594f102a` | 0 |
| `IntrinsicEngine` | `5f7843c99be6f978b2939b463f48abfb39348c66` | 0 |

Prospect still has local uncommitted research work and an untracked `discuss/`
directory. IntrinsicEngine has local uncommitted RUNTIME-201 work. Task 005 did
not inspect those changes as workflow authority and did not write to any target
checkout. StructSplat and realtime-gs remain clean.

The target checks were rerun from disposable `git archive HEAD` snapshots so
the live working trees stayed untouched:

- Prospect's epistemic diagnostics exited zero while retaining
  `claim_supported: false` and blocked/reference-only dispositions.
- StructSplat's docs, ARA, task, and script checks passed; its focused workflow
  tests passed 8/8.
- realtime-gs's docs, ARA, and script checks passed; its focused workflow tests
  passed 12/12.
- IntrinsicEngine validated 175 task files and 811 task IDs, reported its
  session brief and skill mirrors current, passed its ARA check, and passed the
  generator self-test.

### Established results

At agent-kit commit `e16513d`, plus Task 005 state, all 36 regression tests and
the live workflow validator pass. Task 004's fixed manifest contains 22
payload files, emits blank state, excludes source history, and refuses all
collisions before writes.

Against the current target files, the new manifest preflight reports:

| Repository | Fixed-payload collisions | Collision |
| --- | ---: | --- |
| `prospect` | 0 | None |
| `structsplat` | 1 | `AGENTS.md` |
| `realtime-gs` | 1 | `AGENTS.md` |
| `IntrinsicEngine` | 1 | `AGENTS.md` |

These are payload-path results, not fit or adoption results. In particular,
Prospect's zero-collision result means the current CLI would begin writing
immediately; it does not prove that adding a second coordination lifecycle is
worth its cost.

### Agent inference

No target-side evidence has changed the Task 003 dispositions. Task 004 makes
a bounded pilot safe to package, while the benefit and process cost remain
unmeasured. A target change still requires a separately prioritized,
falsifiable pilot.

## Evaluation Criteria

1. **Authority**: one clear source of agent policy across harnesses.
2. **Coordination**: durable ownership, handoff, turn, and escalation state.
3. **Independent review**: the author cannot be the sole final approver of a
   substantial claim or critical change.
4. **Task lifecycle**: explicit scope, dependencies, completion, and history.
5. **Executable memory**: validators and regression tests enforce important
   workflow invariants.
6. **Evidence discipline**: experiments and claims stay bound to raw evidence,
   controls, source, and limitations.
7. **Migration compatibility**: adoption does not overwrite or duplicate an
   existing authority, task system, ARA, or CI workflow.
8. **Proportionality**: process cost matches repository size and risk.

## Established Results

### The former tracked-tree installer was not a distributable boundary

**Repository observation at Task 003.** `agent-kit/README.md` installed every
tracked path with:

```text
git -C agent-kit archive --format=tar HEAD | tar -x -C target-repository
```

The assessment fixed the source to
`d8d649512f454c219dba55dd12f4d0398cb742e9`. From
`/home/alex/Documents`, the exact filesystem collision probe was:

```bash
kit_root=/home/alex/Documents/agent-kit
target_root=/home/alex/Documents/<target>
source_commit=d8d649512f454c219dba55dd12f4d0398cb742e9

git -C "$kit_root" ls-tree -r --name-only "$source_commit" |
  while IFS= read -r tracked_path; do
    if [ -e "$target_root/$tracked_path" ] ||
       [ -L "$target_root/$tracked_path" ]; then
      printf '%s\n' "$tracked_path"
    fi
  done
```

Run it once with `<target>` equal to `prospect`, `structsplat`, `realtime-gs`,
and `IntrinsicEngine`; pipe to `wc -l` for the counts below.

The separate tracked-set probe for payload paths that would be newly added was:

```bash
comm -23 \
  <(git -C "$kit_root" ls-tree -r --name-only "$source_commit" | sort) \
  <(git -C "$target_root" ls-tree -r --name-only HEAD | sort) |
  rg '^(\.agents/state/|docs/(audits|tasks)/|ara/|tests/)'
```

Finally, the actual archive payload was enumerated without extraction:

```bash
git -C "$kit_root" archive --format=tar "$source_commit" | tar -tf -
```

At the inspected commit, the tracked tree includes:

- `.agents/state/state.md` and `.agents/state/current-task.md` containing
  `agent-kit`'s own operational state;
- `docs/tasks/001-agent-workflow-audit.md` and
  `docs/tasks/002-fix-workflow-audit-findings.md`;
- the audit report;
- `agent-kit`'s ARA claims, observations, exploration nodes, and dated session
  records; and
- the workflow regression suite.

**Established result.** The documented collision preflight reports:

| Target | Exact tracked-path collisions |
| --- | ---: |
| `prospect` | 11 |
| `structsplat` | 12 |
| `realtime-gs` | 11 |
| `IntrinsicEngine` | 12 |

Every target collides with its existing ARA; three also collide with
`AGENTS.md`. Even if those collisions were manually resolved, the non-colliding
agent-kit state, task-001/task-002 archives, and dated ARA session would still
be copied into all four targets.

**Agent inference at Task 003.** Collision safety would prevent accidental
overwrite, but it would not make the tracked repository a clean installation
payload. Deployment therefore remained blocked until packaging was separated
from development history.

**Established resolution.** Task 004 retired this command. The current
installer uses a fixed 22-file manifest, blank state templates, complete
preflight collision refusal, exclusive file creation, and rollback of only
installer-created paths. Its distribution tests and independent review close
the historical P0 blocker without establishing target fit.

### The coordination kernel is the genuine differentiator

**Repository observation.** `agent-kit` uniquely combines:

- mandatory Driver/Reviewer assignment and role rotation;
- a repository-persisted `Turn` marker;
- append-only handoff and review records;
- an independent verdict with explicit self-review downgrade;
- bounded revision rounds;
- accepted-branch merge closeout and metadata-only non-merge closeout; and
- validation of roles, turns, statuses, verdicts, task IDs, archives, duplicate
  fields, and fenced-code decoys.

**Established result.** The workflow suite passes 31 tests and the live
validator accepts the two operational archives.

None of the four targets enforces this complete combination.

Review evidence must be separated into three levels:

1. **Norm** — instructions tell an agent to act as a reviewer/referee.
2. **Recorded practice** — repository history records a reviewer label,
   non-author handoff, fresh-workspace audit, or independent audit artifact.
3. **Mechanical enforcement** — a validator rejects terminal approval when
   proposer and reviewer labels are not distinct or the verdict/turn is
   invalid.

| Repository | Review norm | Recorded distinct-review practice | Persisted evidence | Distinct identity mechanically enforced |
| --- | --- | --- | --- | --- |
| `agent-kit` | Mandatory Reviewer for substantial tasks | Tasks 001-003 record separate Driver/Reviewer passes | Current-task handoff log and archived task | Yes for distinct nonempty labels and verdict state; no cryptographic authentication |
| `prospect` | Non-author/referee review required for protected evidence | Reviews at `52744be`, `03cd3fc`, and `bde6266`; handoff `e41b22e` | Markdown/ARA review artifacts and free-text reviewer field | No; the schema accepts any nonempty reviewer string |
| `realtime-gs` | Results-audit skill requires a referee stance | Fresh-workspace scientist audit at `ca11378` followed `095313d` before C25-C27 promotion | Machine-readable audit, ARA, and Git authorship | No general validator binds reviewer to a distinct author |
| `structsplat` | Results-bearing tasks require an audit/referee pass | FIT-042 requires an independent artifact audit; FIT-043 records an independent cold audit | Task and evidence bundle | No proposer/reviewer identity or terminal-verdict check in task policy |
| `IntrinsicEngine` | Review Agent, per-change review, clean-workshop, and periodic audit guidance | RUNTIME-190 records `Reviewer: Codex`; retirement history records multiple independent reviews | Task/PR/review and retirement records | No general identity-separation validator; root sequence ends in self-review |

The gap is therefore not “no independent review.” It is the narrower absence
of general, mechanically checked identity separation and terminal review state.
Whether closing that gap pays for its coordination cost is an unverified pilot
question in Prospect and realtime-gs.

## Repository Assessments

### `prospect`

#### Repository observations

- `CLAUDE.md` is a strong semantic and evidence contract, but there is no root
  `AGENTS.md` for harness-neutral authority.
- Two project-prefixed skills under `.agents/skills/` cover transformational
  research ideation and adversarial result auditing.
- The experiment contract freezes claims, controls, budgets, seeds, metrics,
  and abandonment rules before formal outcomes.
- `prospect-results-audit` requires raw recomputation, causal custody, matched
  budgets, controls, fresh-process restoration, and a disposition for every
  claim.
- `docs/wm002-q1-review-handoff.md` is an unusually strong non-author handoff:
  it binds the reviewed commit and digests, identifies prior reviewer misses,
  names traps and untested surfaces, limits reviewer authority, and explicitly
  prohibits consuming the protected experiment.
- Recent history demonstrates that this is more than aspirational prose:
  `e41b22e` handed the exact source to another non-author reviewer, and the
  third review at `bde6266` independently recomputed identities and found nine
  non-blocking issues. Two earlier non-author reviews found blocking defects
  the self-review missed.
- The Q1 schema persists a free-text `reviewer`, and the entry gate checks
  source/protocol bindings, but it cannot establish that the reviewer differs
  from the author.
- There is no generic durable task record, role assignment, turn marker,
  terminal verdict schema, workflow state validator, or branch closeout
  protocol.
- `make epistemic-diagnostics` completed successfully while reporting
  `claim_supported: false` and scoped blocking reasons for every maturity gate;
  the command did not turn green diagnostic predicates into unsupported
  capability claims.

#### Recommendation

**Run a selective coordination pilot only after explicit prioritization; do
not replace the current workflow and do not treat the pilot as an adoption
decision.**

The distribution blocker is fixed. A separately authorized pilot should:

1. Add one clean project task record that binds a Driver label, final Reviewer
   label, turn, verdict, and repository-persisted handoff.
2. Add the narrow validator needed to reject invalid labels, turn, and verdict
   state for that pilot.
3. Preserve both `prospect-*` skills, all ARA content, experiment rules,
   non-author scientific audits, and current CI.
4. Permit additional non-author scientific reviews beyond the single task
   Reviewer; one final task verdict must not replace Prospect's multi-pass
   evidence audits.
5. Add or merge a harness-neutral authority adapter only if the pilot agents
   require it; this is a target integration need, not part of the universal
   packaging blocker.

The hypothesis is that explicit task closure catches state/approval drift not
covered by the scientific audit. The pilot succeeds only if it avoids duplicate
authority and either catches a material coordination defect or measurably
improves handoff reproducibility at acceptable cost.

### `realtime-gs`

#### Repository observations

- `AGENTS.md` is a thin redirect to the detailed `CLAUDE.md` contract.
- Six prefixed skills cover verification, benchmarks, experiments, review,
  docs sync, and results audit, mirrored into `.agents/skills/` by symlink.
- The repository has no `tasks/` lifecycle or equivalent durable active-task
  authority.
- `rtgs-review` is explicitly a self-review; the results audit adopts an
  independent-referee stance but does not bind reviewer identity or prevent
  author approval.
- Recent history records real separate-review practice: after implementation
  `095313d`, a different Git author performed a fresh-workspace scientist pass
  at `ca11378`, producing a machine-readable audit before claims C25-C27 were
  promoted. No general task/state checker enforces that separation.
- Results-bearing work has strong domain gates: real calibrated data, held-out
  discipline, append-only experiment records, source/config bindings, a
  portable `index.html`, preview artifacts, viewer receipts, and
  `check_results_bundle.py`.
- Docs, ARA, and script-layout checks pass. The 12 workflow-checker regression
  tests pass with `PYTHONPATH=src`; the repository-local `.venv` was absent, so
  the broader repository test gate was not run.

#### Recommendation

**Run the first clean coordination pilot here; preserve every domain workflow
and defer adoption until the pilot reports evidence.**

This is a low-conflict pilot candidate because the repository has no competing
task tree. That is an inference about fit, not evidence that its adoption
priority exceeds Prospect's:

1. Add one clean current-task record with Driver/Reviewer labels, turn,
   persisted handoff, verdict, and closeout state.
2. Add only the state validation required by the pilot.
3. Route existing `rtgs-*` and `realtime-gs-*` skills alongside any pilot
   coordination skill; do not rename or replace them.
4. Merge or redirect authority files only as required by the participating
   harnesses.
5. Leave the ARA, experiment log, result-bundle checker, real-data/viewer gate,
   and benchmark protocol untouched.

Complete one ordinary code task and one results-bearing task. Measure process
time, duplicate-state incidents, handoff reconstruction, and material findings;
then choose adopt, revise, or remove. CI integration becomes a condition of
wider adoption, not a prerequisite for a disposable/local pilot.

### `structsplat`

#### Repository observations

- `AGENTS.md` redirects to a detailed canonical `CLAUDE.md`.
- Eight project-prefixed skills are canonical under `.claude/skills/` and
  exposed under `.agents/skills/` through tracked symlinks.
- `tasks/INDEX.md` is the declared current outcome authority. At the inspected
  commit, the checker reported 73 active and 43 retired tasks.
- Task IDs, index membership, dependencies, status vocabulary, ARA structure,
  docs reachability, script placement, and skill mirroring are checked in CI.
- A recent task record demonstrates preregistered one-shot rules, source
  hashes, negative-result preservation, independent cold audit, exact failure
  accounting, and refusal to retune after a near pass.
- FIT-042 explicitly requires an independent artifact audit, and completed
  FIT-043 records an independent cold audit. These are persisted review
  practices, not mechanically checked author/reviewer identity.
- `structsplat-review` is primarily a pre-commit/self-review checklist.
  Results-bearing work has a referee skill, but ordinary substantial task
  acceptance does not require a distinct reviewer identity or persisted
  verdict.
- Structural checks and all seven workflow-checker tests pass.

#### Recommendation

**Do not install the full agent-kit state/task layout. If tighter identity
enforcement is desired, test only that invariant inside the existing task
system.**

Adding `.agents/state/current-task.md`, `.agents/state/backlog.md`, and
`docs/tasks/` would create a second status, backlog, and archive authority next
to `tasks/INDEX.md` and `tasks/done/`. Instead:

1. Select one substantial task whose existing audit already expects a separate
   reviewer.
2. Add Driver/Reviewer labels and a terminal verdict to that task or linked
   review artifact without adding a parallel current-task/backlog/archive.
3. Extend `check_task_policy.py` or a focused companion checker only for the
   tested invariant.
4. Preserve the current task IDs, INDEX outcome authority, ADR discipline,
   ARA checker, domain skills, verification script, and CI.

Adopt the check more broadly only if it catches a defect not already caught by
the artifact audit or improves reproducibility without creating status drift.

### `IntrinsicEngine`

#### Repository observations

- `AGENTS.md` is a comprehensive, harness-neutral authority; `CLAUDE.md`,
  Copilot instructions, and Codex configuration are deliberately subordinate.
- Twenty-one project skills are routed from a core skill. Canonical procedure
  docs are mirrored into skill references and checked for drift across three
  harness surfaces.
- The task graph uses YAML front matter, stable subsystem IDs, dependency
  edges, backlog/active/done/archive states, generated unblocked views, strict
  state-link validation, frozen archive history, micro-task templates, and a
  maturity taxonomy.
- The inspected repository validates 175 current task files, indexes 811 IDs,
  and has an up-to-date generated session brief. Task-policy, state-link,
  skill-mirror, and ARA checks all pass.
- CI separates fast feedback, structural policy, CPU, sanitizers, Vulkan,
  source coverage, release/SLO, and nightly evidence.
- The repository contains its own zero-dependency `tools/agentkit` generator
  with config-driven templates, `--dry-run`, idempotent skip behavior,
  `doctor`, `resync`, vendored checks, CI templates, prefixed skills, and a
  temporary-directory self-test. Its self-test passes.
- Per-change review is a self-review/PR checklist. A rotating human-led audit
  is intentionally additive and does not gate every PR. Agent roles are
  responsibilities, not mutually independent proposer/approver identities.
- RUNTIME-190 records `Reviewer: Codex`, and retirement history contains
  repeated independent-review records. The practice exists; the generic task
  validator does not require distinct proposer/reviewer identities.
- The shipped handoff skill writes conversational state to the OS temporary
  directory, which is useful for context compaction but is not durable
  repository evidence.

#### Recommendation

**Do not replace or side-load the full agent-kit workflow.**

IntrinsicEngine already exceeds agent-kit in authority management, task
planning, maturity, validation, CI, and portable bootstrapping. A second
`.agents/state` and `docs/tasks` lifecycle would be a regression.

If a concrete high-risk failure justifies tighter enforcement, pilot only
these two-agent properties:

1. For one substantial research claim, architecture decision, or critical
   implementation, record distinct proposer and reviewer labels plus a
   terminal verdict in the existing task/PR record.
2. Persist review-relevant handoff claims and evidence in the repository.
   Retain the temporary handoff skill for conversation compaction, but do not
   use it as the only transport for approval state.

Do not impose per-task two-agent turns on routine slices; that would conflict
with the repository's deliberately bounded weekly audit and micro-task model.
No priority is assigned until a concrete missed defect or coordination failure
defines a falsifiable need.

## Competing Methods

### Raw tracked-tree installation

Rejected. It collides with all four repositories and exports operational
history as if it were template content.

### Wholesale workflow replacement

Rejected. It would discard stronger domain rules, task graphs, evidence
ledgers, checkers, and CI. It would be most damaging in StructSplat and
IntrinsicEngine.

### Side-by-side full workflows

Rejected. Two task/status/archive authorities create ambiguous ownership and
inevitable drift.

### Selective coordination experiments

Selected as the only reversible next evaluation method, not as an adoption
decision. Preserve each target's authority and domain workflow. Prospect and
realtime-gs are candidates for separate bounded pilots of the minimal
invariants named above now that Task 004 closed the distribution blocker.
StructSplat and IntrinsicEngine should run an in-place schema/checker
experiment only when a concrete coordination failure justifies one.

## Relevant Implementations to Bring Back into `agent-kit`

### P0 — Universal distribution blocker (completed in Task 004)

Task 004 implemented and independently accepted the behavior specified below
using a fixed manifest rather than a general generator.

#### Create an explicit clean payload boundary

**Evidence source:** agent-kit's reproduced collision and history-contamination
failure.

Replace the current installation section and tracked-tree export with a
bounded payload that:

- contains an explicit allowlist of reusable templates and implementation
  files;
- emits blank operational state rather than agent-kit's current state;
- excludes agent-kit's ARA, audits, completed tasks, dated sessions, and
  repository regression fixtures from the target's history; and
- detects every destination collision before writing anything, then refuses
  the operation without partial output.

This must replace, not merely supplement, `git archive HEAD | tar`.
An explicit export manifest and an IntrinsicEngine-style generator are
candidate implementations. The evidence does not yet justify precommitting to
target naming, harness selection, skill renaming, overwrite support, or a
general generator platform.

#### Add a disposable distribution regression

The test must exercise the artifact users would actually install:

- In a fresh temporary repository, install the payload and prove operational
  state is blank and no source-repository task, audit, ARA, session, or fixture
  history is present.
- In a temporary repository containing each protected destination path, prove
  the installer reports all collisions, exits nonzero, and writes nothing.
- Enumerate the produced archive or manifest output and compare it to the
  declared allowlist.

P0 ended when Task 004's clean boundary and regression were independently
reviewed. It did not include target-specific authority, naming, or CI work.

### P1 — High-value, bounded additions (completed in Task 004)

#### Add a generic research-results audit skill

**Sources:** Prospect, StructSplat, realtime-gs.

`experiment-design` specifies a good experiment and
`review-and-falsification` challenges conclusions, but neither currently
requires a results claim table, raw recomputation, exact source/config binding,
control/accounting audit, evidence-scope classification, and explicit
confirm/narrow/refute/retire disposition.

Task 004 added this as an optional research profile, not a universal
software-task gate. Repository-specific rules such as complete-stream bit
accounting, calibrated viewer handoffs, or checkpoint custody remain local
extensions.

### Target-conditioned pilot requirements

These are integration decisions, not universal distribution blockers:

- Add a thin authority redirect or adapter only when the participating agent
  harness cannot discover the target's current canonical instructions.
- Prefix or rename an installed coordination skill only if a preflight finds a
  real name collision or the target deliberately exposes several repositories
  in one skill-discovery surface.
- Before an authorized pilot targets a zero-collision repository, add a
  read-only plan or `--dry-run` path so operators can inspect the exact payload
  without beginning installation. Borrow only this safety behavior from
  IntrinsicEngine's generator; do not add overwrite, update, or general
  generator scope.
- Add the target state validator to CI before a pilot becomes normal
  repository policy. A disposable or local pilot may run it explicitly.

### P2 — Optional hypotheses and profiles

The following single-source ideas from IntrinsicEngine are not current
agent-kit priorities. Promote one only after its stated trigger is observed:

- **Maturity vocabulary:** test structure/reference/backend/parity/retirement
  labels only if an audit finds that agent-kit reported a scaffold or partial
  path as shipped. Keep the vocabulary only if a blind reviewer classifies the
  same evidence more accurately without material extra ceremony.
- **Periodic cross-task audit:** trial one bounded audit only if scope,
  documentation, or dead-seam drift escapes accepted per-task reviews. Keep it
  only if it finds distinct material issues at a justified review cost.
- **Micro-task profile:** test a smaller record only if measured pilot data
  shows that the current substantial-work protocol imposes disproportionate
  time on genuinely mechanical, single-slice work. It must not weaken the
  existing boundary around behavioral, interface, dependency, state, or
  durable-artifact changes.

Other optional, target-dependent profiles are:

- **Generated dependency-aware session brief** from IntrinsicEngine: valuable
  for large task graphs, unnecessary for a repository using one active task.
- **Session setup hook** from IntrinsicEngine/StructSplat/realtime-gs: useful
  when provisioning is idempotent and side effects are explicit.
- **Config-driven docs-sync and task validators** from IntrinsicEngine and
  StructSplat: provide extension points only when a target has corresponding
  policies.
- **Portable result bundle and viewer receipt** from realtime-gs: valuable for
  visual/interactive research, not a generic agent-kit requirement.
- **Artifact custody and one-shot authorization** from Prospect: valuable for
  protected confirmatory experiments, excessive for ordinary repository work.

## What Should Not Move into the Core

- StructSplat's renderer, numerical, rate-accounting, and task-area rules.
- realtime-gs's calibrated-scene, WebGL viewer, and Gaussian-specific gates.
- Prospect's epistemic object model and Q0/Q1 authorization schema.
- IntrinsicEngine's engine layering, CMake/CTest, Vulkan, method-manifest, and
  large task-prefix taxonomy.
- A universal task dependency graph or broad CI matrix.

These are examples of how repositories extend a coordination kernel, not
generic workflow rules.

## Assumptions

- The intended operating topology remains two cooperating agents, with human
  escalation for policy decisions.
- Existing checked-in workflow files are the authority; unrecorded social
  practices may change the recommendation.
- The target ARA ledgers and task histories must be preserved byte-for-byte
  unless a separate migration task explicitly changes them.
- Adoption should minimize duplicate state and should not require renumbering
  existing task or claim IDs.

## Known Failure Modes

1. **Dual authority:** adding a full agent-kit task tree beside an existing
   index or graph gives agents conflicting status and ownership.
2. **History contamination:** a template installation copies agent-kit's own
   tasks and ARA into a target.
3. **Scientific regression:** replacing specialized results audits with a
   generic code review weakens evidence.
4. **Reviewer theatre:** a "referee stance" without distinct identity or a
   durable verdict does not guarantee independence.
5. **Process overload:** mandatory full two-agent turns for micro changes can
   cost more than the risk they reduce.
6. **Mirror drift:** copied policy under AGENTS, CLAUDE, Codex, Copilot, and
   skill directories diverges without a canonical source and checker.
7. **Potential skill collision:** generic names could shadow one another when
   several repositories share a discovery surface. No live collision was
   reproduced in this assessment, so prevention is target-conditioned.
8. **False completion:** green structural or CPU checks are reported as proof
   of a real backend, held-out result, or deployed capability.

## Smallest Safe Decision Sequence

1. Completed in Task 004: fix and independently review agent-kit's distribution
   boundary and the disposable fresh-target, collision-refusal, no-history, and
   payload-allowlist regression.
2. If a target pilot becomes an explicit repository priority, add the
   read-only installation plan and frame only the named minimal coordination
   invariants in `realtime-gs`.
3. After one ordinary task and one results-bearing task, assess coordination
   time, duplicate-state incidents, handoff reconstruction, and material
   findings; then adopt, revise, or remove that pilot.
4. Run a separate Prospect pilot only if the realtime-gs result or a local
   Prospect coordination failure supports its cost. Preserve Prospect's
   multi-reviewer scientific gates.
5. Consider a narrow existing-schema identity/verdict experiment in
   StructSplat or IntrinsicEngine only after a concrete high-risk failure
   defines the need. Do not install a parallel workflow there.

## Open Questions

- Should independent review be mandatory for every substantial target task, or
  only research, architecture, critical implementation, and release tasks?
  The proposed realtime-gs pilot can measure this.
- How should a task record additional non-author scientific reviewers beyond
  the assigned final Reviewer?
- Which existing CI workflow should host the validator in Prospect and
  realtime-gs without duplicating their current gates?

## Implications for This Repository

The two-agent protocol should remain agent-kit's core. Task 004 made the
required deployment changes:

- distribute clean templates, not the repository's tracked history;
- expose an explicit, auditable payload boundary before any installation;
- support adaptation into an existing task authority rather than requiring a
  parallel one;
- preserve target repositories' specialist skills and resolve naming only
  when a preflight demonstrates a collision; and
- treat stronger target evidence systems as extensions to keep, not workflows
  to replace.

The present standing decision for all four repositories is **do not install as
normal policy and do not replace**. P0 makes a separately authorized bounded
pilot safe to package; it does not establish that any target should adopt
agent-kit.
