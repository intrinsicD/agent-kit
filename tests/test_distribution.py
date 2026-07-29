#!/usr/bin/env python3
"""Regression tests for the versioned, non-overwriting distribution payload."""

import importlib.util
import hashlib
import io
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


def doctor_command(target):
    return [sys.executable, str(INSTALLER), "doctor", str(target)]


SLUGGED_DRY_RUN_PLAN = """\
Write plan (23 files):
  - immutable: AGENTS.md
  - immutable: .agents/skills/acme-code-audit/SKILL.md
  - immutable: .agents/skills/acme-experiment-design/SKILL.md
  - immutable: .agents/skills/acme-handoff/SKILL.md
  - immutable: .agents/skills/acme-implementation/SKILL.md
  - immutable: .agents/skills/acme-novel-idea-generation/SKILL.md
  - immutable: .agents/skills/acme-productization/SKILL.md
  - immutable: .agents/skills/acme-repo-organization/SKILL.md
  - immutable: .agents/skills/acme-research-methods/SKILL.md
  - immutable: .agents/skills/acme-results-audit/SKILL.md
  - immutable: .agents/skills/acme-review-and-falsification/SKILL.md
  - immutable: .agents/skills/acme-task-orchestration/SKILL.md
  - immutable: scripts/validate_agent_workflow.py
  - user-template: .agents/state/current-task.md
  - user-template: .agents/state/state.md
  - user-template: .agents/state/backlog.md
  - user-template: .agents/state/ideas.md
  - user-template: docs/decisions/README.md
  - user-template: docs/research/README.md
  - user-template: docs/experiments/README.md
  - user-template: docs/audits/README.md
  - user-template: docs/tasks/README.md
  - receipt: .agents/kit-install.json
Collision report:
  - none
"""


