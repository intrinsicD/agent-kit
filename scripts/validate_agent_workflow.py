#!/usr/bin/env python3
"""Validate the two-agent workflow installation and internal consistency."""

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

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

problems = []

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
    routed = set(
        re.findall(r"^- `([a-z0-9-]+)`:", agents_file.read_text(encoding="utf-8"), re.MULTILINE)
    )
    for skill in sorted(disk_skills - routed):
        problems.append(f"{skill}: on disk but not listed in AGENTS.md skill routing")
    for skill in sorted(routed - disk_skills):
        problems.append(f"{skill}: listed in AGENTS.md skill routing but not on disk")

if problems:
    print("Agent workflow validation failed:")
    for problem in problems:
        print(f"  - {problem}")
    sys.exit(1)

print("Agent workflow installation is complete and consistent.")
print(f"Found {len(disk_skills)} skills, all required state files and directories.")
