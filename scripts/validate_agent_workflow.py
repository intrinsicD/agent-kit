#!/usr/bin/env python3
"""Validate installation and operating state for the two-agent workflow."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
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

REQUIRED_FILLED_TASK_SECTIONS = [
    "Title",
    "Goal",
    "Motivation",
    "Success Criteria",
    "Constraints",
    "Non-Goals",
    "Selected Skills",
    "Minimal Plan",
]

MODES = {
    "Explore",
    "Decide",
    "Implement",
    "Validate",
    "Stabilize",
    "Productize",
}

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

ACTIVE_STATUS_TURNS = {
    "Not started": "driver",
    "In progress": "driver",
    "In review": "reviewer",
    "Revision required": "driver",
    "Blocked on human decision": "human",
    "Accepted": "driver",
    "Accepted with follow-up": "driver",
    "Provisionally accepted (self-reviewed)": "driver",
    "Rejected": "driver",
    "Inconclusive": "driver",
    "Superseded": "driver",
}

TERMINAL_STATUSES = {
    "Accepted",
    "Accepted with follow-up",
    "Rejected",
    "Inconclusive",
    "Superseded",
}

REVIEW_VERDICTS = {
    "Accepted",
    "Accepted with follow-up",
    "Revision required",
    "Rejected",
    "Inconclusive",
}

STATUS_REVIEW_VERDICTS = {
    "Accepted": {"Accepted"},
    "Accepted with follow-up": {"Accepted with follow-up"},
    "Provisionally accepted (self-reviewed)": {
        "Accepted",
        "Accepted with follow-up",
    },
    "Revision required": {"Revision required"},
    "Rejected": {"Rejected"},
    "Inconclusive": {"Inconclusive"},
}

TASK_ID_TEMPLATE = (
    "Next unused number in `docs/tasks/`, zero-padded (for example `007`)."
)
MODE_TEMPLATE = "Explore / Decide / Implement / Validate / Stabilize / Productize"
STATUS_TEMPLATE = """\
Not started / In progress / In review / Revision required /
Blocked on human decision / Accepted / Accepted with follow-up /
Provisionally accepted (self-reviewed) / Rejected / Inconclusive / Superseded"""
ROLE_ASSIGNMENT_TEMPLATE = """\
- Driver:
- Reviewer:
- Turn: driver / reviewer / human"""
HUMAN_DECISIONS_TEMPLATE = """\
Escalated questions and the answers humans gave. An answer that exists only in
chat is not recorded. Use one block per decision:

```markdown
### Question
### Options
### Recommendation
### Decision
### Date
```"""
HANDOFF_LOG_TEMPLATE = """\
Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`."""
TASK_TEMPLATE_SECTIONS = {
    "Title": "",
    "Task ID": TASK_ID_TEMPLATE,
    "Role Assignment": ROLE_ASSIGNMENT_TEMPLATE,
    "Mode": MODE_TEMPLATE,
    "Goal": "",
    "Motivation": "",
    "Success Criteria": "",
    "Constraints": "",
    "Non-Goals": "",
    "Selected Skills": "-",
    "Current Evidence": "",
    "Minimal Plan": "",
    "Status": STATUS_TEMPLATE,
    "Human Decisions": HUMAN_DECISIONS_TEMPLATE,
    "Handoff Log": HANDOFF_LOG_TEMPLATE,
}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
ROUTING_SECTION = re.compile(
    r"^## Skill routing$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
REVIEW_BLOCK = re.compile(
    r"^### Review(?:[^\S\n]+\([^()\n]*\))?[^\S\n]*$\n?"
    r"(.*?)(?=^### |\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)
FENCE_OPEN = re.compile(r"^[ ]{0,3}(`{3,}|~{3,}).*$")
ARCHIVE_NAME = re.compile(r"^(\d{3,})-[a-z0-9-]+\.md$")