class DistributionBoundaryTests(unittest.TestCase):
    def test_manifest_v2_is_an_explicit_clean_core_payload(self):
        document, rows = manifest_rows()
        self.assertEqual({"version", "groups"}, set(document))
        self.assertEqual(2, document["version"])
        self.assertEqual({"core", "verify"}, set(document["groups"]))
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

    def test_verify_group_is_an_explicit_six_file_payload(self):
        document, core_rows = manifest_rows()
        rows = document["groups"]["verify"]

        self.assertEqual(22, len(core_rows))
        self.assertEqual(6, len(rows))
        self.assertEqual(
            {
                "scripts/check_authority.py": "scripts/check_authority.py",
                "scripts/check_doc_links.py": "scripts/check_doc_links.py",
                "scripts/check_docs_sync.py": "scripts/check_docs_sync.py",
                "docs-sync-rules.toml": ("distribution/templates/docs-sync-rules.toml"),
                "scripts/verify.sh": ("distribution/templates/scripts/verify.sh"),
                ".github/workflows/agent-workflow.yml": (
                    "distribution/templates/.github/workflows/agent-workflow.yml"
                ),
            },
            {row["destination"]: row["source"] for row in rows},
        )
        for row in rows:
            source = REPOSITORY_ROOT / row["source"]
            self.assertTrue(source.is_file(), row["source"])
            self.assertFalse(source.is_symlink(), row["source"])

    def test_core_plus_verify_install_passes_its_distributed_gate(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            run(["git", "init", "-b", "main"], cwd=target, check=True)

            installation = run(
                install_command(
                    target,
                    "--slug",
                    "acme",
                    "--profile",
                    "verify",
                )
            )

            self.assertEqual(0, installation.returncode, installation.stdout)
            verification = run(["./scripts/verify.sh"], cwd=target)
            self.assertEqual(0, verification.returncode, verification.stdout)
            self.assertIn("[1/4] Workflow structure", verification.stdout)
            self.assertIn("check_authority: OK (11 skills)", verification.stdout)
            self.assertIn("check_doc_links: OK", verification.stdout)
            self.assertIn("check_docs_sync: OK (0 rules)", verification.stdout)

            receipt = json.loads(
                (target / ".agents/kit-install.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                ["core", "verify"],
                receipt["config"]["groups"],
            )
            self.assertEqual(16, len(receipt["immutable_files"]))
            self.assertEqual(12, len(receipt["user_owned_templates"]))
            self.assertIn(
                "scripts/check_authority.py",
                receipt["immutable_files"],
            )
            self.assertIn(
                "scripts/verify.sh",
                receipt["user_owned_templates"],
            )
            self.assertTrue((target / "scripts/verify.sh").stat().st_mode & 0o100)

            doctor = run(doctor_command(target))
            self.assertEqual(0, doctor.returncode, doctor.stdout)
            self.assertIn(
                "Summary: 16 OK, 0 MODIFIED, 0 MISSING",
                doctor.stdout,
            )

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

    def test_manifest_rejects_unsafe_rows_and_cross_group_duplicates(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "one.txt").write_text("one\n", encoding="utf-8")
            (root / "two.txt").write_text("two\n", encoding="utf-8")
            path = root / "manifest.json"
            invalid_groups = (
                {"core": [{"source": "one.txt", "destination": ".git/config"}]},
                {
                    "core": [
                        {
                            "source": "one.txt",
                            "destination": ".agents/kit-install.json",
                        }
                    ]
                },
                {
                    "core": [{"source": "one.txt", "destination": "shared.txt"}],
                    "extra": [{"source": "two.txt", "destination": "shared.txt"}],
                },
                {
                    "core": [{"source": "one.txt", "destination": "one.txt"}],
                    "extra": [{"source": "one.txt", "destination": "two.txt"}],
                },
                {
                    "core": [
                        {
                            "source": "../one.txt",
                            "destination": "unsafe.txt",
                        }
                    ]
                },
            )
            for groups in invalid_groups:
                with self.subTest(groups=groups):
                    path.write_text(
                        json.dumps({"version": 2, "groups": groups}),
                        encoding="utf-8",
                    )
                    with self.assertRaises(INSTALLER_MODULE.ManifestError):
                        INSTALLER_MODULE.load_manifest(root, path)

    def test_manifest_rejects_raw_and_receipt_destination_hierarchies(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "one.txt").write_text("one\n", encoding="utf-8")
            (root / "two.txt").write_text("two\n", encoding="utf-8")
            path = root / "manifest.json"
            invalid_rows = (
                [
                    {"source": "one.txt", "destination": "node"},
                    {"source": "two.txt", "destination": "node/child.txt"},
                ],
                [{"source": "one.txt", "destination": ".agents"}],
                [
                    {
                        "source": "one.txt",
                        "destination": ".agents/kit-install.json/child.txt",
                    }
                ],
            )
            for rows in invalid_rows:
                with self.subTest(rows=rows):
                    path.write_text(
                        json.dumps({"version": 2, "groups": {"core": rows}}),
                        encoding="utf-8",
                    )
                    with self.assertRaisesRegex(
                        INSTALLER_MODULE.ManifestError,
                        "destination hierarchy conflict",
                    ):
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

    def test_inline_rewrite_uses_unicode_word_boundaries_and_is_idempotent(self):
        source = (
            "`implementation` `/implementation/` `(implementation)` "
            "`Ximplementation` `implementationX` `implementation_detail` "
            "`préimplementation` `implementationé` `acme-implementation`"
        )
        expected = (
            "`acme-implementation` `/acme-implementation/` "
            "`(acme-implementation)` `Ximplementation` `implementationX` "
            "`implementation_detail` `préimplementation` `implementationé` "
            "`acme-implementation`"
        )

        rendered = INSTALLER_MODULE._rewrite_inline_skill_names(source, "acme-")

        self.assertEqual(expected, rendered)
        self.assertEqual(
            expected,
            INSTALLER_MODULE._rewrite_inline_skill_names(rendered, "acme-"),
        )

    def test_rendered_and_receipt_hierarchy_conflicts_are_configuration_errors(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_source = root / "skill.md"
            skill_source.write_text(
                "---\nname: implementation\n---\n\nUse `implementation`.\n",
                encoding="utf-8",
            )
            blocker_source = root / "blocker.txt"
            blocker_source.write_text("blocker\n", encoding="utf-8")
            manifest_path = root / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": 2,
                        "groups": {
                            "core": [
                                {
                                    "source": "skill.md",
                                    "destination": (
                                        ".agents/skills/implementation/SKILL.md"
                                    ),
                                },
                                {
                                    "source": "blocker.txt",
                                    "destination": (
                                        ".agents/skills/acme-implementation"
                                    ),
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            slug_manifest = INSTALLER_MODULE.load_manifest(root, manifest_path)
            receipt_manifest = INSTALLER_MODULE.DistributionManifest(
                version=2,
                sha256="0" * 64,
                groups={
                    "core": (
                        INSTALLER_MODULE.PayloadFile(
                            source=blocker_source,
                            destination=Path(".agents"),
                        ),
                    )
                },
            )

            for label, manifest, slug in (
                ("slug-rendered", slug_manifest, "acme"),
                ("generated-receipt", receipt_manifest, None),
            ):
                with self.subTest(label=label, interface="plan"):
                    with self.assertRaisesRegex(
                        INSTALLER_MODULE.ManifestError,
                        "destination hierarchy conflict",
                    ):
                        INSTALLER_MODULE.build_install_plan(manifest, slug=slug)

                for dry_run in (False, True):
                    with self.subTest(
                        label=label,
                        interface="dry-run" if dry_run else "install",
                    ):
                        target = root / f"target-{label}-{dry_run}"
                        target.mkdir()
                        before = workspace_snapshot(target)
                        arguments = INSTALLER_MODULE.argparse.Namespace(
                            target=target,
                            slug=slug,
                            no_prefix=slug is None,
                            profile=[],
                            dry_run=dry_run,
                        )
                        with (
                            mock.patch.object(
                                INSTALLER_MODULE,
                                "load_manifest",
                                return_value=manifest,
                            ),
                            mock.patch.object(
                                INSTALLER_MODULE.sys,
                                "stderr",
                                new=io.StringIO(),
                            ) as stderr,
                        ):
                            result = INSTALLER_MODULE._run_install(arguments)

                        self.assertEqual(2, result)
                        self.assertIn(
                            "destination hierarchy conflict", stderr.getvalue()
                        )
                        self.assertEqual(before, workspace_snapshot(target))

    def test_fresh_slugged_install_is_valid_and_preserves_git_metadata(self):
        _, rows = manifest_rows()
        plan = INSTALLER_MODULE.build_install_plan(
            INSTALLER_MODULE.load_manifest(), slug="acme"
        )
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
                f"Installed {len(rows)} agent workflow payload files and receipt",
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

            before_doctor = workspace_snapshot(target)
            doctor = run(doctor_command(target))
            self.assertEqual(0, doctor.returncode, doctor.stdout)
            self.assertIn("Summary: 13 OK, 0 MODIFIED, 0 MISSING", doctor.stdout)
            self.assertEqual(before_doctor, workspace_snapshot(target))

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
            receipt = json.loads(
                (target / ".agents/kit-install.json").read_text(encoding="utf-8")
            )
            self.assertIsNone(receipt["config"]["slug"])
            self.assertEqual("", receipt["config"]["prefix"])

    def test_clean_dry_run_has_a_stable_full_snapshot_and_no_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            (target / "keep.txt").write_text("keep\n", encoding="utf-8")
            before = workspace_snapshot(target)

            dry_run = run(install_command(target, "--slug", "acme", "--dry-run"))

            self.assertEqual(0, dry_run.returncode, dry_run.stdout)
            self.assertEqual(SLUGGED_DRY_RUN_PLAN, dry_run.stdout)
            self.assertEqual(before, workspace_snapshot(target))

    def test_colliding_dry_run_reports_receipt_and_payload_without_writes(self):
        expected = SLUGGED_DRY_RUN_PLAN.replace(
            "Collision report:\n  - none\n",
            "Collision report:\n  - .agents/kit-install.json\n  - AGENTS.md\n",
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            (target / "AGENTS.md").write_text("keep rules\n", encoding="utf-8")
            agents = target / ".agents"
            agents.mkdir()
            (agents / "kit-install.json").write_text("keep receipt\n", encoding="utf-8")
            before = workspace_snapshot(target)

            dry_run = run(install_command(target, "--slug", "acme", "--dry-run"))

            self.assertEqual(1, dry_run.returncode, dry_run.stdout)
            self.assertEqual(expected, dry_run.stdout)
            self.assertEqual(before, workspace_snapshot(target))

    def test_receipt_records_provenance_configuration_and_ownership(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()

            installation = run(install_command(target, "--slug", "acme"))

            self.assertEqual(0, installation.returncode, installation.stdout)
            receipt = json.loads(
                (target / ".agents/kit-install.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                {
                    "receipt_version",
                    "manifest",
                    "config",
                    "installed_at",
                    "immutable_files",
                    "user_owned_templates",
                },
                set(receipt),
            )
            self.assertEqual(1, receipt["receipt_version"])
            self.assertEqual(
                {
                    "version": 2,
                    "sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
                },
                receipt["manifest"],
            )
            self.assertEqual(
                {"slug": "acme", "prefix": "acme-", "groups": ["core"]},
                receipt["config"],
            )
            self.assertRegex(
                receipt["installed_at"],
                r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$",
            )
            self.assertEqual(13, len(receipt["immutable_files"]))
            self.assertEqual(9, len(receipt["user_owned_templates"]))
            self.assertNotIn(
                ".agents/state/current-task.md", receipt["immutable_files"]
            )
            self.assertIn(
                ".agents/state/current-task.md",
                receipt["user_owned_templates"],
            )
            for relative, expected_digest in receipt["immutable_files"].items():
                self.assertEqual(
                    expected_digest,
                    hashlib.sha256((target / relative).read_bytes()).hexdigest(),
                    relative,
                )

    def test_receipt_collision_refuses_before_any_payload_write(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            receipt = target / ".agents/kit-install.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("owned by target\n", encoding="utf-8")
            before = workspace_snapshot(target)

            installation = run(install_command(target, "--no-prefix"))

            self.assertEqual(1, installation.returncode, installation.stdout)
            self.assertIn("  - .agents/kit-install.json", installation.stdout)
            self.assertEqual(before, workspace_snapshot(target))
            self.assertFalse((target / "AGENTS.md").exists())

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

    def test_doctor_reports_modified_and_missing_immutable_files_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            installation = run(install_command(target, "--slug", "acme"))
            self.assertEqual(0, installation.returncode, installation.stdout)
            (target / "AGENTS.md").write_text("locally changed\n", encoding="utf-8")
            (target / "scripts/validate_agent_workflow.py").unlink()
            before = workspace_snapshot(target)

            doctor = run(doctor_command(target))

            self.assertEqual(1, doctor.returncode, doctor.stdout)
            self.assertIn("  MODIFIED AGENTS.md", doctor.stdout)
            self.assertIn("  MISSING scripts/validate_agent_workflow.py", doctor.stdout)
            self.assertIn("1 MODIFIED, 1 MISSING", doctor.stdout)
            self.assertEqual(before, workspace_snapshot(target))

    def test_doctor_does_not_trust_immutable_files_through_symlinked_ancestors(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "target"
            target.mkdir()
            installation = run(install_command(target, "--no-prefix"))
            self.assertEqual(0, installation.returncode, installation.stdout)

            external_scripts = root / "external-scripts"
            external_scripts.mkdir()
            validator = target / "scripts/validate_agent_workflow.py"
            (external_scripts / "validate_agent_workflow.py").write_bytes(
                validator.read_bytes()
            )
            validator.unlink()
            validator.parent.rmdir()
            validator.parent.symlink_to(external_scripts, target_is_directory=True)
            before = workspace_snapshot(target)

            doctor = run(doctor_command(target))

            self.assertEqual(1, doctor.returncode, doctor.stdout)
            self.assertIn(
                "  MODIFIED scripts/validate_agent_workflow.py", doctor.stdout
            )
            self.assertEqual(before, workspace_snapshot(target))

    def test_doctor_treats_templates_as_presence_only(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            installation = run(install_command(target, "--no-prefix"))
            self.assertEqual(0, installation.returncode, installation.stdout)
            task = target / ".agents/state/current-task.md"
            task.write_text("user-owned content\n", encoding="utf-8")
            before_modified_check = workspace_snapshot(target)

            modified_check = run(doctor_command(target))

            self.assertEqual(0, modified_check.returncode, modified_check.stdout)
            self.assertIn(
                "  PRESENT .agents/state/current-task.md", modified_check.stdout
            )
            self.assertEqual(before_modified_check, workspace_snapshot(target))

            missing_template = target / "docs/tasks/README.md"
            missing_template.unlink()
            before_missing_check = workspace_snapshot(target)
            missing_check = run(doctor_command(target))
            self.assertEqual(1, missing_check.returncode, missing_check.stdout)
            self.assertIn("  MISSING docs/tasks/README.md", missing_check.stdout)
            self.assertEqual(before_missing_check, workspace_snapshot(target))

    def test_doctor_requires_template_destinations_to_resolve_to_files(self):
        for replacement in ("directory", "dangling-symlink"):
            with self.subTest(replacement=replacement):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    target = Path(temporary_directory) / "target"
                    target.mkdir()
                    installation = run(install_command(target, "--no-prefix"))
                    self.assertEqual(0, installation.returncode, installation.stdout)
                    task = target / ".agents/state/current-task.md"
                    task.unlink()
                    if replacement == "directory":
                        task.mkdir()
                    else:
                        task.symlink_to("missing-task.md")
                    before = workspace_snapshot(target)

                    doctor = run(doctor_command(target))

                    self.assertEqual(1, doctor.returncode, doctor.stdout)
                    self.assertIn(
                        "  MISSING .agents/state/current-task.md",
                        doctor.stdout,
                    )
                    self.assertIn(
                        "8 templates PRESENT, 1 templates MISSING",
                        doctor.stdout,
                    )
                    self.assertEqual(before, workspace_snapshot(target))

    def test_doctor_missing_receipt_uses_unknown_presence_fallback_without_writes(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            installation = run(install_command(target, "--slug", "acme"))
            self.assertEqual(0, installation.returncode, installation.stdout)
            (target / ".agents/kit-install.json").unlink()
            before = workspace_snapshot(target)

            doctor = run(doctor_command(target))

            self.assertEqual(1, doctor.returncode, doctor.stdout)
            self.assertIn(
                "Receipt: MISSING (install configuration unknown)", doctor.stdout
            )
            self.assertIn("Fallback core presence checks:", doctor.stdout)
            self.assertIn(
                "  PRESENT .agents/skills/acme-code-audit/SKILL.md "
                "(for .agents/skills/code-audit/SKILL.md)",
                doctor.stdout,
            )
            self.assertIn("integrity and selected profiles are unknown", doctor.stdout)
            self.assertEqual(before, workspace_snapshot(target))

    def test_doctor_rejects_malformed_receipt_as_schema_error_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            receipt = target / ".agents/kit-install.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("{}\n", encoding="utf-8")
            before = workspace_snapshot(target)

            doctor = run(doctor_command(target))

            self.assertEqual(2, doctor.returncode, doctor.stdout)
            self.assertIn("receipt must contain", doctor.stdout)
            self.assertEqual(before, workspace_snapshot(target))

    def test_nonexistent_target_is_not_created(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "missing"

            installation = run(install_command(target, "--no-prefix"))

            self.assertEqual(2, installation.returncode, installation.stdout)
            self.assertIn("Target must be an existing directory", installation.stdout)
            self.assertFalse(target.exists())

            doctor = run(doctor_command(target))
            self.assertEqual(2, doctor.returncode, doctor.stdout)
            self.assertIn("Target must be an existing directory", doctor.stdout)
            self.assertFalse(target.exists())

    def test_install_cli_rejects_missing_conflicting_and_invalid_naming_modes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            for options in (
                (),
                ("--slug", "Agent"),
                ("--slug", "acme", "--no-prefix"),
                ("--no-prefix", "--profile", "missing"),
            ):
                with self.subTest(options=options):
                    before = workspace_snapshot(target)
                    installation = run(install_command(target, *options))
                    self.assertEqual(2, installation.returncode, installation.stdout)
                    self.assertEqual(before, workspace_snapshot(target))

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

    def test_receipt_write_failure_rolls_back_the_entire_install_plan(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory) / "target"
            target.mkdir()
            (target / "keep.txt").write_text("target content\n", encoding="utf-8")
            before = workspace_snapshot(target)
            plan = INSTALLER_MODULE.build_install_plan(
                INSTALLER_MODULE.load_manifest(),
                slug="acme",
                installed_at="2026-01-02T03:04:05Z",
            )
            real_copy = INSTALLER_MODULE.shutil.copyfileobj

            def fail_during_receipt_write(source_stream, destination_stream):
                if str(destination_stream.name).endswith(".agents/kit-install.json"):
                    destination_stream.write(b"partial receipt")
                    raise OSError("injected receipt failure")
                real_copy(source_stream, destination_stream)

            with mock.patch.object(
                INSTALLER_MODULE.shutil,
                "copyfileobj",
                side_effect=fail_during_receipt_write,
            ):
                with self.assertRaisesRegex(OSError, "injected receipt failure"):
                    INSTALLER_MODULE.install_payload(target, plan)

            self.assertEqual(before, workspace_snapshot(target))


if __name__ == "__main__":
    unittest.main()
