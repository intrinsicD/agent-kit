# Two-Agent Repository Skills

A lightweight skill-based operating system for repositories developed by two
collaborating agents.

It supports:

- literature and method research,
- novel idea generation,
- cross-field method transfer,
- experiment planning and execution,
- quantitative results and claim auditing,
- implementation,
- independent review,
- scientific and code audits,
- repository organization,
- productization.

The workflow is intentionally minimal. `AGENTS.md` acts as a router, while the
detailed behavior lives in focused skills under `.agents/skills/`.

## Installation

The installable boundary is the named-group allowlist in
[`distribution/manifest.json`](distribution/manifest.json). Its `core` group
contains the 22 reusable payload files. Inspect it, create or choose an existing
target directory, then preview a namespaced installation from the agent-kit
checkout:

```bash
python3 agent-kit/scripts/install_agent_workflow.py \
  install target-repository --slug my-project --dry-run
```

The slug must match `^[a-z][a-z0-9-]*$` and contain at most 24 characters.
It prefixes all eleven skill directory names, frontmatter names, and
backtick-quoted cross-references so skills remain distinct in multi-repository
discovery surfaces. If the target is deliberately used in isolation, the
explicit escape hatch is `--no-prefix`:

```bash
python3 agent-kit/scripts/install_agent_workflow.py \
  install target-repository --no-prefix --dry-run
```

Remove `--dry-run` to install after reviewing the complete write plan and
collision report. The target directory must already exist. `core` is always
selected; repeat `--profile NAME` to add manifest groups when optional profiles
become available.

Before writing, the installer checks every selected destination, the generated
`.agents/kit-install.json` receipt, and every required parent. If any protected
path exists, is a symlink, or is blocked by a file/symlink ancestor, it reports
all collisions and exits without creating payload files. Files are created
exclusively, and an interrupted ordinary write rolls back only paths created by
that invocation. There is no overwrite, update, uninstall, or repair mode. Run
the installer while no other process is changing target paths; preflight is not
an adversarial filesystem transaction.

The payload contains the reusable authority, skills, validator, and separate
blank project-state/index templates. It deliberately excludes agent-kit's root
README, live state, ARA, audits, completed tasks, dated sessions, and regression
tests. It never enters `.git/`, so the target's history, branch, remotes, and
unrelated files remain owned by the target repository.

Expected slugged layout:

```text
repository/
├── AGENTS.md
├── .agents/
│   ├── kit-install.json
│   ├── skills/
│   │   ├── my-project-code-audit/
│   │   ├── my-project-implementation/
│   │   └── ... nine more prefixed skills
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

The receipt records the manifest version and SHA-256, selected slug/prefix and
groups, installation time, hashes for immutable payload files, and the paths of
user-owned templates. Diagnose an installation without modifying it:

```bash
python3 agent-kit/scripts/install_agent_workflow.py doctor target-repository
```

Doctor reports immutable files as `OK`, `MODIFIED`, or `MISSING`; state and
documentation templates are user-owned after installation and are checked only
as `PRESENT` or `MISSING`. A missing receipt reports an unknown installation
and falls back to bounded `core` presence checks. Exit codes are 0 for a clean
result, 1 for collisions/findings/install failure, and 2 for usage,
environment, manifest, or receipt-schema errors. Doctor never repairs or
writes.

The previous positional installer form is intentionally unsupported; use the
`install` subcommand and choose either `--slug` or `--no-prefix`.

### Opt-in verification profile

Select the `verify` profile during the initial installation to add a generic
target gate and CI wiring:

```bash
python3 agent-kit/scripts/install_agent_workflow.py \
  install target-repository --slug my-project --profile verify --dry-run
