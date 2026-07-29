#!/usr/bin/env python3
"""Regression tests for the single verification entry point and CI mirror."""

from pathlib import Path
import re
import stat
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VERIFY_SCRIPT = REPOSITORY_ROOT / "scripts/verify.sh"
CI_WORKFLOW = REPOSITORY_ROOT / ".github/workflows/ci.yml"
DEVELOPMENT_REQUIREMENTS = REPOSITORY_ROOT / "requirements-dev.txt"
RUFF_CONFIGURATION = REPOSITORY_ROOT / "pyproject.toml"

EXPECTED_STAGES = (
    "ruff check .",
    "ruff format --check .",
    "PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py",
    "PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_ara.py",
    "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v",
)
TRAILING_SHELL_COMMENT = re.compile(r"\s+#.*$")


def normalized_shell_lines(script_text):
    return [
        TRAILING_SHELL_COMMENT.sub("", line.strip()).rstrip()
        for line in script_text.splitlines()
    ]


class VerificationEntryPointTests(unittest.TestCase):
    def test_verify_script_runs_exactly_the_five_documented_stages(self):
        lines = VERIFY_SCRIPT.read_text(encoding="utf-8").splitlines()
        executable_lines = normalized_shell_lines("\n".join(lines))
        stage_commands = []
        for index, line in enumerate(lines):
            if not line.startswith('echo "['):
                continue
            command_index = index + 1
            while command_index < len(lines) and not lines[command_index].strip():
                command_index += 1
            self.assertLess(command_index, len(lines), f"stage at line {index + 1}")
            stage_commands.append(lines[command_index].strip())

        self.assertEqual(EXPECTED_STAGES, tuple(stage_commands))
        for expected in EXPECTED_STAGES:
            self.assertEqual(
                1,
                executable_lines.count(expected),
                f"gate command must occur exactly once: {expected}",
            )

    def test_trailing_comment_cannot_hide_duplicate_gate(self):
        script = VERIFY_SCRIPT.read_text(encoding="utf-8")
        duplicated = f"{script}\n{EXPECTED_STAGES[3]} # duplicated gate\n"
        executable_lines = normalized_shell_lines(duplicated)
        self.assertEqual(2, executable_lines.count(EXPECTED_STAGES[3]))

    def test_verify_script_is_executable_posix_shell(self):
        self.assertEqual("#!/bin/sh", VERIFY_SCRIPT.read_text().splitlines()[0])
        mode = VERIFY_SCRIPT.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR)

    def test_ci_matrix_invokes_verify_verbatim(self):
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('python-version: ["3.11", "3.12", "3.13"]', workflow)
        self.assertEqual(1, workflow.count("run: ./scripts/verify.sh"))
        for command in EXPECTED_STAGES:
            self.assertNotIn(command, workflow)

    def test_ruff_version_and_python_floor_are_explicit(self):
        self.assertEqual(
            "ruff==0.15.20\n",
            DEVELOPMENT_REQUIREMENTS.read_text(encoding="utf-8"),
        )
        self.assertIn(
            'target-version = "py311"',
            RUFF_CONFIGURATION.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
