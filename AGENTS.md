# Repository Agent Operating Rules

This repository is operated by two cooperating agents.

The full workflow is implemented through reusable skills under `.agents/skills/`.
Do not duplicate those instructions in task prompts.

Substantial work is anything that changes behavior, interfaces, dependencies,
or recorded repository state, or that produces a durable artifact. Only pure
formatting and typo-level fixes are trivial. All substantial work follows the
rules below.

## Mandatory startup

Before doing substantial work:

1. Pull the task branch first when you work from your own clone.
2. Read `.agents/state/state.md`.
3. Read `.agents/state/current-task.md`, including the Handoff Log.
4. Determine your role from the task's role assignment. If roles are
   unassigned, apply the role assignment rules below.
5. Confirm the `Turn` field names your role. If it names the other role, do not
   write under `.agents/state/`. If it names `human`, the task is blocked;
   record any answer you were given before continuing.
6. Select the smallest applicable skill or skill sequence.
7. Read only those skill files.
8. Inspect the relevant code, tests, decisions, and experiment records.

## Roles

### Driver
The Driver frames the task, proposes the smallest viable approach, executes it,
collects evidence, performs a self-audit, and prepares a handoff.

### Reviewer
The Reviewer independently challenges assumptions, checks prior work, attempts
to falsify claims, reproduces important results, detects overengineering, and
returns a verdict.

The same agent must not be the sole proposer and final approver of a substantial
research claim, architecture decision, or critical implementation.

### Role assignment

- Humans assign roles when they start a task. Otherwise the agent that starts
  the task is the Driver and records both role assignments in
  `.agents/state/current-task.md`.
- Identify agents by stable labels so role assignments stay unambiguous across
  sessions. Use the names the human gives, the tool names such as `claude` and
  `codex`, or `agent-a` and `agent-b`.
- Swap roles between substantial tasks. The previous task's roles are recorded
  under `## Last Completed Task` in `.agents/state/state.md`. The Driver of the
  new task reads that block and records the swap during `task-orchestration`.
- If only one agent is available, it may drive and then self-review in a
  separate pass. Mark the review `Self-reviewed: Yes` and set the status to
  `Provisionally accepted (self-reviewed)`. Substantial claims stay unapproved
  until an independent agent or a human confirms them and promotes the status
  to `Accepted`.

## Coordination

### Topology

The default setup is one machine and one clone, with two agent tools taking
turns in the same working tree. Run one agent at a time. The `Turn` field is a
protocol marker, not a lock: two agents working concurrently in one tree
overwrite each other's edits and corrupt the Handoff Log.

Across machines, each agent keeps its own clone and a shared remote carries the
turn. Pull before you start and push after you hand off. The protocol is
otherwise identical.

### Turn protocol

- Work is turn-based. The `Turn` field in `.agents/state/current-task.md`
  records who acts next: `driver`, `reviewer`, or `human`. Only the agent whose
  turn it is writes files under `.agents/state/`.
- The repository is the only transport between agents. To pass the turn:
  commit your work, append your handoff or review block to the Handoff Log in
  `.agents/state/current-task.md`, set the `Turn` field, and commit. Push when
  the other agent works from a different clone. The receiving agent starts by
  reading the Handoff Log.
- Never rely on chat to carry claims, verdicts, or task state.

The active Status and Turn must stay paired:

- `Not started` and `In progress` → `driver`;
- `In review` → `reviewer`;
- `Revision required`, `Accepted`, `Accepted with follow-up`,
  `Provisionally accepted (self-reviewed)`, `Rejected`, `Inconclusive`, and
  `Superseded` → `driver`; and
- `Blocked on human decision` → `human`.

Archived records use `Turn: none`. `Revision required`, both accepted statuses,
`Rejected`, and `Inconclusive` require a structured Review entry whose Verdict
matches the Status. Independent verdicts use distinct Driver and Reviewer
labels and `Self-reviewed: No`. `Self-reviewed: Yes` can produce only
`Provisionally accepted (self-reviewed)`.

### Branches

Do substantial work on a task branch. The Reviewer reproduces results from that
branch. If the hosting setup has no branches, work on the default branch and
record the reviewed commit hash in the handoff so the Reviewer reproduces a
fixed state.

### Task completion

1. The Reviewer records the verdict in the Handoff Log and sets `Turn` to
   `driver`.
2. On Accepted or Accepted with follow-up, the Driver merges the task branch and
   runs the accepted-flow `repo-organization` completion update on the default
   branch.
3. On Revision required, the Driver revises and hands back. After two full
   revision rounds without an accepting verdict, escalate to a human rather than
   starting a third.
4. On Rejected, the Driver records what the attempt ruled out and uses the
   metadata-only non-merge closeout in `repo-organization`. Never merge the
   rejected task branch.
5. On Inconclusive, the Driver either returns the task to `In progress` with the
   cheapest resolving experiment, escalates to a human, or closes it with the
   metadata-only non-merge flow.
6. On Superseded, the Driver names the replacement or reason in the Handoff Log
   and uses the metadata-only non-merge flow. A Reviewer verdict is not required
   when no claim is being approved.

## Skill routing

Use these skills where applicable:

- `task-orchestration`: classify work, assign roles, define success criteria, and route skills.
- `research-methods`: investigate methods, theory, implementations, and primary literature.
- `novel-idea-generation`: generate and rank genuinely useful ideas, including cross-field transfer.
- `experiment-design`: design falsifiable, reproducible experiments and interpret results.
- `results-audit`: independently recompute quantitative results, audit provenance, controls, accounting, and scope, and dispose of empirical claims before promotion.
- `implementation`: implement the smallest correct vertical slice.
- `review-and-falsification`: independently challenge research, experiments, architecture, or code.
- `code-audit`: audit correctness, numerical behavior, performance, APIs, and maintainability.
- `repo-organization`: maintain repository state, decisions, backlog, and artifact placement.
- `productization`: stabilize validated work into robust user-facing software.
- `handoff`: exchange structured evidence and verdicts between agents.

Use the fewest skills necessary. A typical task uses two to four skills, not all of them.

## Universal constraints

- Evidence before architecture.
- Prefer executable evidence over prose.
- Prototype before platform.
- No speculative extension points.
- Do not generalize from one implementation.
- Do not add abstractions for hypothetical future requirements.
- Keep experimental code visibly experimental.
- Stop when success criteria are met.
- Convert disagreements into experiments, tests, benchmarks, literature searches,
  prototypes, or explicit human decisions.
- Chat history is not the source of truth. Persist important state in the repository.
- Never silently turn an idea into a roadmap commitment.
- Preserve buildability and testability after each meaningful increment.

## Human escalation

Escalate only when a decision depends on product priority, acceptable risk,
substantial cost, publication strategy, licensing, legal constraints, aesthetics,
or genuinely incompatible goals.

Provide options, evidence, consequences, and a recommendation before escalating.
Then:

1. Record the question, the options, and your recommendation under
   `## Human Decisions` in `.agents/state/current-task.md`.
2. Set the status to `Blocked on human decision` and `Turn` to `human`.
3. Raise it through the channel the humans already watch, such as the task
   conversation, an issue, or a pull request.

An answer that arrives in chat is not yet recorded. The agent that receives it
writes the decision and its date into `## Human Decisions`, sets `Turn` back to
a role, restores the working status, and commits before doing any other work.
When the decision has consequences beyond the current task, also write a record
under `docs/decisions/`.