def markdown_lines(text):
    """Yield each line with whether it belongs to a fenced code block."""
    fence_character = None
    fence_length = 0
    for line in text.splitlines():
        if fence_character is not None:
            yield line, True
            closing_fence = re.fullmatch(
                rf"[ ]{{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[^\S\n]*",
                line,
            )
            if closing_fence:
                fence_character = None
                fence_length = 0
            continue

        opening_fence = FENCE_OPEN.match(line)
        if opening_fence:
            marker = opening_fence.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            yield line, True
        else:
            yield line, False


def without_fenced_code(text):
    """Blank fenced code while preserving line boundaries for Markdown scans."""
    return "\n".join(
        "" if is_fenced else line for line, is_fenced in markdown_lines(text)
    )


def sections(text, level=2, *, with_duplicates=False):
    """Split Markdown into a {heading: body} map at one heading level."""
    prefix = "#" * level + " "
    found = {}
    duplicates = set()
    heading = None
    body = []
    for line, is_fenced in markdown_lines(text):
        if not is_fenced and line.startswith(prefix):
            if heading is not None:
                if heading in found:
                    duplicates.add(heading)
                found[heading] = "\n".join(body).strip()
            heading = line[len(prefix) :].strip()
            body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        if heading in found:
            duplicates.add(heading)
        found[heading] = "\n".join(body).strip()
    if with_duplicates:
        return found, duplicates
    return found


def field_values(body, name):
    """Read visible `- Name: value` fields from a section body."""
    visible_body = without_fenced_code(body)
    matches = re.finditer(
        rf"^-[^\S\n]*{re.escape(name)}:[^\S\n]*(.*)$",
        visible_body,
        re.MULTILINE,
    )
    return [match.group(1).strip() for match in matches]


def review_blocks(handoff_log):
    """Return structured values from exact `### Review` log entries."""
    parsed = []
    review_text = without_fenced_code(handoff_log)
    for match in REVIEW_BLOCK.finditer(review_text):
        nested, duplicates = sections(match.group(1), level=4, with_duplicates=True)
        parsed.append(
            {
                "Verdict": nested.get("Verdict", "").strip(),
                "Self-reviewed": nested.get("Self-reviewed", "")
                .strip()
                .removesuffix("."),
                "Duplicate state fields": duplicates & {"Verdict", "Self-reviewed"},
            }
        )
    return parsed


def is_unfilled_task_template(task):
    """Recognize only the complete, unchanged active-task template."""
    return set(task) == set(TASK_TEMPLATE_SECTIONS) and all(
        task.get(heading) == expected
        for heading, expected in TASK_TEMPLATE_SECTIONS.items()
    )


def parse_task_document(text, source, problems):
    """Parse a task and validate its root and level-two heading structure."""
    task, duplicates = sections(text, with_duplicates=True)
    nonblank_lines = [line for line in text.splitlines() if line.strip()]
    root_headings = [
        line[2:].strip()
        for line, is_fenced in markdown_lines(text)
        if not is_fenced and line.startswith("# ") and not line.startswith("## ")
    ]
    if (
        not nonblank_lines
        or nonblank_lines[0].strip() != "# Current Task"
        or root_headings != ["Current Task"]
    ):
        problems.append(f"{source}: root heading must be exactly '# Current Task'")

    for heading in sorted(duplicates):
        problems.append(f"{source}: duplicate `## {heading}` section")

    unexpected = set(task) - set(REQUIRED_TASK_SECTIONS)
    for heading in sorted(unexpected):
        problems.append(f"{source}: unexpected `## {heading}` section")

    return task


