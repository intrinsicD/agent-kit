---
name: task-orchestration
description: Frame a repository task, assign Driver and Reviewer roles, define measurable success, and select the smallest useful skill sequence.
---

# Task Orchestration

Use this skill at the beginning of any non-trivial task.

## Procedure

1. Read `.agents/state/state.md` and `.agents/state/current-task.md`.
2. Inspect relevant code, tests, decisions, experiments, and open failures.
3. Classify the task:
   - Explore
   - Decide
   - Implement
   - Validate
   - Stabilize
   - Productize
4. Confirm the role assignment and turn recorded in
   `.agents/state/current-task.md`. If roles are unassigned, apply the role
   assignment rules in `AGENTS.md` and record the result, including any role
   swap from the previous task.
5. Define observable success criteria.
6. Write explicit non-goals.
7. Select the fewest applicable skills.
8. Propose the smallest sequence that can resolve the task.
9. Identify the main uncertainty and the cheapest way to reduce it.
10. Update `.agents/state/current-task.md`.

## Routing guidance

- Unclear methods or prior art → `research-methods`
- New algorithm or method ideas → `novel-idea-generation`
- Empirical uncertainty → `experiment-design`
- Defined behavior requiring code → `implementation`
- Independent challenge → `review-and-falsification`
- Critical correctness or performance → `code-audit`
- State or structure drift → `repo-organization`
- Validated functionality becoming user-facing → `productization`
- Agent exchange → `handoff`

## Anti-overengineering gate

Before approving a plan, answer:

- What current problem is being solved?
- Can a smaller experiment or vertical slice resolve it?
- Which proposed files, abstractions, or layers can be omitted?
- Is any work justified only by hypothetical future reuse?
- What is the reversal path?

Reject or shrink plans that cannot answer these questions.

## Output

Update `.agents/state/current-task.md` with:

- task id,
- role assignment and turn,
- mode,
- selected skills,
- measurable success criteria,
- constraints,
- non-goals,
- minimal plan,
- current status.
