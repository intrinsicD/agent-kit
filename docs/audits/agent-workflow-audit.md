# Audit: Two-Agent Repository Workflow

Date: 2026-07-28

## Scope

This audit covers the workflow contract in `AGENTS.md`, the task and repository
state templates, all ten routed skills, the installation and operating guidance
in `README.md`, the completed-task example, and
`scripts/validate_agent_workflow.py`.

The review asks whether a fresh user can install the kit safely, whether agents
can follow the documented lifecycle without inventing missing steps, and
whether the validator rejects states that violate the workflow's core
single-writer and independent-review guarantees.

## Overall Assessment

**Revision required.** The workflow has a clear, deliberately small conceptual
model, and the baseline installation validator passes. It is not safe to
recommend in its current form, however: the documented installation command can
replace a target repository's Git metadata, the handoff skill emits review
markup that the validator rejects, and the validator accepts states that bypass
independent approval.

## Remediation Status

Task 002 contains a candidate remediation for all six findings, pending
independent review:

- installation now exports only tracked files with `git archive` and documents
  collision preflight and overwrite behavior;
- Handoff Log templates use nested `###` entries and `####` fields;
- active and archived records share explicit role, mode, status, turn,
  structured-verdict, and self-review validation;
- accepted branches have a merge flow, while Rejected, closed Inconclusive, and
  Superseded branches use a tested metadata-only closeout commit;
- only the complete untouched task template bypasses active validation, and
  archives require a complete schema, matching id, terminal status, and
  `Turn: none`; and
- the illustrative record now lives under `docs/examples/`, outside operational
  history.

The candidate passes 21 automated regression tests, including the eleven-case
audit matrix, valid active/archive lifecycles, tracked-only installation, and
accepted/non-merge Git closeout probes. The findings and original verdict below
remain the historical assessment of the pre-remediation workflow until the
Reviewer returns a verdict on Task 002.

## Findings

### F1 — Critical: the installation command copies `.git/` into the target

`README.md:23-28` recommends:

```bash
cp -r agent-kit/. target-repository/
```

The `/.` source form includes every dotfile and dot-directory, including
`agent-kit/.git/`. When the destination is already a Git repository, GNU `cp`
merges the kit's Git database into the destination and overwrites matching
metadata.

A disposable target repository was initialized with
`origin=https://example.invalid/original-target.git`, then the documented
command was run from this checkout. Afterwards:

```text
before remote: https://example.invalid/original-target.git
after remote:  https://github.com/intrinsicD/agent-kit.git
after branch:  task/001-agent-workflow-audit
after HEAD:    b5c8d06
```

The command also copies untracked local files, not just the kit's intended
contents.

**Required fix:** replace the command with a tracked-file export that excludes
Git metadata, for example:

```bash
git -C agent-kit archive --format=tar HEAD | tar -x -C target-repository
```

Document collision behavior for files that already exist in the target.

### F2 — High: the handoff templates are incompatible with the validator

The Handoff Log is a level-two section. Both the handoff skill
(`.agents/skills/handoff/SKILL.md:27-61`) and the review skill
(`.agents/skills/review-and-falsification/SKILL.md:45-58`) tell agents to append
new level-two `## Handoff` and `## Review` sections inside it.

The validator's `sections()` function treats every `##` heading as a new
top-level section (`scripts/validate_agent_workflow.py:90-105`). It then looks
for a Review heading only inside the truncated body of `## Handoff Log`
(`scripts/validate_agent_workflow.py:231-238`). Consequently, an Accepted task
using the skill's exact `## Review` template fails with:

```text
current-task.md: status 'Accepted' requires a Review block in the Handoff Log
```

The illustrative task happens to use `### Handoff` and `### Review`
(`docs/tasks/000-example-task.md:78-118`), which is compatible with the parser
but contradicts the reusable skills.

**Required fix:** establish one schema. The smallest change is to make Handoff
Log entries level three and their fields level four in both skills, matching the
example. Add a fixture generated from the documented templates.

### F3 — High: independent approval and turn transitions are not enforced

The workflow says the same agent cannot be sole proposer and final approver
(`AGENTS.md:35-58`) and that the Reviewer returns the turn to the Driver after a
verdict (`AGENTS.md:92-100`). The validator checks only that both role labels
are non-empty, that a broad `Review` heading exists for accepted statuses, and
that `human` is paired with the blocked status
(`scripts/validate_agent_workflow.py:206-255`).

Disposable fixtures demonstrated that the validator accepts all of these:

| Invalid state | Validator result |
| --- | --- |
| `Accepted` with `Turn: reviewer` | Pass |
| identical Driver and Reviewer labels | Pass |
| `Accepted` with only a `### Review Focus` heading and no verdict | Pass |
| `Accepted` with `Self-reviewed: Yes` | Pass |
| `Rejected` with no review | Pass |
| `Inconclusive` with no review | Pass |
| `In review` with `Turn: driver` | Pass |
| `Revision required` with `Turn: reviewer` | Pass |

