#!/usr/bin/env python3
"""Validate the two-agent workflow installation and internal consistency.

Two groups of checks:

1. Installation: required files and directories, skill frontmatter, and
   agreement between the skill routing in AGENTS.md and the skills on disk.
2. Operating state: when a task is active, that its Turn, Status, and Task ID
   are legal and mutually consistent, and that archived task records are
   uniquely numbered.

The operating-state checks are skipped while `current-task.md` is an unfilled
template, so a fresh installation validates cleanly.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".agents/state/state.md",
    ".agents/state/current-task.md",
    ".agents/state/backlog.md",
    ".agents/state/ideas.md",
]

REQUIRED_DIRS = [
    ".agents/skills",
    "docs/decisions",
    "docs/research",
    "docs/experiments",
    "docs/audits",
    "docs/tasks",
]

REQUIRED_TASK_SECTIONS = [
    "Title",
    "Task ID",
    "Role Assignment",
    "Mode",
    "Goal",
    "Motivation",
    "Success Criteria",
    "Constraints",
    "Non-Goals",
    "Selected Skills",
    "Current Evidence",
    "Minimal Plan",
    "Status",
    "Human Decisions",
    "Handoff Log",
]

TURNS = {"driver", "reviewer", "human"}

STATUSES = {
    "Not started",
    "In progress",
    "In review",
    "Revision required",
    "Blocked on human decision",
    "Accepted",
    "Accepted with follow-up",
    "Provisionally accepted (self-reviewed)",
    "Rejected",
    "Inconclusive",
    "Superseded",
}

REVIEWED_STATUSES = {
    "Accepted",
    "Accepted with follow-up",
    "Provisionally accepted (self-reviewed)",
}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
ROUTING_SECTION = re.compile(
    r"^## Skill routing$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
REVIEW_HEADING = re.compile(r"^#{2,4}\s*Review\b", re.MULTILINE | re.IGNORECASE)
ARCHIVE_NAME = re.compile(r"^(\d{3,})-[a-z0-9-]+\.md$")

problems = []


def sections(text):
    """Split markdown into a {heading: body} map of its level-two sections."""
    found = {}
    heading = None
    body = []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading is not None:
                found[heading] = "\n".join(body).strip()
            heading = line[3:].strip()
            body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        found[heading] = "\n".join(body).strip()
    return found


def field(body, name):
    """Read a `- Name: value` field out of a section body.

    Horizontal whitespace only: `\\s*` would match the newline after an empty
    field and capture the following line as its value.
    """
    match = re.search(
        rf"^-[^\S\n]*{re.escape(name)}:[^\S\n]*(.*)$", body, re.MULTILINE
    )
    return match.group(1).strip() if match else ""


def is_placeholder(value):
    """Template alternatives such as `driver / reviewer / human` are unfilled."""
    return not value or "/" in value


# Installation ---------------------------------------------------------------

for relative in REQUIRED_FILES:
    if not (ROOT / relative).is_file():
        problems.append(f"missing file: {relative}")

for relative in REQUIRED_DIRS:
    if not (ROOT / relative).is_dir():
        problems.append(f"missing directory: {relative}")

skills_dir = ROOT / ".agents/skills"
disk_skills = set()
if skills_dir.is_dir():
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        disk_skills.add(entry.name)
        skill_file = entry / "SKILL.md"
        if not skill_file.is_file():
            problems.append(f"missing file: .agents/skills/{entry.name}/SKILL.md")
            continue
        match = FRONTMATTER.match(skill_file.read_text(encoding="utf-8"))
        if not match:
            problems.append(f"{entry.name}: SKILL.md has no frontmatter block")
            continue
        frontmatter = match.group(1)
        name = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        if not name or name.group(1) != entry.name:
            problems.append(
                f"{entry.name}: frontmatter name must match the directory name"
            )
        if not description or not description.group(1).strip():
            problems.append(f"{entry.name}: frontmatter description is missing")

agents_file = ROOT / "AGENTS.md"
if agents_file.is_file():
    routing = ROUTING_SECTION.search(agents_file.read_text(encoding="utf-8"))
    if not routing:
        problems.append("AGENTS.md: no `## Skill routing` section found")
    else:
        routed = set(re.findall(r"^- `([a-z0-9-]+)`:", routing.group(1), re.MULTILINE))
        for skill in sorted(disk_skills - routed):
            problems.append(f"{skill}: on disk but not listed in AGENTS.md skill routing")
        for skill in sorted(routed - disk_skills):
            problems.append(f"{skill}: listed in AGENTS.md skill routing but not on disk")

# Archived task records ------------------------------------------------------

archived_ids = {}
tasks_dir = ROOT / "docs/tasks"
if tasks_dir.is_dir():
    for entry in sorted(tasks_dir.glob("*.md")):
        if entry.name == "README.md":
            continue
        match = ARCHIVE_NAME.match(entry.name)
        if not match:
            problems.append(
                f"docs/tasks/{entry.name}: name must be <task-id>-<slug>.md, "
                "with a zero-padded id and a lowercase slug"
            )
            continue
        task_id = match.group(1)
        if task_id in archived_ids:
            problems.append(
                f"docs/tasks/{entry.name}: task id {task_id} already used by "
                f"{archived_ids[task_id]}"
            )
        else:
            archived_ids[task_id] = entry.name

# Active task ----------------------------------------------------------------

task_file = ROOT / ".agents/state/current-task.md"
if task_file.is_file():
    task = sections(task_file.read_text(encoding="utf-8"))

    for heading in REQUIRED_TASK_SECTIONS:
        if heading not in task:
            problems.append(f"current-task.md: missing `## {heading}` section")

    title = task.get("Title", "")
    roles = task.get("Role Assignment", "")
    turn = field(roles, "Turn").lower()
    status = task.get("Status", "")
    task_id = task.get("Task ID", "")

    # A titled task is an active one; an untitled file is still the template.
    if title:
        if not field(roles, "Driver"):
            problems.append("current-task.md: active task has no Driver")
        if not field(roles, "Reviewer"):
            problems.append("current-task.md: active task has no Reviewer")

        if is_placeholder(turn) or turn not in TURNS:
            problems.append(
                f"current-task.md: Turn must be one of {sorted(TURNS)}, found "
                f"{field(roles, 'Turn')!r}"
            )

        if is_placeholder(status) or status not in STATUSES:
            found = status.splitlines()[0] if status else ""
            problems.append(
                "current-task.md: Status must be one of the documented values, "
                f"found {found!r}"
            )
        else:
            if status in REVIEWED_STATUSES and not REVIEW_HEADING.search(
                task.get("Handoff Log", "")
            ):
                problems.append(
                    f"current-task.md: status {status!r} requires a Review block "
                    "in the Handoff Log"
                )
            if (status == "Blocked on human decision") != (turn == "human"):
                problems.append(
                    "current-task.md: status 'Blocked on human decision' and "
                    "Turn 'human' must be set together"
                )

        if not re.fullmatch(r"\d{3,}", task_id):
            found = task_id.splitlines()[0] if task_id else ""
            problems.append(
                "current-task.md: Task ID must be a zero-padded number, found "
                f"{found!r}"
            )
        elif task_id in archived_ids:
            problems.append(
                f"current-task.md: task id {task_id} is already archived as "
                f"docs/tasks/{archived_ids[task_id]}"
            )

if problems:
    print("Agent workflow validation failed:")
    for problem in problems:
        print(f"  - {problem}")
    sys.exit(1)

print("Agent workflow installation is complete and consistent.")
print(f"Found {len(disk_skills)} skills, all required state files and directories.")
if archived_ids:
    print(f"Archived tasks: {len(archived_ids)}. No active task issues found.")
