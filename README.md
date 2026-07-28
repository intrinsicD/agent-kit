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
│   ├── skills/
│   └── state/
│       ├── current-task.md
│       ├── state.md
│       ├── backlog.md
│       └── ideas.md
├── docs/
│   ├── decisions/
│   ├── research/
│   ├── experiments/
│   ├── audits/
│   └── tasks/
└── scripts/
    └── validate_agent_workflow.py
```

Run `python3 scripts/validate_agent_workflow.py` after installation and after
any structural change. It checks the required files, the skill frontmatter, and
that the skill routing in `AGENTS.md` matches the skills on disk.

Most agent harnesses automatically discover `AGENTS.md`. For harnesses with
native skill discovery, point them to `.agents/skills/`. For Claude Code:

```bash
mkdir -p .claude && ln -s ../.agents/skills .claude/skills
```

## Recommended first use

1. Fill in `.agents/state/state.md`.
2. Assign one agent as Driver and the other as Reviewer. If you do not,
   the first agent to start a task becomes the Driver and records both role
   assignments, following the role assignment rules in `AGENTS.md`.
3. Create the first task in `.agents/state/current-task.md`.
4. The Driver begins with `task-orchestration`.
5. The Reviewer uses `review-and-falsification` and, when appropriate,
   `code-audit`.
6. Switch roles for the next substantial task.

Agents exchange work through the repository: each handoff and verdict is
appended to the Handoff Log in `.agents/state/current-task.md`, and completed
tasks are archived under `docs/tasks/`. See
`docs/tasks/000-example-task.md` for a filled-in example of a completed task.

## Design principle

The skills contain procedures and acceptance criteria. The repository files
contain project-specific state and evidence. This keeps prompts short and avoids
a large, static process document.