def validate_reviews(task, source, status, driver, reviewer, problems):
    """Validate review structure and its relationship to task state."""
    reviews = review_blocks(task.get("Handoff Log", ""))

    for index, parsed_review in enumerate(reviews, start=1):
        verdict = parsed_review["Verdict"]
        self_reviewed = parsed_review["Self-reviewed"]
        for name in sorted(parsed_review["Duplicate state fields"]):
            problems.append(
                f"{source}: Review {index} has duplicate `#### {name}` field"
            )
        if verdict not in REVIEW_VERDICTS:
            problems.append(
                f"{source}: Review {index} Verdict must be one of "
                f"{sorted(REVIEW_VERDICTS)}, found {verdict!r}"
            )
        if self_reviewed not in {"Yes", "No"}:
            problems.append(
                f"{source}: Review {index} Self-reviewed must be 'Yes' or 'No', "
                f"found {self_reviewed!r}"
            )

    expected_verdicts = STATUS_REVIEW_VERDICTS.get(status)
    if not expected_verdicts:
        return
    if not reviews:
        problems.append(
            f"{source}: status {status!r} requires a structured Review block "
            "in the Handoff Log"
        )
        return

    latest = reviews[-1]
    verdict = latest["Verdict"]
    self_reviewed = latest["Self-reviewed"]
    if verdict not in expected_verdicts:
        problems.append(
            f"{source}: status {status!r} requires latest Review Verdict "
            f"in {sorted(expected_verdicts)}, found {verdict!r}"
        )

    provisional = status == "Provisionally accepted (self-reviewed)"
    if self_reviewed == "Yes" and not provisional:
        problems.append(
            f"{source}: Self-reviewed 'Yes' requires status "
            "'Provisionally accepted (self-reviewed)'"
        )
    if provisional and self_reviewed != "Yes":
        problems.append(
            f"{source}: status 'Provisionally accepted (self-reviewed)' "
            "requires Self-reviewed 'Yes'"
        )
    if self_reviewed == "No" and driver and reviewer and driver == reviewer:
        problems.append(
            f"{source}: independent review requires distinct Driver and Reviewer"
        )


def validate_task_record(
    task,
    source,
    problems,
    *,
    archived,
    filename_task_id=None,
):
    """Validate the shared schema for an active or archived task."""
    for heading in REQUIRED_TASK_SECTIONS:
        if heading not in task:
            problems.append(f"{source}: missing `## {heading}` section")

    for heading in REQUIRED_FILLED_TASK_SECTIONS:
        if not task.get(heading, ""):
            if heading == "Title":
                kind = "archived" if archived else "active"
                problems.append(f"{source}: {kind} task has no Title")
            else:
                problems.append(f"{source}: task has no {heading}")

    roles = task.get("Role Assignment", "")
    role_values = {
        name: field_values(roles, name) for name in ("Driver", "Reviewer", "Turn")
    }
    for name, values in role_values.items():
        if len(values) > 1:
            problems.append(f"{source}: duplicate Role Assignment field {name!r}")
    driver = role_values["Driver"][0] if role_values["Driver"] else ""
    reviewer = role_values["Reviewer"][0] if role_values["Reviewer"] else ""
    turn = role_values["Turn"][0].lower() if role_values["Turn"] else ""
    status = task.get("Status", "")
    task_id = task.get("Task ID", "")
    mode = task.get("Mode", "")

    if not driver:
        problems.append(f"{source}: task has no Driver")
    if not reviewer:
        problems.append(f"{source}: task has no Reviewer")

    if task.get("Selected Skills", "").strip() == "-":
        problems.append(f"{source}: Selected Skills must replace the '-' placeholder")

    if not re.fullmatch(r"\d{3,}", task_id):
        found = task_id.splitlines()[0] if task_id else ""
        problems.append(
            f"{source}: Task ID must be a zero-padded number, found {found!r}"
        )
    elif archived and filename_task_id != task_id:
        problems.append(
            f"{source}: Task ID {task_id!r} does not match filename id "
            f"{filename_task_id!r}"
        )

    if mode not in MODES:
        found = mode.splitlines()[0] if mode else ""
        problems.append(
            f"{source}: Mode must be one of {sorted(MODES)}, found {found!r}"
        )

    if status not in STATUSES:
        found = status.splitlines()[0] if status else ""
        problems.append(
            f"{source}: Status must be one of the documented values, found {found!r}"
        )
    elif archived:
        if status not in TERMINAL_STATUSES:
            problems.append(
                f"{source}: archived task Status must be terminal, found {status!r}"
            )
    else:
        expected_turn = ACTIVE_STATUS_TURNS[status]
        if turn != expected_turn:
            problems.append(
                f"{source}: status {status!r} requires Turn "
                f"{expected_turn!r}, found {turn!r}"
            )

    if archived:
        if turn != "none":
            problems.append(
                f"{source}: archived task requires Turn 'none', found {turn!r}"
            )
    elif turn not in {"driver", "reviewer", "human"}:
        problems.append(
            f"{source}: Turn must be 'driver', 'reviewer', or 'human', found {turn!r}"
        )

    if status in STATUSES:
        validate_reviews(task, source, status, driver, reviewer, problems)
        handoff_log = task.get("Handoff Log", "").strip()
        if status == "Superseded" and (
            not handoff_log or handoff_log == HANDOFF_LOG_TEMPLATE
        ):
            problems.append(
                f"{source}: status 'Superseded' requires a meaningful reason "
                "in the Handoff Log"
            )


