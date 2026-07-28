#!/usr/bin/env python3
"""Validate the minimal two-agent workflow installation."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    ".agent/state.md",
    ".agent/current-task.md",
    ".agent/backlog.md",
    ".agent/ideas.md",
]

SKILLS = [
    "task-orchestration",
    "research-methods",
    "novel-idea-generation",
    "experiment-design",
    "implementation",
    "review-and-falsification",
    "code-audit",
    "repo-organization",
    "productization",
    "handoff",
]

missing = []

for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        missing.append(relative)

for skill in SKILLS:
    relative = f".agents/skills/{skill}/SKILL.md"
    if not (ROOT / relative).is_file():
        missing.append(relative)

if missing:
    print("Agent workflow validation failed. Missing:")
    for item in missing:
        print(f"  - {item}")
    sys.exit(1)

print("Agent workflow installation is complete.")
print(f"Found {len(SKILLS)} skills and all required state files.")