The false-positive heading occurs because
`^#{2,4}\s*Review\b` also matches `Review Focus`
(`scripts/validate_agent_workflow.py:84`). Rejected and Inconclusive are omitted
from `REVIEWED_STATUSES` (`scripts/validate_agent_workflow.py:74-78`) even
though the lifecycle requires a Reviewer verdict before either outcome can be
handled.

**Required fix:** parse a structured review block and validate its Verdict and
Self-reviewed fields. Encode the allowed status/turn transitions. Require
distinct role labels for independent acceptance; permit a same-agent review
only with `Provisionally accepted (self-reviewed)`.

### F4 — High: rejected work has no safe branch-completion path

All substantial work must occur on a task branch (`AGENTS.md:85-90`). Accepted
work is merged before the completion update, but Rejected work must be archived
without merging (`AGENTS.md:92-104`). The archive procedure reads and resets
the task branch's active state and updates repository state
(`.agents/skills/repo-organization/SKILL.md:59-76`).

Following those instructions leaves an impossible choice:

- archive on the task branch, in which case the durable rejection record never
  reaches the default branch; or
- merge the branch, which also integrates the rejected implementation.

A selective metadata transfer could solve this, but no such sequence is
defined. Inconclusive is also described both as something to archive and as a
state from which the Driver defines another experiment. `Superseded` is an
allowed status but has no completion rule.

**Required fix:** define and test terminal flows for Accepted, Rejected,
Inconclusive, and Superseded. For rejected work, create a metadata-only closeout
commit that can be applied to the default branch without the rejected changes,
or provide an equivalent automated close command.

### F5 — Medium: corrupted active and archived state can bypass validation

The validator decides that a task is active solely from a non-empty Title
(`scripts/validate_agent_workflow.py:206-213`). A fixture with a blank title but
`Task ID: 000`, an invalid Turn, and an invalid Status passed as an unfilled
template.

Archived task files are checked only for filename shape and duplicate numeric
ids (`scripts/validate_agent_workflow.py:172-194`). A file named
`999-malformed.md` containing only `# not a task record` passed, even though
archived records are the source of truth for handoffs, verdicts, role rotation,
and negative results.

**Required fix:** recognize the template by all of its sentinel values (or an
explicit state marker), not by Title alone. Reuse the task schema for archives,
requiring `Turn: none`, a terminal Status, matching Task ID, and the appropriate
review semantics.

### F6 — Medium: the example task is accidentally treated as real history

The role-assignment skill says that when `Last Completed Task` is empty, agents
must fall back to the most recent file in `docs/tasks/`
(`.agents/skills/task-orchestration/SKILL.md:23-27`). On a fresh install the
only such file is `000-example-task.md`, which explicitly says it is not real
history (`docs/tasks/000-example-task.md:1-4`;
`docs/tasks/README.md:16-17`).

This conflicts with the first-use rule that the initiating agent becomes the
Driver (`README.md:97-103`). It also makes the validator report one archived
task on a fresh kit.

**Required fix:** move the example outside `docs/tasks/`, or explicitly exclude
it from role fallback, archive counts, collision checks, and next-id selection.

## Evidence

Commands executed:

```text
git pull --ff-only
python3 scripts/validate_agent_workflow.py
python3 -m py_compile scripts/validate_agent_workflow.py
```

The baseline validator passed and reported ten routed skills and one archived
task. Eleven disposable fixture checks were then run: the documented level-two
review was the one valid state rejected; the eight invalid transition/approval
states in F3, the blank-title partial state, and a malformed archive were all
accepted.

The installation probe and all validator fixtures were created under temporary
directories; they did not modify the reviewed repository.

## Required Fixes

1. Replace the destructive installation command.
2. Make Handoff Log templates and parsing agree.
3. Validate review semantics, role independence, and status/turn transitions.
4. Define executable closeout paths for every terminal status on task branches.
5. Validate partially initialized and archived task records.
6. Remove the illustrative task from operational history.

## Optional Improvements

- Add an automated test suite around the validator using the fixture matrix
  above plus valid lifecycle fixtures.
- Add one end-to-end dry run covering task initialization, Driver handoff,
  Reviewer revision, acceptance, merge, archive, and role swap.
- Print a narrower success message: the current
  “installation is complete and consistent” overstates what is checked.

## Residual Risks

The Turn field remains a cooperative marker rather than a lock. The repository
documents this limitation for a shared worktree, but two independently started
agents can still read the same turn before either commits. Git will expose some
cross-machine races as push conflicts; it cannot prevent concurrent writes in
one working tree. Any deployment that cannot guarantee sequential invocation
needs an external lock or compare-and-swap mechanism.

## Verdict

**Revision required.** The design is understandable and salvageable without a
large rewrite, but F1-F4 block safe adoption.
