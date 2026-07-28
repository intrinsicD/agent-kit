# Research Note: Cross-Repository Agent Workflow Adoption

Date: 2026-07-29

## Research Question

Should the two-agent workflow in `agent-kit` be added to, or replace the
agentic workflows in `prospect`, `structsplat`, `realtime-gs`, and
`IntrinsicEngine`? Conversely, which workflow mechanisms in those repositories
should be integrated into `agent-kit` or replace part of it?

## Decision Summary

Do not replace any target repository's workflow wholesale, and do not run the
current `git archive HEAD` installation command against any of them.

The useful part of `agent-kit` is its independently validated coordination
kernel: explicit Driver and Reviewer identities, a turn marker, repository-
persisted handoffs, an independent terminal verdict, role rotation, and safe
merge versus non-merge closeout. That kernel is missing or informal in all four
targets. Their repository-specific experiment, task, evidence, validation, and
CI systems are stronger than the corresponding generic parts of `agent-kit`
and must remain authoritative.

| Repository | Disposition | Priority | Scope |
| --- | --- | --- | --- |
| `prospect` | Selectively adopt after the distribution blocker is fixed | High | Add the coordination kernel and a harness-neutral authority file; preserve the semantic/evidence contract, ARA, and both project skills. |
| `realtime-gs` | Adopt the clean coordination profile after the distribution blocker is fixed | Highest | It has no durable task system, so clean task state and handoffs fill a real gap; preserve all experiment, result-bundle, ARA, and domain-skill machinery. |
| `structsplat` | Integrate only independent-review and handoff semantics | Medium | Extend the existing task workflow/checker; do not add a second task archive, status authority, or backlog. |
| `IntrinsicEngine` | Do not install or replace; integrate only a high-risk review gate | Medium-low | Preserve its task graph, generated session brief, validators, CI, skills, and portable bootstrap. Add independent approval only for research claims, architecture decisions, and critical implementations. |

The first implementation task should be in `agent-kit`, not a target
repository: replace the tracked-tree archive installer with a clean,
manifest-driven generator or export that never ships this repository's own
state, audit history, ARA records, or regression fixtures.

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

### The current installer is not a distributable boundary

**Repository observation.** `agent-kit/README.md` installs every tracked path
with:

