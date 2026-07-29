#!/usr/bin/env python3
"""Regression tests for the generic, distributable validator pack."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_CHECKER = REPOSITORY_ROOT / "scripts/check_authority.py"
DOC_LINK_CHECKER = REPOSITORY_ROOT / "scripts/check_doc_links.py"
DOCS_SYNC_CHECKER = REPOSITORY_ROOT / "scripts/check_docs_sync.py"
GIT_ENVIRONMENT = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Validator Test",
    "GIT_AUTHOR_EMAIL": "validator@example.invalid",
    "GIT_COMMITTER_NAME": "Validator Test",
    "GIT_COMMITTER_EMAIL": "validator@example.invalid",
}


def run(arguments, cwd=None):
    return subprocess.run(
        arguments,
        cwd=cwd,
        env=GIT_ENVIRONMENT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def checker_command(checker, root, *options):
    return [sys.executable, str(checker), "--root", str(root), *options]


def make_authority_tree(root):
    (root / "AGENTS.md").write_text("# Repository authority\n", encoding="utf-8")
    skill = root / ".agents/skills/implementation/SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        "---\nname: implementation\ndescription: Implement a bounded change.\n---\n",
        encoding="utf-8",
    )


class AuthorityCheckerTests(unittest.TestCase):
    def test_live_repository_passes_strict_authority_check(self):
        result = run(checker_command(AUTHORITY_CHECKER, REPOSITORY_ROOT, "--strict"))

        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("check_authority: OK", result.stdout)

    def test_alias_symlinks_and_explicit_redirect_marker_are_accepted(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            make_authority_tree(root)
            (root / "CLAUDE.md").symlink_to("AGENTS.md")
            claude = root / ".claude"
            claude.mkdir()
            (claude / "skills").symlink_to("../.agents/skills")

            symlink_result = run(checker_command(AUTHORITY_CHECKER, root, "--strict"))

            self.assertEqual(0, symlink_result.returncode, symlink_result.stdout)

            (root / "CLAUDE.md").unlink()
            (root / "CLAUDE.md").write_text(
                "<!-- agent-kit: authority=AGENTS.md -->\n"
                "Follow the repository contract above.\n",
                encoding="utf-8",
            )
            marker_result = run(checker_command(AUTHORITY_CHECKER, root, "--strict"))
            self.assertEqual(0, marker_result.returncode, marker_result.stdout)

    def test_findings_warn_by_default_and_fail_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            make_authority_tree(root)
            (root / "CLAUDE.md").write_text(
                "# Independent and drifting policy\n",
                encoding="utf-8",
            )

            warning = run(checker_command(AUTHORITY_CHECKER, root))
            strict = run(checker_command(AUTHORITY_CHECKER, root, "--strict"))

            self.assertEqual(0, warning.returncode, warning.stdout)
            self.assertIn("check_authority: WARNING", warning.stdout)
            self.assertIn("CLAUDE.md", warning.stdout)
            self.assertEqual(1, strict.returncode, strict.stdout)
            self.assertIn("check_authority: ERROR", strict.stdout)

    def test_dual_physical_roots_name_drift_and_codex_drift_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            make_authority_tree(root)
            second_skill = root / ".claude/skills/review/SKILL.md"
            second_skill.parent.mkdir(parents=True)
            second_skill.write_text(
                "---\nname: other-name\n---\n",
                encoding="utf-8",
            )
            codex_config = root / ".codex/config.yaml"
            codex_config.parent.mkdir()
            codex_config.write_text("model: example\n", encoding="utf-8")

            result = run(checker_command(AUTHORITY_CHECKER, root, "--strict"))

            self.assertEqual(1, result.returncode, result.stdout)
            self.assertIn("physical skills root", result.stdout)
            self.assertIn("frontmatter name", result.stdout)
            self.assertIn(".codex/config.yaml", result.stdout)

    def test_codex_contract_reference_must_not_exist_only_in_a_comment(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            make_authority_tree(root)
            config = root / ".codex/config.yaml"
            config.parent.mkdir()
            config.write_text(
                "# Contract: AGENTS.md\nmodel: example\n",
                encoding="utf-8",
            )

            comment_only = run(checker_command(AUTHORITY_CHECKER, root, "--strict"))
            self.assertEqual(1, comment_only.returncode, comment_only.stdout)
            self.assertIn(".codex/config.yaml", comment_only.stdout)

            config.write_text(
                "instructions: AGENTS.md # canonical contract\n",
                encoding="utf-8",
            )
            visible_reference = run(
                checker_command(AUTHORITY_CHECKER, root, "--strict")
            )
            self.assertEqual(
                0,
                visible_reference.returncode,
                visible_reference.stdout,
            )

    def test_invalid_root_is_an_environment_error(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing = Path(temporary_directory) / "missing"

            result = run(checker_command(AUTHORITY_CHECKER, missing, "--strict"))

            self.assertEqual(2, result.returncode, result.stdout)


class DocumentLinkCheckerTests(unittest.TestCase):
    def test_live_repository_passes_strict_document_link_check(self):
        result = run(checker_command(DOC_LINK_CHECKER, REPOSITORY_ROOT, "--strict"))

        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("check_doc_links: OK", result.stdout)

    def test_relative_root_external_anchor_and_fenced_links_are_handled(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "AGENTS.md").write_text(
                "[guide](docs/guide.md)\n"
                "[readme](/README.md)\n"
                "[external](https://example.invalid/missing)\n"
                "[anchor](#local)\n"
                "`[inline-example](missing-inline.md)`\n"
                "```\n[example](missing-in-fence.md)\n```\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text("# Read me\n", encoding="utf-8")
            guide = root / "docs/guide.md"
            guide.parent.mkdir()
            guide.write_text(
                '[state](../.agents/state/state.md "state")\n'
                "[parentheses](guide(with-parens).md)\n",
                encoding="utf-8",
            )
            (root / "docs/guide(with-parens).md").write_text(
                "# Parenthesized path\n",
                encoding="utf-8",
            )
            state = root / ".agents/state/state.md"
            state.parent.mkdir(parents=True)
            state.write_text("# State\n", encoding="utf-8")
            skill = root / ".agents/skills/example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("[guide](../../../docs/guide.md)\n", encoding="utf-8")

            result = run(checker_command(DOC_LINK_CHECKER, root, "--strict"))

            self.assertEqual(0, result.returncode, result.stdout)
            self.assertIn("6 Markdown files", result.stdout)

    def test_missing_and_escaping_links_warn_or_fail(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "AGENTS.md").write_text(
                "[missing](docs/missing.md)\n",
                encoding="utf-8",
            )
            broken = root / "docs/broken.md"
            broken.parent.mkdir()
            broken.write_text("[escape](../../outside.md)\n", encoding="utf-8")

            warning = run(checker_command(DOC_LINK_CHECKER, root))
            strict = run(checker_command(DOC_LINK_CHECKER, root, "--strict"))

            self.assertEqual(0, warning.returncode, warning.stdout)
            self.assertIn("check_doc_links: WARNING", warning.stdout)
            self.assertEqual(1, strict.returncode, strict.stdout)
            self.assertIn("does not exist", strict.stdout)
            self.assertIn("escapes repository root", strict.stdout)

    def test_present_scan_root_must_resolve_inside_repository(self):
        for populated in (False, True):
            with self.subTest(populated=populated):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    workspace = Path(temporary_directory)
                    root = workspace / "repository"
                    root.mkdir()
                    (root / "AGENTS.md").write_text(
                        "# Authority\n",
                        encoding="utf-8",
                    )
                    external = workspace / "external-docs"
                    external.mkdir()
                    if populated:
                        (external / "guide.md").write_text(
                            "# External\n",
                            encoding="utf-8",
                        )
                    (root / "docs").symlink_to(
                        external,
                        target_is_directory=True,
                    )

                    result = run(checker_command(DOC_LINK_CHECKER, root, "--strict"))

                    self.assertEqual(1, result.returncode, result.stdout)
                    self.assertIn(
                        "Markdown scan root escapes repository root: docs",
                        result.stdout,
                    )

    def test_balanced_and_escaped_brackets_in_link_text_are_scanned(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "AGENTS.md").write_text(
                "[outer [inner]](missing-nested.md)\n"
                r"[outer \[inner\]](missing-escaped.md)" + "\n",
                encoding="utf-8",
            )

            missing = run(checker_command(DOC_LINK_CHECKER, root, "--strict"))

            self.assertEqual(1, missing.returncode, missing.stdout)
            self.assertIn("missing-nested.md", missing.stdout)
            self.assertIn("missing-escaped.md", missing.stdout)

            (root / "missing-nested.md").write_text(
                "# Nested\n",
                encoding="utf-8",
            )
            (root / "missing-escaped.md").write_text(
                "# Escaped\n",
                encoding="utf-8",
            )
            existing = run(checker_command(DOC_LINK_CHECKER, root, "--strict"))
            self.assertEqual(0, existing.returncode, existing.stdout)


class DocumentationSyncCheckerTests(unittest.TestCase):
    def write_rule(self, root):
        (root / "docs-sync-rules.toml").write_text(
            "[[rule]]\n"
            'trigger = ["src/**"]\n'
            'one_of = ["docs/**", "README.md"]\n'
            'reason = "Public behavior must be documented."\n',
            encoding="utf-8",
        )

    def test_empty_rules_need_no_git_or_changed_file_source(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs-sync-rules.toml").write_text(
                "# Add repository-specific [[rule]] entries here.\n",
                encoding="utf-8",
            )

            result = run(checker_command(DOCS_SYNC_CHECKER, root, "--strict"))

            self.assertEqual(0, result.returncode, result.stdout)
            self.assertIn("check_docs_sync: OK (0 rules)", result.stdout)

    def test_explicit_files_trigger_warn_fail_and_satisfy_rules(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_rule(root)

            warning = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--files",
                    "src/api.py",
                )
            )
            strict = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--strict",
                    "--files",
                    "src/api.py",
                )
            )
            satisfied = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--strict",
                    "--files",
                    "src/api.py",
                    "docs/api.md",
                )
            )

            self.assertEqual(0, warning.returncode, warning.stdout)
            self.assertIn("check_docs_sync: WARNING", warning.stdout)
            self.assertIn("Public behavior must be documented.", warning.stdout)
            self.assertEqual(1, strict.returncode, strict.stdout)
            self.assertEqual(0, satisfied.returncode, satisfied.stdout)

    def test_globs_support_recursive_components_and_character_classes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs-sync-rules.toml").write_text(
                "[[rule]]\n"
                'trigger = ["src/**/*.py"]\n'
                'one_of = ["docs/[ab].md"]\n'
                'reason = "Python changes need bounded documentation."\n',
                encoding="utf-8",
            )

            immediate = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--strict",
                    "--files",
                    "src/api.py",
                    "docs/a.md",
                )
            )
            nested = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--strict",
                    "--files",
                    "src/nested/api.py",
                )
            )

            self.assertEqual(0, immediate.returncode, immediate.stdout)
            self.assertEqual(1, nested.returncode, nested.stdout)

    def test_git_base_uses_merge_base_for_the_complete_change(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            run(["git", "init", "-b", "main"], cwd=root)
            self.write_rule(root)
            source = root / "src/api.py"
            source.parent.mkdir()
            source.write_text("before\n", encoding="utf-8")
            documentation = root / "docs/api.md"
            documentation.parent.mkdir()
            documentation.write_text("before\n", encoding="utf-8")
            run(["git", "add", "."], cwd=root)
            run(["git", "commit", "-m", "baseline"], cwd=root)
            run(["git", "tag", "baseline"], cwd=root)

            source.write_text("after\n", encoding="utf-8")
            run(["git", "add", "src/api.py"], cwd=root)
            run(["git", "commit", "-m", "change source"], cwd=root)
            missing = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--strict",
                    "--base",
                    "baseline",
                )
            )
            self.assertEqual(1, missing.returncode, missing.stdout)

            documentation.write_text("after\n", encoding="utf-8")
            run(["git", "add", "docs/api.md"], cwd=root)
            run(["git", "commit", "-m", "update docs"], cwd=root)
            satisfied = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--strict",
                    "--base",
                    "baseline",
                )
            )
            self.assertEqual(0, satisfied.returncode, satisfied.stdout)

    def test_missing_change_source_degrades_only_outside_strict_mode(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_rule(root)

            warning = run(checker_command(DOCS_SYNC_CHECKER, root))
            strict = run(checker_command(DOCS_SYNC_CHECKER, root, "--strict"))

            self.assertEqual(0, warning.returncode, warning.stdout)
            self.assertIn("check_docs_sync: SKIPPED", warning.stdout)
            self.assertEqual(2, strict.returncode, strict.stdout)

    def test_unsafe_changed_path_and_option_like_base_are_configuration_errors(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs-sync-rules.toml").write_text(
                "# Empty policy still validates explicit inputs.\n",
                encoding="utf-8",
            )

            unsafe_path = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--files",
                    "../outside.py",
                )
            )
            option_base = run(
                checker_command(
                    DOCS_SYNC_CHECKER,
                    root,
                    "--base=-arbitrary-option",
                )
            )

            self.assertEqual(2, unsafe_path.returncode, unsafe_path.stdout)
            self.assertEqual(2, option_base.returncode, option_base.stdout)

    def test_malformed_globs_are_configuration_errors_before_diff_evaluation(self):
        for pattern in ("[z-a]", "[!]", "[unterminated"):
            with self.subTest(pattern=pattern):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = Path(temporary_directory)
                    (root / "docs-sync-rules.toml").write_text(
                        "[[rule]]\n"
                        f'trigger = ["{pattern}"]\n'
                        'one_of = ["docs/**"]\n'
                        'reason = "Malformed patterns are never policy."\n',
                        encoding="utf-8",
                    )
                    run(["git", "init", "-b", "main"], cwd=root)
                    run(["git", "add", "docs-sync-rules.toml"], cwd=root)
                    run(["git", "commit", "-m", "rules"], cwd=root)

                    explicit = run(
                        checker_command(
                            DOCS_SYNC_CHECKER,
                            root,
                            "--strict",
                            "--files",
                            "unrelated.txt",
                        )
                    )
                    empty_diff = run(
                        checker_command(
                            DOCS_SYNC_CHECKER,
                            root,
                            "--strict",
                            "--base",
                            "HEAD",
                        )
                    )

                    for result in (explicit, empty_diff):
                        self.assertEqual(2, result.returncode, result.stdout)
                        self.assertIn("invalid glob", result.stdout)
                        self.assertNotIn("Traceback", result.stdout)

    def test_invalid_toml_schema_is_a_configuration_error(self):
        invalid_documents = (
            "[[rule]\n",
            '[[rule]]\ntrigger = ["src/**"]\none_of = ["docs/**"]\nreason = "   "\n',
            "[[rule]]\n"
            'trigger = "src/**"\n'
            'one_of = ["docs/**"]\n'
            'reason = "Document changes."\n',
        )
        for document in invalid_documents:
            with self.subTest(document=document):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = Path(temporary_directory)
                    (root / "docs-sync-rules.toml").write_text(
                        document,
                        encoding="utf-8",
                    )

                    result = run(checker_command(DOCS_SYNC_CHECKER, root, "--strict"))

                    self.assertEqual(2, result.returncode, result.stdout)


if __name__ == "__main__":
    unittest.main()
