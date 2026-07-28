# Two-Agent Repository Skills

A lightweight skill-based operating system for repositories developed by two
collaborating agents.

It supports:

- literature and method research,
- novel idea generation,
- cross-field method transfer,
- experiment planning and execution,
- implementation,
- independent review,
- scientific and code audits,
- repository organization,
- productization.

The workflow is intentionally minimal. `AGENTS.md` acts as a router, while the
detailed behavior lives in focused skills under `.agents/skills/`.

## Installation

Copy the contents of this folder into the root of a repository.

Expected layout:

```text
repository/
├── AGENTS.md
├── .agents/
│   └── skills/
├── .agent/
│   ├── current-task.md
│   ├── state.md
│   ├── backlog.md
│   └── ideas.md
├── docs/
│   ├── decisions/
│   ├── research/
│   ├── experiments/
│   └── audits/
└── scripts/
    └── validate_agent_workflow.py
```

Most agent harnesses automatically discover `AGENTS.md`. For harnesses with
native skill discovery, point them to `.agents/skills/`.

## Recommended first use

1. Fill in `.agent/state.md`.
2. Create the first task in `.agent/current-task.md`.
3. Assign one agent as Driver and the other as Reviewer.
4. The Driver begins with `task-orchestration`.
5. The Reviewer uses `review-and-falsification` and, when appropriate,
   `code-audit`.
6. Switch roles for the next substantial task.

## Design principle

The skills contain procedures and acceptance criteria. The repository files
contain project-specific state and evidence. This keeps prompts short and avoids
a large, static process document.
