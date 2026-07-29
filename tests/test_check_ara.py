#!/usr/bin/env python3
"""Regression tests for the agent-kit ARA claim-ledger checker."""

import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPOSITORY_ROOT / "scripts/check_ara.py"


def load_checker_module():
    spec = importlib.util.spec_from_file_location(
        "ara_checker_under_test", CHECKER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load checker from {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER_MODULE = load_checker_module()


VALID_CLAIMS = textwrap.dedent(
    """\
    # Claims

    ## C01: First claim
    - **Statement**: The fixture is structurally valid.
    - **Status**: supported
    - **Provenance**: test
    - **Crystallized via**: fixture
    - **Falsification criteria**: The checker reports a finding.
    - **Proof**: [docs/evidence.md, abcdef0]
    - **Dependencies**: []
    - **Tags**: fixture
    - **From staging**: O01

    ## C02: Dependent claim
    - **Statement**: Dependencies can resolve to another claim.
    - **Status**: hypothesis
    - **Provenance**: test
    - **Crystallized via**: fixture
    - **Falsification criteria**: C01 is absent.
    - **Proof**: [abcdef0]
    - **Dependencies**: [C01]
    - **Tags**: fixture
    - **From staging**: O02
    """
)


class AraCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.outside_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        for relative in CHECKER_MODULE.REQUIRED_FILES:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n", encoding="utf-8")

        (self.root / "ara/PAPER.md").write_text(
            "# Fixture ARA\n\n- [Claims](logic/claims.md)\n",
            encoding="utf-8",
        )
        (self.root / "ara/logic/claims.md").write_text(
            VALID_CLAIMS,
            encoding="utf-8",
        )
        (self.root / "ara/staging/observations.yaml").write_text(
            "observations:\n  - id: O01\n  - id: O02\n",
            encoding="utf-8",
        )
        (self.root / "docs").mkdir()
        (self.root / "docs/evidence.md").write_text("proof\n", encoding="utf-8")
        (self.root / "README.md").write_text(
            "Claims live in `ara/logic/claims.md`.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()
        self.outside_directory.cleanup()

    def findings(self):
        return CHECKER_MODULE.AraChecker(self.root).run()

    def replace_claims(self, old, new):
        path = self.root / "ara/logic/claims.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assert_finding_contains(self, expected):
        findings = self.findings()
        self.assertTrue(
            any(expected in finding for finding in findings),
            f"{expected!r} not found in {findings!r}",
        )

    def test_valid_fixture_passes(self):
        self.assertEqual([], self.findings())

    def test_live_ledger_passes(self):
        self.assertEqual([], CHECKER_MODULE.AraChecker(REPOSITORY_ROOT).run())

    def test_missing_required_file_fails(self):
        (self.root / "ara/trace/pm_reasoning_log.yaml").unlink()
        self.assert_finding_contains("required ARA file missing")

    def test_broken_paper_link_fails(self):
        (self.root / "ara/PAPER.md").write_text(
            "# Fixture ARA\n\n- [Missing](logic/missing.md)\n",
            encoding="utf-8",
        )
        self.assert_finding_contains("which does not exist")

    def test_broken_paper_image_path_fails(self):
        (self.root / "ara/PAPER.md").write_text(
            "# Fixture ARA\n\n![Missing](evidence/missing.png)\n",
            encoding="utf-8",
        )
        self.assert_finding_contains("which does not exist")

    def test_duplicate_claim_id_fails(self):
        claims = self.root / "ara/logic/claims.md"
        claims.write_text(
            claims.read_text(encoding="utf-8")
            + "\n## C01: Duplicate\n"
            + VALID_CLAIMS.split("## C01: First claim\n", 1)[1].split("\n## C02:", 1)[
                0
            ],
            encoding="utf-8",
        )
        self.assert_finding_contains("duplicate claim ID")

    def test_stray_level_two_heading_fails(self):
        self.replace_claims("# Claims\n", "# Claims\n\n## Notes\n")
        self.assert_finding_contains("malformed or stray claim heading")

    def test_missing_required_field_fails(self):
        self.replace_claims("- **Provenance**: test\n", "")
        self.assert_finding_contains("missing required field 'Provenance'")

    def test_unknown_field_fails(self):
        self.replace_claims(
            "- **From staging**: O01\n",
            "- **From staging**: O01\n- **Mystery**: value\n",
        )
        self.assert_finding_contains("unknown field 'Mystery'")

    def test_punctuated_unknown_field_fails(self):
        self.replace_claims(
            "- **From staging**: O01\n",
            "- **From staging**: O01\n- **Mystery-key** : value\n",
        )
        self.assert_finding_contains("unknown field 'Mystery-key'")

    def test_boundary_is_an_accepted_optional_field(self):
        self.replace_claims(
            "- **From staging**: O01\n",
            "- **From staging**: O01\n- **Boundary**: Fixture scope only.\n",
        )
        self.assertEqual([], self.findings())

    def test_unknown_status_fails(self):
        self.replace_claims("- **Status**: supported\n", "- **Status**: accepted\n")
        self.assert_finding_contains("unknown status disposition 'accepted'")

    def test_punctuated_disposed_status_still_requires_existing_path(self):
        self.replace_claims("- **Status**: supported\n", "- **Status**: supported:\n")
        self.replace_claims("[docs/evidence.md, abcdef0]", "[abcdef0]")
        self.assert_finding_contains("cites no existing repository proof path")

    def test_empty_status_fails(self):
        self.replace_claims("- **Status**: supported\n", "- **Status**:\n")
        self.assert_finding_contains("has no status disposition")

    def test_punctuation_only_status_fails(self):
        self.replace_claims("- **Status**: supported\n", "- **Status**: :;,.\n")
        self.assert_finding_contains("has no status disposition")

    def test_unresolved_dependency_fails(self):
        self.replace_claims(
            "- **Dependencies**: [C01]\n", "- **Dependencies**: [C99]\n"
        )
        self.assert_finding_contains("undefined claim 'C99'")

    def test_self_dependency_fails(self):
        self.replace_claims(
            "- **Dependencies**: [C01]\n", "- **Dependencies**: [C02]\n"
        )
        self.assert_finding_contains("depends on itself")

    def test_missing_proof_path_fails(self):
        self.replace_claims("docs/evidence.md", "docs/missing.md")
        self.assert_finding_contains("missing proof path 'docs/missing.md'")

    def test_proof_path_cannot_escape_repository(self):
        outside_path = Path(self.outside_directory.name) / "outside.md"
        outside_path.write_text("external proof\n", encoding="utf-8")
        from_docs = os.path.relpath(outside_path, self.root / "docs")
        escaped_path = f"docs/{Path(from_docs).as_posix()}"
        self.replace_claims("[docs/evidence.md, abcdef0]", f"[{escaped_path}]")
        self.assert_finding_contains("escapes repository root")

    def test_proof_symlink_cannot_escape_repository(self):
        outside_path = Path(self.outside_directory.name) / "outside.md"
        outside_path.write_text("external proof\n", encoding="utf-8")
        (self.root / "docs/external-link.md").symlink_to(outside_path)
        self.replace_claims(
            "[docs/evidence.md, abcdef0]",
            "[docs/external-link.md]",
        )
        self.assert_finding_contains("escapes repository root")

    def test_disposed_claim_requires_existing_path(self):
        self.replace_claims("[docs/evidence.md, abcdef0]", "[abcdef0]")
        self.assert_finding_contains("cites no existing repository proof path")

    def test_undefined_staging_observation_fails(self):
        self.replace_claims("- **From staging**: O01\n", "- **From staging**: O99\n")
        self.assert_finding_contains("undefined staging observation 'O99'")

    def test_readme_must_point_to_claim_ledger(self):
        (self.root / "README.md").write_text("No ledger link.\n", encoding="utf-8")
        self.assert_finding_contains("README.md does not mention")


if __name__ == "__main__":
    unittest.main()