def validate(root):
    """Return problems plus installation counts for one repository root."""
    problems = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            problems.append(f"missing file: {relative}")

    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            problems.append(f"missing directory: {relative}")

    skills_dir = root / ".agents/skills"
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

    agents_file = root / "AGENTS.md"
    if agents_file.is_file():
        routing = ROUTING_SECTION.search(agents_file.read_text(encoding="utf-8"))
        if not routing:
            problems.append("AGENTS.md: no `## Skill routing` section found")
        else:
            routed = set(
                re.findall(r"^- `([a-z0-9-]+)`:", routing.group(1), re.MULTILINE)
            )
            for skill in sorted(disk_skills - routed):
                problems.append(
                    f"{skill}: on disk but not listed in AGENTS.md skill routing"
                )
            for skill in sorted(routed - disk_skills):
                problems.append(
                    f"{skill}: listed in AGENTS.md skill routing but not on disk"
                )

    archived_ids = {}
    tasks_dir = root / "docs/tasks"
    if tasks_dir.is_dir():
        for entry in sorted(tasks_dir.glob("*.md")):
            if entry.name == "README.md":
                continue
            source = f"docs/tasks/{entry.name}"
            match = ARCHIVE_NAME.match(entry.name)
            filename_task_id = match.group(1) if match else None
            if not match:
                problems.append(
                    f"{source}: name must be <task-id>-<slug>.md, with a "
                    "zero-padded id and a lowercase slug"
                )
            elif filename_task_id in archived_ids:
                problems.append(
                    f"{source}: task id {filename_task_id} already used by "
                    f"{archived_ids[filename_task_id]}"
                )
            else:
                archived_ids[filename_task_id] = entry.name

            task = parse_task_document(
                entry.read_text(encoding="utf-8"), source, problems
            )
            validate_task_record(
                task,
                source,
                problems,
                archived=True,
                filename_task_id=filename_task_id,
            )

    task_file = root / ".agents/state/current-task.md"
    if task_file.is_file():
        task = parse_task_document(
            task_file.read_text(encoding="utf-8"),
            "current-task.md",
            problems,
        )
        if not is_unfilled_task_template(task):
            validate_task_record(
                task,
                "current-task.md",
                problems,
                archived=False,
            )
            task_id = task.get("Task ID", "")
            if re.fullmatch(r"\d{3,}", task_id) and task_id in archived_ids:
                problems.append(
                    f"current-task.md: task id {task_id} is already archived as "
                    f"docs/tasks/{archived_ids[task_id]}"
                )

    return problems, disk_skills, archived_ids


def main():
    problems, disk_skills, archived_ids = validate(ROOT)
    if problems:
        print("Agent workflow validation failed:")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print("Agent workflow installation and state validation passed.")
    print(f"Found {len(disk_skills)} skills, all required state files and directories.")
    print(f"Validated archived tasks: {len(archived_ids)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
