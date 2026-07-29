#!/usr/bin/env python3
"""Regression tests for the versioned, non-overwriting distribution payload."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPOSITORY_ROOT / "scripts/install_agent_workflow.py"
MANIFEST = REPOSITORY_ROOT / "distribution/manifest.json"
GIT_ENVIRONMENT = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Workflow Test",
    "GIT_AUTHOR_EMAIL": "workflow@example.invalid",
    "GIT_COMMITTER_NAME": "Workflow Test",
    "GIT_COMMITTER_EMAIL": "workflow@example.invalid",
}


def load_installer_module():
    spec = importlib.util.spec_from_file_location(
        "agent_workflow_installer_under_test", INSTALLER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load installer from {INSTALLER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


INSTALLER_MODULE = load_installer_module()


def run(arguments, cwd=None, check=False):
    return subprocess.run(
        arguments,
        cwd=cwd,
        env=GIT_ENVIRONMENT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def workspace_snapshot(root):
    """Capture every target path except Git internals."""

    snapshot = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if relative.parts[0] == ".git":
            continue
        key = relative.as_posix()
        if path.is_symlink():
            snapshot[key] = ("symlink", os.readlink(path))
        elif path.is_file():
            snapshot[key] = ("file", path.read_bytes())
        elif path.is_dir():
            snapshot[key] = ("directory",)
    return snapshot


def manifest_rows():
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return document, document["groups"]["core"]


def install_command(target, *options):
    return [
        sys.executable,
        str(INSTALLER),
        "install",
        str(target),
        *options,
    ]


class DistributionBoundaryTests(unittest.TestCase):
    def test_manifest_v2_is_an_explicit_clean_core_payload(self):
        document, rows = manifest_rows()
        self.assertEqual({"version", "groups"}, set(document))
        self.assertEqual(2, document["version"])
        self.assertEqual({"core"}, set(document["groups"]))
        self.assertEqual(22, len(rows))

        sources = [row["source"] for row in rows]
        destinations = [row["destination"] for row in rows]
        self.assertEqual(len(sources), len(set(sources)))
        self.assertEqual(len(destinations), len(set(destinations)))

        source_skills = {
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in REPOSITORY_ROOT.glob(".agents/skills/*/SKILL.md")
        }
        distributed_skills = {
            source for source in sources if source.startswith(".agents/skills/")
        }
        self.assertEqual(source_skills, distributed_skills)
        self.assertIn(".agents/skills/results-audit/SKILL.md", sources)

        expected_mapping = {source: source for source in sorted(source_skills)}
        expected_mapping.update(
            {
                "AGENTS.md": "AGENTS.md",
                "scripts/validate_agent_workflow.py": (
                    "scripts/validate_agent_workflow.py"
                ),
                ".agents/state/current-task.md": (
                    "distribution/templates/current-task.md"
                ),
                ".agents/state/state.md": "distribution/templates/state.md",
                ".agents/state/backlog.md": "distribution/templates/backlog.md",
                ".agents/state/ideas.md": "distribution/templates/ideas.md",
                "docs/decisions/README.md": (
                    "distribution/templates/docs/decisions/README.md"
                ),
                "docs/research/README.md": (
                    "distribution/templates/docs/research/README.md"
                ),
                "docs/experiments/README.md": (
                    "distribution/templates/docs/experiments/README.md"
                ),
                "docs/audits/README.md": (
                    "distribution/templates/docs/audits/README.md"
                ),
                "docs/tasks/README.md": "distribution/templates/docs/tasks/README.md",
            }
        )
        self.assertEqual(
            expected_mapping,
            {row["destination"]: row["source"] for row in rows},
        )

        state_rows = [
            row for row in rows if row["destination"].startswith(".agents/state/")
        ]
        self.assertEqual(4, len(state_rows))
        self.assertTrue(
            all(
                row["source"].startswith("distribution/templates/")
                for row in state_rows
            )
        )

        prohibited_destinations = {
            "README.md",
            "scripts/install_agent_workflow.py",
        }
        self.assertTrue(prohibited_destinations.isdisjoint(destinations))
        self.assertFalse(
            any(
                destination.startswith((".ara/", "ara/", "tests/", "docs/sessions/"))
                for destination in destinations
            )
        )
        for history_directory in (
            "docs/research/",
            "docs/audits/",
            "docs/tasks/",
        ):
            self.assertEqual(
                [f"{history_directory}README.md"],
                sorted(
                    destination
                    for destination in destinations
                    if destination.startswith(history_directory)
                ),
            )

        for row in rows:
            source = REPOSITORY_ROOT / row["source"]
            self.assertTrue(source.is_file(), row["source"])
            self.assertFalse(source.is_symlink(), row["source"])

    def test_invalid_manifest_forms_are_rejected(self):
        invalid_documents = (
            [],
            {"version": 1, "groups": {"core": []}},
            {"version": 2, "files": []},
            {"version": 2, "groups": {}},
            {"version": 2, "groups": {"extra": []}},
            {"version": 2, "groups": {"core": []}},
            {"version": 2, "groups": {"core": {}, "bad/name": []}},
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = root / "manifest.json"
            for document in invalid_documents:
                with self.subTest(document=document):
                    path.write_text(json.dumps(document), encoding="utf-8")
                    with self.assertRaises(INSTALLER_MODULE.ManifestError):
                        INSTALLER_MODULE.load_manifest(root, path)

    def test_named_group_selection_is_a_stable_union(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for name in ("core.txt", "extra.txt"):
                (root / name).write_text(name, encoding="utf-8")
            document = {
                "version": 2,
                "groups": {
                    "core": [{"source": "core.txt", "destination": "out/core.txt"}],
                    "extra": [{"source": "extra.txt", "destination": "out/extra.txt"}],
                },
            }
            path = root / "manifest.json"
            path.write_text(json.dumps(document), encoding="utf-8")

            manifest = INSTALLER_MODULE.load_manifest(root, path)
            selected = INSTALLER_MODULE.select_payload(
                manifest, ("core", "extra", "core")
            )

            self.assertEqual(
                ["out/core.txt", "out/extra.txt"],
                [entry.destination.as_posix() for entry in selected],
            )
            with self.assertRaisesRegex(
                INSTALLER_MODULE.ManifestError, "unknown payload group"
            ):
                INSTALLER_MODULE.select_payload(manifest, ("core", "missing"))

    def test_slug_validation_has_a_narrow_public_contract(self):
        for valid in ("a", "agent-kit", "a1", "a" * 24):
            with self.subTest(valid=valid):
                self.assertEqual(valid, INSTALLER_MODULE.validate_slug(valid))
        for invalid in (
            "",
            "Agent",
            "1agent",
            "-agent",
            "agent_kit",
            "agent--kit!",
            "a" * 25,
            None,
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    INSTALLER_MODULE.validate_slug(invalid)

    def test_slug_rendering_changes_only_bounded_naming_surfaces(self):
        payload = INSTALLER_MODULE.load_payload()
        plan = INSTALLER_MODULE.render_payload(payload, "acme")
        by_destination = {
            entry.destination.as_posix(): entry.content.decode("utf-8")
            for entry in plan
        }

        for token in INSTALLER_MODULE.SKILL_TOKENS:
            destination = f".agents/skills/acme-{token}/SKILL.md"
            self.assertIn(destination, by_destination)
            self.assertIn(f"name: acme-{token}\n", by_destination[destination])
            self.assertNotIn(f"name: {token}\n", by_destination[destination])

        for content in by_destination.values():
            for span in INSTALLER_MODULE.INLINE_CODE_PATTERN.finditer(content):
                self.assertIsNone(
                    INSTALLER_MODULE.SKILL_TOKEN_PATTERN.search(span.group(1)),
                    span.group(0),
                )

        agents = by_destination["AGENTS.md"]
        self.assertIn("critical implementation.", agents)
        self.assertIn("prepares a handoff.", agents)
        implementation = by_destination[".agents/skills/acme-implementation/SKILL.md"]
        self.assertIn("two real implementations already exist", implementation)
        self.assertIn("interfaces with one implementation", implementation)

    def test_fresh_slugged_install_is_valid_and_preserves_git_metadata(self):
        _, rows = manifest_rows()
        plan = INSTALLER_MODULE.render_payload(INSTALLER_MODULE.load_payload(), "acme")
        expected_destinations = {entry.destination.as_posix() for entry in plan}

        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            run(["git", "init", "-b", "main"], cwd=target, check=True)
            run(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    "https://example.invalid/original.git",
                ],
                cwd=target,
                check=True,
            )
            (target / "project.txt").write_text("target history\n", encoding="utf-8")
            run(["git", "add", "project.txt"], cwd=target, check=True)
            run(
                ["git", "commit", "-m", "target history"],
                cwd=target,
                check=True,
            )
            original_head = run(
                ["git", "rev-parse", "HEAD"], cwd=target, check=True
            ).stdout.strip()
            original_git_head = (target / ".git/HEAD").read_bytes()

            installation = run(install_command(target, "--slug", "acme"))

            self.assertEqual(0, installation.returncode, installation.stdout)
            self.assertIn(
                f"Installed {len(rows)} agent workflow files",
                installation.stdout,
            )
            installed_files = {
                relative
                for relative, value in workspace_snapshot(target).items()
                if value[0] in {"file", "symlink"} and relative != "project.txt"
            }
            self.assertEqual(expected_destinations, installed_files)

            validation = run(
                [sys.executable, "scripts/validate_agent_workflow.py"],
                cwd=target,
            )
            self.assertEqual(0, validation.returncode, validation.stdout)
            self.assertIn("Found 11 skills", validation.stdout)
            self.assertIn("Validated archived tasks: 0.", validation.stdout)

            self.assertEqual(
                original_head,
                run(
                    ["git", "rev-parse", "HEAD"], cwd=target, check=True
                ).stdout.strip(),
            )
            self.assertEqual(
                "main",
                run(
                    ["git", "branch", "--show-current"],
                    cwd=target,
                    check=True,
                ).stdout.strip(),
            )
            self.assertEqual(
                "https://example.invalid/original.git",
                run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=target,
                    check=True,
                ).stdout.strip(),
            )
            self.assertEqual(original_git_head, (target / ".git/HEAD").read_bytes())

    def test_explicit_no_prefix_preserves_payload_bytes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()

            installation = run(install_command(target, "--no-prefix"))

            self.assertEqual(0, installation.returncode, installation.stdout)
            for entry in INSTALLER_MODULE.load_payload():
                self.assertEqual(
                    entry.source.read_bytes(),
                    (target / entry.destination).read_bytes(),
                )

    def test_all_exact_collisions_are_reported_before_any_write(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            (target / "AGENTS.md").write_text("target rules\n", encoding="utf-8")
            scripts = target / "scripts"
            scripts.mkdir()
            (scripts / "validate_agent_workflow.py").write_text(
                "target validator\n", encoding="utf-8"
            )
            state = target / ".agents/state"
            state.mkdir(parents=True)
            (state / "current-task.md").symlink_to("missing-task.md")
            before = workspace_snapshot(target)

            installation = run(install_command(target, "--slug", "acme"))

            self.assertEqual(1, installation.returncode, installation.stdout)
            self.assertIn("  - .agents/state/current-task.md", installation.stdout)
            self.assertIn("  - AGENTS.md", installation.stdout)
            self.assertIn(
                "  - scripts/validate_agent_workflow.py",
                installation.stdout,
            )
            self.assertEqual(before, workspace_snapshot(target))
            self.assertFalse((target / ".agents/skills").exists())

    def test_all_blocking_ancestors_are_reported_before_any_write(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            (target / ".agents").write_text(
                "blocks the workflow tree\n", encoding="utf-8"
            )
            (target / "docs").symlink_to("missing-docs")
            before = workspace_snapshot(target)

            installation = run(install_command(target, "--no-prefix"))

            self.assertEqual(1, installation.returncode, installation.stdout)
            self.assertIn("  - .agents", installation.stdout)
            self.assertIn("  - docs", installation.stdout)
            self.assertEqual(before, workspace_snapshot(target))
            self.assertFalse((target / "AGENTS.md").exists())

    def test_nonexistent_target_is_not_created(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "missing"

            installation = run(install_command(target, "--no-prefix"))

            self.assertEqual(2, installation.returncode, installation.stdout)
            self.assertIn("Target must be an existing directory", installation.stdout)
            self.assertFalse(target.exists())

    def test_old_positional_cli_is_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            before = workspace_snapshot(target)

            installation = run([sys.executable, str(INSTALLER), str(target)])

            self.assertEqual(2, installation.returncode, installation.stdout)
            self.assertIn("invalid choice", installation.stdout)
            self.assertEqual(before, workspace_snapshot(target))

    def test_copy_failure_rolls_back_only_installer_created_paths(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_one = root / "source-one"
            source_two = root / "source-two"
            source_one.write_text("first payload\n", encoding="utf-8")
            source_two.write_text("second payload\n", encoding="utf-8")
            target = root / "target"
            target.mkdir()
            (target / "keep.txt").write_text("target content\n", encoding="utf-8")
            before = workspace_snapshot(target)
            payload = (
                INSTALLER_MODULE.PlannedFile(
                    source=source_one,
                    destination=Path("first.txt"),
                    content=source_one.read_bytes(),
                ),
                INSTALLER_MODULE.PlannedFile(
                    source=source_two,
                    destination=Path("nested/second.txt"),
                    content=source_two.read_bytes(),
                ),
            )
            real_copy = INSTALLER_MODULE.shutil.copyfileobj
            call_count = 0

            def fail_during_second_copy(source_stream, destination_stream):
                nonlocal call_count
                call_count += 1
                if call_count == 2:
                    destination_stream.write(b"partial")
                    raise OSError("injected copy failure")
                real_copy(source_stream, destination_stream)

            with mock.patch.object(
                INSTALLER_MODULE.shutil,
                "copyfileobj",
                side_effect=fail_during_second_copy,
            ):
                with self.assertRaisesRegex(OSError, "injected copy failure"):
                    INSTALLER_MODULE.install_payload(target, payload)

            self.assertEqual(before, workspace_snapshot(target))


if __name__ == "__main__":
    unittest.main()
