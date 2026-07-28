# Repository Agent Operating Rules

This repository is operated by two cooperating agents.

The full workflow is implemented through reusable skills under `.agents/skills/`.
Do not duplicate those instructions in task prompts.

## Mandatory startup

Before doing substantial work:

1. Read `.agent/state.md`.
2. Read `.agent/current-task.md`.
3. Identify whether you are the `driver` or `reviewer`.
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