```

The profile is not an update mechanism: if `core` is already installed, the
existing receipt and payload correctly collide. A `core` + `verify` install
adds the same three standard-library checker files used by agent-kit, plus
three target-owned templates:

- `scripts/check_authority.py` detects divergent `AGENTS.md`/`CLAUDE.md`,
  duplicate physical skill roots, mismatched skill frontmatter names, and an
  optional `.codex/config.yaml` that does not reference `AGENTS.md`;
- `scripts/check_doc_links.py` resolves local Markdown links under the
  authority, README, `docs/`, state, and skill trees while ignoring fenced
  examples, external schemes, and same-document anchors;
- `scripts/check_docs_sync.py` evaluates repository-owned
  `docs-sync-rules.toml` obligations against explicit changed files or a Git
  merge base;
- `docs-sync-rules.toml`, `scripts/verify.sh`, and
  `.github/workflows/agent-workflow.yml` are editable templates. The target
  gate includes a marked `# TODO: repository-specific gates` extension point,
  and the workflow invokes that gate once instead of duplicating its stages.

Run the installed gate locally with:

```bash
./scripts/verify.sh
```

Authority and link findings warn by default when their checkers are invoked
directly; `--strict` changes findings to exit 1. The target gate runs both in
strict mode. `CLAUDE.md` may symlink to `AGENTS.md` or contain the exact marker
`<!-- agent-kit: authority=AGENTS.md -->`.

The shipped docs-sync rules file contains only a commented example. Add
target-specific `[[rule]]` entries with nonempty `trigger`, `one_of`, and
`reason` values, then supply the change set explicitly:

```bash
python3 scripts/check_docs_sync.py --root . --strict \
  --files src/example.py docs/example.md
python3 scripts/check_docs_sync.py --root . --strict --base origin/main
```

With configured rules, omitting both change-set options or using an
unresolvable Git base emits a skip warning and exits 0 in the default
warning-only mode; strict mode returns exit 2 because no reliable input was
available. An empty rules file passes without requiring Git.

Run `python3 scripts/validate_agent_workflow.py` after installation and after
any structural change. It checks two things:

- installation: required files, skill frontmatter, and agreement between the
  skill routing in `AGENTS.md` and the skills on disk;
- operating state: exact fresh-template recognition; active task role, mode,
  `Turn`, `Status`, task-id, structured-review, and self-review semantics; and
  complete archived records with unique, filename-matching ids, terminal
  statuses, `Turn: none`, and the required verdict.

The operating-state checks stay quiet only while `current-task.md` is the
complete unfilled template. A partially initialized record fails validation
instead of being mistaken for a fresh installation.

For source development, install the pinned development dependency and run the
single verification entry point after changing workflow or distribution
behavior:

```bash
python3 -m pip install -r requirements-dev.txt
./scripts/verify.sh
```

The command runs Ruff lint and formatting checks, validates workflow state,
strictly checks authority surfaces and local document links, checks the source
repository's claim ledger, and runs the full regression suite. The ARA checker,
source gate, development dependency, and tests are not installed into targets;
the optional `verify` profile instead ships the three generic checkers and a
distinct target gate.

## Evidence and claims

The source repository records durable capability and research claims in
[`ara/logic/claims.md`](ara/logic/claims.md). Each claim binds its status and
falsification criteria to repository evidence; `scripts/check_ara.py` enforces
the ledger's structure and on-disk proof links through `./scripts/verify.sh`.
The live ledger is project history and is deliberately excluded from the
distribution payload.

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
   `code-audit`. For quantitative or empirical claim promotion, the Reviewer
   also uses the optional `results-audit` skill.
6. Switch roles for the next substantial task. The completion update records the
   previous roles under `## Last Completed Task` in `state.md`, so the swap does
   not depend on anyone remembering.

Agents exchange work through the repository: each handoff and verdict is
appended to the Handoff Log in `.agents/state/current-task.md`, decisions that
need a human are recorded under `## Human Decisions`, and completed tasks are
archived under `docs/tasks/`. See `docs/examples/completed-task.md` for an
illustrative completed record that is intentionally outside operational task
history.

## Design principle

The skills contain procedures and acceptance criteria. The repository files
contain project-specific state and evidence. This keeps prompts short and avoids
a large, static process document.
