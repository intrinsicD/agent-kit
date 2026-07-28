#!/usr/bin/env python3
"""Regression tests for the documented two-agent workflow."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

STOCK_HANDOFF_LOG = """\
Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`."""

UNFILLED_TASK = """\
# Current Task

## Title

## Task ID

Next unused number in `docs/tasks/`, zero-padded (for example `007`).

## Role Assignment

- Driver:
- Reviewer:
- Turn: driver / reviewer / human

## Mode

Explore / Decide / Implement / Validate / Stabilize / Productize

## Goal

## Motivation

## Success Criteria

## Constraints

## Non-Goals

## Selected Skills

-

## Current Evidence

## Minimal Plan

## Status

Not started / In progress / In review / Revision required /
Blocked on human decision / Accepted / Accepted with follow-up /
Provisionally accepted (self-reviewed) / Rejected / Inconclusive / Superseded

## Human Decisions

Escalated questions and the answers humans gave. An answer that exists only in
chat is not recorded. Use one block per decision:

```markdown
### Question
### Options
### Recommendation
### Decision
### Date
```

## Handoff Log

Append Driver handoffs, Reviewer verdicts, escalations, and session completion
blocks here in chronological order. Entries use `###` headings and their fields
use `####` headings so every entry remains nested under this Handoff Log. Do
not delete earlier entries. On task completion this file is archived to
`docs/tasks/<task-id>-<slug>.md`.
"""


def review(verdict="Accepted", self_reviewed="No"):
    return textwrap.dedent(
        f"""\
        ### Review (reviewer, Reviewer)

        #### Verdict

        {verdict}

        #### Self-reviewed

        {self_reviewed}

        #### Correctness

        Checked.

        #### Evidence Quality

        Reproduced.

        #### Simplicity

        Minimal.

        #### Missing Cases

        None.

        #### Required Changes

        None.

        #### Optional Improvements

        None.
        """
    )


def superseded_reason():
    return textwrap.dedent(
        """\
        ### Session Completion (driver, Driver)

        #### Work completed

        Superseded by task 003.

        #### Recommended next action

        Continue with task 003.
        """
    )


def task_record(
    *,
    task_id="002",
    title="Exercise workflow validation",
    driver="driver",
    reviewer="reviewer",
    turn="driver",
    status="In progress",
    selected_skills="- `task-orchestration`",
    handoff_log="",
):
    indented_selected_skills = textwrap.indent(
        selected_skills.strip(), "        "
    )
    indented_handoff_log = textwrap.indent(handoff_log.strip(), "        ")
    return textwrap.dedent(
        f"""\
        # Current Task

        ## Title

        {title}

        ## Task ID

        {task_id}

        ## Role Assignment

        - Driver: {driver}
        - Reviewer: {reviewer}
        - Turn: {turn}

        ## Mode

        Validate

        ## Goal

        Exercise the workflow schema.

        ## Motivation

        Prevent invalid repository state.

        ## Success Criteria

        - The intended fixture has the documented result.

        ## Constraints

        - Use only disposable fixture state.

        ## Non-Goals

        - No product behavior changes.

        ## Selected Skills

{indented_selected_skills}

        ## Current Evidence

        - This is a regression fixture.

        ## Minimal Plan

        1. Run the validator.

        ## Status

        {status}

        ## Human Decisions

        None.

        ## Handoff Log

