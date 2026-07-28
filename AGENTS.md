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

1. Read `.agents/state/state.md`.
2. Read `.agents/state/current-task.md`.
3. Determine your role from the task's role assignment. If roles are
   unassigned, apply the role assignment rules below.
4. Select the smallest applicable skill or skill sequence.
5. Read only those skill files.
6. Inspect the relevant code, tests, decisions, and experiment records.

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
- Identify agents by stable labels (names given by the human, or `agent-a` and
  `agent-b`) so role assignments stay unambiguous across sessions.
- Swap roles between substantial tasks. The Driver of the new task records the
  swap during `task-orchestration`.
- If only one agent is available, it may drive and then self-review in a
  separate pass, but it must label the verdict as self-reviewed, and
  substantial claims stay unapproved until an independent agent or a human
  confirms them.

## Coordination

- Work is turn-based. The `Turn` field in `.agents/state/current-task.md`
  records which role acts next. Only the agent whose turn it is writes files
  under `.agents/state/`.
- The repository is the only transport between agents. To pass the turn:
  commit your work, append your handoff or review block to the Handoff Log in
  `.agents/state/current-task.md`, set the `Turn` field to the other role, and
  commit. The receiving agent starts by reading the Handoff Log.
- Do substantial work on a task branch when the hosting setup supports
  branches. The Reviewer reproduces results from that branch. Merge only after
  the verdict is Accepted or Accepted with follow-up.
- Never rely on chat to carry claims, verdicts, or task state.

## Skill routing

Use these skills where applicable:

- `task-orchestration`: classify work, assign roles, define success criteria, and route skills.
- `research-methods`: investigate methods, theory, implementations, and primary literature.
- `novel-idea-generation`: generate and rank genuinely useful ideas, including cross-field transfer.
- `experiment-design`: design falsifiable, reproducible experiments and interpret results.
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
Record the escalation in the Handoff Log, set the task status to
`Blocked on human decision`, and raise it through the channel the humans
already watch, such as the task conversation, an issue, or a pull request.