```text
git -C agent-kit archive --format=tar HEAD | tar -x -C target-repository
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

**Agent inference.** Collision safety prevents accidental overwrite, but it
does not make the tracked repository a clean installation payload. Deployment
must remain blocked until packaging is separated from development history.

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
- There is no generic durable task record, role assignment, turn marker,
  terminal verdict schema, workflow state validator, or branch closeout
  protocol.
- `make epistemic-diagnostics` completed successfully while reporting
  `claim_supported: false` and scoped blocking reasons for every maturity gate;
  the command did not turn green diagnostic predicates into unsupported
  capability claims.

#### Recommendation

**Selectively adopt the clean coordination profile; do not replace the current
workflow.**

After the distribution blocker is fixed:

1. Make one harness-neutral contract authoritative. Migrate the current
   `CLAUDE.md` substance into that authority and make other harness files thin
   redirects rather than maintaining competing policy.
2. Add clean, project-initialized Driver/Reviewer state and repository-
   persisted task handoffs.
3. Add the agent-kit state validator to CI.
4. Preserve both `prospect-*` skills, all ARA content, experiment rules,
   non-author scientific audits, and current CI.
5. Permit additional non-author scientific reviews beyond the single task
   Reviewer; one final task verdict must not replace Prospect's multi-pass
   evidence audits.

The expected benefit is cross-harness coordination and reproducible task
closure, not stronger scientific evidence—the target already has the stronger
evidence workflow.

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
- Results-bearing work has strong domain gates: real calibrated data, held-out
  discipline, append-only experiment records, source/config bindings, a
  portable `index.html`, preview artifacts, viewer receipts, and
  `check_results_bundle.py`.
- Docs, ARA, and script-layout checks pass. The 12 workflow-checker regression
  tests pass with `PYTHONPATH=src`; the repository-local `.venv` was absent, so
  the broader repository test gate was not run.

#### Recommendation

**Adopt the clean coordination profile; preserve every domain workflow.**

This is the best first pilot because the single-current-task model fills an
actual gap rather than duplicating a task graph:

1. Merge the current hard rules into one authoritative cross-harness contract.
2. Add clean task state, Driver/Reviewer turns, persisted handoffs, independent
   verdicts, and closeout validation.
3. Route existing `rtgs-*` and `realtime-gs-*` skills alongside the generic
   coordination skills; do not rename or replace them.
4. Add workflow validation to the existing CI job or a small structural job.
5. Leave the ARA, experiment log, result-bundle checker, real-data/viewer gate,
   and benchmark protocol untouched.

An initial pilot should complete one ordinary code task and one results-bearing
task before wider adoption.

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
- `structsplat-review` is primarily a pre-commit/self-review checklist.
  Results-bearing work has a referee skill, but ordinary substantial task
  acceptance does not require a distinct reviewer identity or persisted
  verdict.
- Structural checks and all seven workflow-checker tests pass.

#### Recommendation

**Do not install the full agent-kit state/task layout. Integrate only its
coordination invariants into the existing task system.**

Adding `.agents/state/current-task.md`, `.agents/state/backlog.md`, and
`docs/tasks/` would create a second status, backlog, and archive authority next
to `tasks/INDEX.md` and `tasks/done/`. Instead:

1. Extend the existing task workflow with Driver, Reviewer, and current-turn
   metadata for substantial active work.
2. Persist handoff and review blocks in the task record or a linked review
   artifact.
3. Require an independent terminal verdict for substantial research claims,
   architecture decisions, and critical implementations.
4. Extend `check_task_policy.py` or a focused companion checker to reject
   self-approved terminal work and invalid turn/verdict combinations.
5. Preserve the current task IDs, INDEX outcome authority, ADR discipline,
   ARA checker, domain skills, verification script, and CI.

This gains agent-kit's principal safety property without duplicating the
repository's stronger task and evidence machinery.

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
- The shipped handoff skill writes conversational state to the OS temporary
  directory, which is useful for context compaction but is not durable
  repository evidence.

#### Recommendation

**Do not replace or side-load the full agent-kit workflow.**

IntrinsicEngine already exceeds agent-kit in authority management, task
planning, maturity, validation, CI, and portable bootstrapping. A second
`.agents/state` and `docs/tasks` lifecycle would be a regression.

Integrate only these two-agent properties:

1. For substantial research claims, architecture decisions, and critical
   implementations, record distinct proposer and reviewer identities plus a
   terminal verdict in the existing task/PR record.
2. Persist review-relevant handoff claims and evidence in the repository.
   Retain the temporary handoff skill for conversation compaction, but do not
   use it as the only transport for approval state.

Do not impose per-task two-agent turns on routine slices; that would conflict
with the repository's deliberately bounded weekly audit and micro-task model.

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

### Selective coordination integration

Selected. Preserve each target's authority and domain workflow, then add only
the missing independently reviewed coordination semantics. Realtime-gs and
Prospect can use a clean single-current-task profile; StructSplat and
IntrinsicEngine should adapt the invariants into their existing task systems.

## Relevant Implementations to Bring Back into `agent-kit`

### P0 — Required before deployment

#### Replace the archive installer with a clean generator/export manifest

**Source:** `IntrinsicEngine/tools/agentkit`.

Replace the current installation section and tracked-tree export with a
template generator or explicit payload manifest that:

- emits blank project state rather than agent-kit's current state;
- excludes agent-kit's ARA, audits, completed task history, and test evidence
  from target project history;
- supports dry-run, collision reporting, idempotent create/skip behavior, and
  an explicit overwrite mode;
- accepts the target project name, slug, authority filename, verification
  commands, and enabled harnesses;
- offers a coordination-only output for repositories with existing task and
  evidence systems; and
- self-tests in disposable repositories.

This should replace, not merely supplement, `git archive HEAD | tar`.

#### Make authority and skill discovery collision-resistant

**Sources:** IntrinsicEngine, StructSplat, realtime-gs.

- Generate one authoritative contract and thin harness redirects.
- Prefix installed skill names with the target repository slug.
- Mirror or symlink skills from one canonical location.
- Check authority and mirror drift.

The current unprefixed generic skill names are safe inside one repository but
ambiguous when multiple repositories expose skills in one agent session.

#### Ship an optional CI gate

**Sources:** all three repositories with structural workflow CI.

Provide a minimal workflow that runs the state validator and workflow
regressions. Local validation without CI allows a malformed handoff or archive
to merge unnoticed.

### P1 — High-value, bounded additions

#### Add a generic research-results audit skill

**Sources:** Prospect, StructSplat, realtime-gs.

`experiment-design` specifies a good experiment and
`review-and-falsification` challenges conclusions, but neither currently
requires a results claim table, raw recomputation, exact source/config binding,
control/accounting audit, evidence-scope classification, and explicit
confirm/narrow/refute/retire disposition.

Add this as an optional research profile, not a universal software-task gate.
Repository-specific rules such as complete-stream bit accounting, calibrated
viewer handoffs, or checkpoint custody remain local extensions.

#### Add a compact maturity vocabulary to implementation and review

**Source:** IntrinsicEngine.

Adopt the distinction between structure existing, a CPU/reference contract
being tested, a real backend/path operating, parity being proven, and legacy
code being retired. Keep it descriptive and optional; its purpose is to stop a
scaffold from being reported as a shipped capability.

#### Add periodic cross-task audit guidance

**Source:** IntrinsicEngine's weekly agent-output and drift audits.

Independent per-task review does not detect recurring scope creep, ceremonial
work, accumulated dead seams, or documentation claims that drift across
several accepted tasks. Add a bounded periodic audit as an optional additive
skill. It must not replace per-task independent review.

#### Right-size trivial and single-slice work

**Source:** IntrinsicEngine's micro-task model.

Agent-kit already exempts pure formatting and typo-level fixes. A small task
record profile for single-slice mechanical work could reduce ceremony without
weakening behavioral, interface, dependency, or research changes.

### P2 — Optional profiles, not core replacements

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
7. **Skill collision:** generic names from multiple open repositories shadow
   one another.
8. **False completion:** green structural or CPU checks are reported as proof
   of a real backend, held-out result, or deployed capability.

## Smallest Safe Adoption Sequence

1. Fix and independently review agent-kit's distribution boundary.
2. Add a disposable-repository installation test proving that generated state
   is blank and no development history is shipped.
3. Pilot the coordination profile in `realtime-gs`.
4. After one ordinary task and one results-bearing task, assess coordination
   cost, duplicate-state incidents, and whether independent review found
   material issues.
5. Apply the same clean profile to `prospect`, preserving its multi-reviewer
   scientific gates.
6. Separately propose narrow checker/task-schema changes for StructSplat and
   IntrinsicEngine; do not install the full profile there.

## Open Questions

- Should independent review be mandatory for every substantial target task, or
  only research, architecture, critical implementation, and release tasks?
  Realtime-gs is the best pilot to measure this.
- Should the generator own a `coordination-only` profile, or should the clean
  payload always be coordination-only with task/evidence modules explicitly
  added? The four-target evidence favors the latter.
- How should a task record additional non-author scientific reviewers beyond
  the assigned final Reviewer?
- Which existing CI workflow should host the validator in Prospect and
  realtime-gs without duplicating their current gates?

## Implications for This Repository

The two-agent protocol should remain agent-kit's core. Its deployment and
integration model should change substantially:

- distribute clean templates, not the repository's tracked history;
- install into existing repositories through explicit, project-aware
  generation;
- support adaptation into an existing task authority rather than requiring a
  parallel one;
- preserve repository-prefixed specialist skills; and
- treat stronger target evidence systems as extensions to keep, not workflows
  to replace.

Until the P0 distribution work is complete, the correct answer for all four
repositories is **assess and adapt, but do not install**.