{indented_handoff_log}
        """
    )


class WorkflowFixture(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_current_task(self, text):
        (self.root / ".agents/state/current-task.md").write_text(
            text, encoding="utf-8"
        )

    def run_validator(self):
        return subprocess.run(
            [sys.executable, "scripts/validate_agent_workflow.py"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def assert_valid(self):
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stdout)

    def assert_invalid(self, expected_text):
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn(expected_text, result.stdout)


class AuditMatrixTests(WorkflowFixture):
    """The eleven cases reproduced by the workflow audit."""

    def test_documented_nested_review_is_accepted(self):
        self.write_current_task(
            task_record(
                status="Accepted",
                turn="driver",
                handoff_log=review(),
            )
        )
        self.assert_valid()

    def test_accepted_with_reviewer_turn_is_rejected(self):
        self.write_current_task(
            task_record(
                status="Accepted",
                turn="reviewer",
                handoff_log=review(),
            )
        )
        self.assert_invalid("requires Turn 'driver'")

    def test_identical_roles_cannot_independently_accept(self):
        self.write_current_task(
            task_record(
                driver="same-agent",
                reviewer="same-agent",
                status="Accepted",
                handoff_log=review(),
            )
        )
        self.assert_invalid(
            "independent review requires distinct Driver and Reviewer"
        )

    def test_review_focus_is_not_a_review(self):
        self.write_current_task(
            task_record(
                status="Accepted",
                handoff_log=(
                    "### Handoff (driver, Driver)\n\n"
                    "#### Review Focus\n\nCheck boundaries.\n"
                ),
            )
        )
        self.assert_invalid("requires a structured Review block")

    def test_self_review_cannot_grant_accepted_status(self):
        self.write_current_task(
            task_record(
                status="Accepted",
                handoff_log=review(self_reviewed="Yes"),
            )
        )
        self.assert_invalid(
            "Self-reviewed 'Yes' requires status "
            "'Provisionally accepted (self-reviewed)'"
        )

    def test_rejected_requires_review(self):
        self.write_current_task(task_record(status="Rejected"))
        self.assert_invalid("requires a structured Review block")

    def test_inconclusive_requires_review(self):
        self.write_current_task(task_record(status="Inconclusive"))
        self.assert_invalid("requires a structured Review block")

    def test_in_review_requires_reviewer_turn(self):
        self.write_current_task(task_record(status="In review", turn="driver"))
        self.assert_invalid("requires Turn 'reviewer'")

    def test_revision_required_requires_driver_turn(self):
        self.write_current_task(
            task_record(
                status="Revision required",
                turn="reviewer",
                handoff_log=review(verdict="Revision required"),
            )
        )
        self.assert_invalid("requires Turn 'driver'")

    def test_blank_title_does_not_hide_partial_active_state(self):
        self.write_current_task(
            task_record(
                title="",
                task_id="777",
                turn="sideways",
                status="Broken",
            )
        )
        self.assert_invalid("active task has no Title")

    def test_malformed_archive_is_rejected(self):
        (self.root / "docs/tasks/999-malformed.md").write_text(
            "# not a task record\n", encoding="utf-8"
        )
        self.assert_invalid("missing `## Title` section")


class ReviewerRegressionTests(WorkflowFixture):
    def test_template_rejects_extra_level_two_section(self):
        self.write_current_task(
            UNFILLED_TASK + "\n## Unexpected\n\nMust not be ignored.\n"
        )
        self.assert_invalid("unexpected `## Unexpected` section")

    def test_template_requires_root_heading(self):
        self.write_current_task(
            UNFILLED_TASK.removeprefix("# Current Task\n\n")
        )
        self.assert_invalid("root heading must be exactly '# Current Task'")

    def test_active_task_rejects_duplicate_sections(self):
        self.write_current_task(
            task_record() + "\n## Status\n\nIn progress\n"
        )
        self.assert_invalid("duplicate `## Status` section")

    def test_fenced_review_example_cannot_approve_task(self):
        fenced_review = textwrap.dedent(
            """\
            ### Handoff (driver, Driver)

            #### Evidence

            ```markdown
            ### Review

            #### Verdict

            Accepted

            #### Self-reviewed

            No

            ### End Example
            ```
            """
        )
        self.write_current_task(
            task_record(
                status="Accepted",
                handoff_log=fenced_review,
            )
        )
        self.assert_invalid("requires a structured Review block")

        fenced_fields = textwrap.dedent(
            """\
            ### Review (reviewer, Reviewer)

            ```markdown
            #### Verdict

            Accepted

            #### Self-reviewed

            No
            ```
            """
        )
        self.write_current_task(
            task_record(
                status="Accepted",
                handoff_log=fenced_fields,
            )
        )
        self.assert_invalid("Review 1 Verdict")

    def test_superseded_rejects_stock_handoff_instructions(self):
        self.write_current_task(
            task_record(
                status="Superseded",
                handoff_log=STOCK_HANDOFF_LOG,
            )
        )
        self.assert_invalid("requires a meaningful reason in the Handoff Log")

    def test_active_task_rejects_selected_skills_placeholder(self):
        self.write_current_task(task_record(selected_skills="-"))
        self.assert_invalid("must replace the '-' placeholder")


class ValidLifecycleTests(WorkflowFixture):
    def test_active_lifecycle_states(self):
        cases = [
            ("In progress", "driver", ""),
            ("In review", "reviewer", ""),
            (
                "Revision required",
                "driver",
                review(verdict="Revision required"),
            ),
            ("Accepted", "driver", review()),
            (
                "Accepted with follow-up",
                "driver",
                review(verdict="Accepted with follow-up"),
            ),
            ("Rejected", "driver", review(verdict="Rejected")),
            ("Inconclusive", "driver", review(verdict="Inconclusive")),
            ("Superseded", "driver", superseded_reason()),
        ]
        for status, turn, handoff_log in cases:
            with self.subTest(status=status):
                self.write_current_task(
                    task_record(
                        status=status,
                        turn=turn,
                        handoff_log=handoff_log,
                    )
                )
                self.assert_valid()

        self.write_current_task(task_record(status="Superseded"))
        self.assert_invalid("requires a meaningful reason in the Handoff Log")

    def test_provisional_self_review_is_valid(self):
        self.write_current_task(
            task_record(
                driver="solo-agent",
                reviewer="solo-agent",
                status="Provisionally accepted (self-reviewed)",
                handoff_log=review(self_reviewed="Yes"),
            )
        )
        self.assert_valid()

    def test_blocked_status_and_human_turn_are_paired(self):
        self.write_current_task(
            task_record(status="Blocked on human decision", turn="human")
        )
        self.assert_valid()


class ArchiveValidationTests(WorkflowFixture):
    def setUp(self):
        super().setUp()
        self.write_current_task(UNFILLED_TASK)

    def write_archive(self, filename_id, slug, **overrides):
        path = self.root / f"docs/tasks/{filename_id}-{slug}.md"
        values = {
            "task_id": filename_id,
            "turn": "none",
            "status": "Accepted",
            "handoff_log": review(),
        }
        values.update(overrides)
        path.write_text(task_record(**values), encoding="utf-8")
        return path

    def test_valid_terminal_archives(self):
        cases = [
            ("010", "accepted", "Accepted", review()),
            (
                "011",
                "accepted-follow-up",
                "Accepted with follow-up",
                review(verdict="Accepted with follow-up"),
            ),
            ("012", "rejected", "Rejected", review(verdict="Rejected")),
            (
                "013",
                "inconclusive",
                "Inconclusive",
                review(verdict="Inconclusive"),
            ),
            ("014", "superseded", "Superseded", superseded_reason()),
        ]
        for task_id, slug, status, handoff_log in cases:
            self.write_archive(
                task_id,
                slug,
                status=status,
                handoff_log=handoff_log,
            )
        self.assert_valid()

    def test_archive_task_id_must_match_filename(self):
        self.write_archive("010", "mismatch", task_id="011")
        self.assert_invalid("Task ID '011' does not match filename id '010'")

    def test_archive_requires_terminal_status(self):
        self.write_archive(
            "010",
            "active-status",
            status="In progress",
            handoff_log="",
        )
        self.assert_invalid("archived task Status must be terminal")

    def test_archive_requires_none_turn(self):
        self.write_archive("010", "live-turn", turn="driver")
        self.assert_invalid("archived task requires Turn 'none'")

    def test_archive_rejects_selected_skills_placeholder(self):
        self.write_archive("010", "placeholder-skills", selected_skills="-")
        self.assert_invalid("must replace the '-' placeholder")


class GitWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        self.root.mkdir()
        self.git_environment = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Workflow Test",
            "GIT_AUTHOR_EMAIL": "workflow@example.invalid",
            "GIT_COMMITTER_NAME": "Workflow Test",
            "GIT_COMMITTER_EMAIL": "workflow@example.invalid",
        }
        self.git("init", "-b", "main")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def git(self, *arguments, input_text=None):
        return subprocess.run(
            ["git", *arguments],
            cwd=self.root,
            env=self.git_environment,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        ).stdout.strip()

    def write(self, relative_path, contents):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    def commit_all(self, message):
        self.git("add", "-A")
        self.git("commit", "-m", message)

    def test_tracked_file_export_preserves_target_git_metadata(self):
        source = self.root
        self.write("tracked.txt", "from kit\n")
        self.commit_all("source")
        self.write("untracked.txt", "must not install\n")

        target = Path(self.temporary_directory.name) / "target"
        target.mkdir()
        subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=target,
            env=self.git_environment,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "https://example.invalid/original.git",
            ],
            cwd=target,
            env=self.git_environment,
            check=True,
        )
        (target / "target.txt").write_text("target history\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "target.txt"],
            cwd=target,
            env=self.git_environment,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "target history"],
            cwd=target,
            env=self.git_environment,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        original_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=target,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()

        archive = subprocess.Popen(
            ["git", "-C", str(source), "archive", "--format=tar", "HEAD"],
            stdout=subprocess.PIPE,
        )
        extraction = subprocess.run(
            ["tar", "-x", "-C", str(target)],
            stdin=archive.stdout,
            check=True,
        )
        archive.stdout.close()
        self.assertEqual(0, extraction.returncode)
        self.assertEqual(0, archive.wait())

        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=target,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        installed_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=target,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=target,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        self.assertEqual("https://example.invalid/original.git", remote)
        self.assertEqual(original_head, installed_head)
        self.assertEqual("main", branch)
        self.assertTrue((target / "tracked.txt").is_file())
        self.assertFalse((target / "untracked.txt").exists())

    def test_accepted_closeout_merges_task_changes(self):
        self.write(".agents/state/current-task.md", UNFILLED_TASK)
        self.write(".agents/state/state.md", "baseline\n")
        self.commit_all("baseline")

        self.git("switch", "-c", "task/accepted")
        self.write("implementation.txt", "accepted behavior\n")
        self.write(
            ".agents/state/current-task.md",
            task_record(status="Accepted", handoff_log=review()),
        )
        self.commit_all("accepted implementation and review")

        self.git("switch", "main")
        self.git("merge", "--no-ff", "task/accepted", "-m", "merge accepted task")
        self.write(
            "docs/tasks/002-accepted.md",
            task_record(
                turn="none",
                status="Accepted",
                handoff_log=review(),
            ),
        )
        self.write(".agents/state/current-task.md", UNFILLED_TASK)
        self.write(".agents/state/state.md", "accepted task recorded\n")
        self.commit_all("complete accepted task")

        self.assertTrue((self.root / "implementation.txt").is_file())
        self.assertTrue((self.root / "docs/tasks/002-accepted.md").is_file())
        self.assertEqual(
            UNFILLED_TASK,
            (self.root / ".agents/state/current-task.md").read_text(
                encoding="utf-8"
            ),
        )

    def test_terminal_metadata_closeout_excludes_unmerged_task_changes(self):
        for status in ("Rejected", "Inconclusive", "Superseded"):
            with self.subTest(status=status):
                case_root = (
                    Path(self.temporary_directory.name)
                    / status.lower().replace(" ", "-")
                )
                subprocess.run(
                    ["git", "clone", str(self.root), str(case_root)],
                    env=self.git_environment,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )

                def case_git(*arguments):
                    return subprocess.run(
                        ["git", *arguments],
                        cwd=case_root,
                        env=self.git_environment,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        check=True,
                    ).stdout.strip()

                state_path = case_root / ".agents/state/state.md"
                current_path = case_root / ".agents/state/current-task.md"
                state_path.parent.mkdir(parents=True, exist_ok=True)
                current_path.write_text(UNFILLED_TASK, encoding="utf-8")
                state_path.write_text("baseline\n", encoding="utf-8")
                case_git("add", "-A")
                case_git("commit", "-m", "baseline")

                branch = f"task/{status.lower().replace(' ', '-')}"
                case_git("switch", "-c", branch)
                (case_root / "rejected-implementation.txt").write_text(
                    "must stay off main\n", encoding="utf-8"
                )
                current_path.write_text(
                    task_record(
                        status=status,
                        handoff_log=(
                            superseded_reason()
                            if status == "Superseded"
                            else review(verdict=status)
                        ),
                    ),
                    encoding="utf-8",
                )
                case_git("add", "-A")
                case_git("commit", "-m", "task changes")

                archive_path = (
                    case_root
                    / f"docs/tasks/002-{status.lower().replace(' ', '-')}.md"
                )
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                archive_path.write_text(
                    task_record(
                        turn="none",
                        status=status,
                        handoff_log=(
                            superseded_reason()
                            if status == "Superseded"
                            else review(verdict=status)
                        ),
                    ),
                    encoding="utf-8",
                )
                current_path.write_text(UNFILLED_TASK, encoding="utf-8")
                state_path.write_text(f"{status} task recorded\n", encoding="utf-8")
                case_git("add", str(current_path), str(state_path), str(archive_path))
                case_git("commit", "-m", f"close {status.lower()} task")
                closeout_commit = case_git("rev-parse", "HEAD")

                case_git("switch", "main")
                case_git("cherry-pick", closeout_commit)

                self.assertFalse(
                    (case_root / "rejected-implementation.txt").exists()
                )
                self.assertTrue(archive_path.is_file())
                self.assertEqual(
                    UNFILLED_TASK, current_path.read_text(encoding="utf-8")
                )
                self.assertEqual(
                    f"{status} task recorded\n",
                    state_path.read_text(encoding="utf-8"),
                )


if __name__ == "__main__":
    unittest.main()
