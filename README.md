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

Copy the contents of this folder into the root of a repository, including the
dotfiles. A plain `cp -r agent-kit/* target/` silently skips `.agents/`:

```bash
cp -r agent-kit/. target-repository/
```

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
any structural change. It checks two things:

- installation: required files, skill frontmatter, and agreement between the
  skill routing in `AGENTS.md` and the skills on disk;
- operating state: when a task is active, that its `Turn`, `Status`, and task id
  are legal and mutually consistent, that an accepted task actually has a review
  in its Handoff Log, and that archived task ids are unique.

The operating-state checks stay quiet while `current-task.md` is an unfilled
template, so a fresh installation validates cleanly.

## Wiring up the agent tools

The two roles are filled by two agent tools. Point each at the same files.

**Codex CLI** reads `AGENTS.md` natively; no setup needed.

**Claude Code** looks for `CLAUDE.md` and for skills under `.claude/skills/`.
Symlink both so there is one copy of everything:

```bash
ln -s AGENTS.md CLAUDE.md
mkdir -p .claude && ln -s ../.agents/skills .claude/skills
```

Other harnesses: most discover `AGENTS.md` on their own, and any harness with
native skill discovery can be pointed at `.agents/skills/`.

### One machine, one clone

This is the default. Both tools run in the same working tree and take turns.
**Run one agent at a time.** The `Turn` field records whose move it is, but it
is a marker, not a lock — two agents editing the tree at once will overwrite
each other's work and corrupt the Handoff Log.

Handing off is just a commit: the next agent reads the Handoff Log in
`.agents/state/current-task.md` and continues.

### Across machines

Each agent keeps its own clone of the same GitHub repository. The protocol is
identical, with two additions: pull before you start, and push after you set the
`Turn` field. Nothing else changes.

## Recommended first use

1. Fill in `.agents/state/state.md`.
2. Assign one agent as Driver and the other as Reviewer, using stable labels
   such as `claude` and `codex`. If you do not, the first agent to start a task
   becomes the Driver and records both role assignments, following the role
   assignment rules in `AGENTS.md`.
3. Create the first task in `.agents/state/current-task.md`.
4. The Driver begins with `task-orchestration`.
5. The Reviewer uses `review-and-falsification` and, when appropriate,
   `code-audit`.
6. Switch roles for the next substantial task. The completion update records the
   previous roles under `## Last Completed Task` in `state.md`, so the swap does
   not depend on anyone remembering.

Agents exchange work through the repository: each handoff and verdict is
appended to the Handoff Log in `.agents/state/current-task.md`, decisions that
need a human are recorded under `## Human Decisions`, and completed tasks are
archived under `docs/tasks/`. See `docs/tasks/000-example-task.md` for a
filled-in example of a completed task.

## Design principle

The skills contain procedures and acceptance criteria. The repository files
contain project-specific state and evidence. This keeps prompts short and avoids
a large, static process document.
