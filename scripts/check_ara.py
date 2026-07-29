#!/usr/bin/env python3
"""Validate the structure and on-disk bindings of the ``ara/`` claim ledger.

The checks are deliberately structural:

1. Required ARA layer files exist.
2. Local paths linked from ``ara/PAPER.md`` resolve.
3. Claim headings are well formed and claim IDs are unique.
4. Every claim has the nine required fields and only known optional fields.
5. Every status starts with a known disposition.
6. Claim dependencies resolve and do not point to the claim itself.
7. Repository proof paths resolve, and disposed claims cite an existing path.
8. Staged observation IDs resolve.
9. ``README.md`` points readers to the claim ledger.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "ara/PAPER.md",
    "ara/logic/claims.md",
    "ara/logic/problem.md",
    "ara/logic/solution/heuristics.md",
    "ara/staging/observations.yaml",
    "ara/trace/exploration_tree.yaml",
    "ara/trace/pm_reasoning_log.yaml",
    "ara/trace/sessions/session_index.yaml",
    "ara/evidence/README.md",
)

REQUIRED_CLAIM_FIELDS = (
    "Statement",
    "Status",
    "Provenance",
    "Crystallized via",
    "Falsification criteria",
    "Proof",
    "Dependencies",
    "Tags",
    "From staging",
)
OPTIONAL_CLAIM_FIELDS = ("Boundary",)

STATUS_WORDS = frozenset(
    {
        "supported",
        "refuted",
        "untested",
        "unavailable",
        "hypothesis",
        "superseded",
        "withdrawn",
    }
)
PATH_ROOTS = (
    "ara/",
    "docs/",
    "scripts/",
    "tests/",
    ".agents/",
    "distribution/",
)

CLAIM_HEADING = re.compile(r"^## (C\d+): (\S.*)$")
FIELD = re.compile(r"^- \*\*([A-Za-z][A-Za-z ]*)\*\*:\s*(.*)$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
COMMIT_REFERENCE = re.compile(r"^[0-9a-f]{7,40}$")


class AraChecker:
    """Collect all ledger findings for one repository root."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.findings: list[str] = []
        self.claim_count = 0

    def finding(self, message: str) -> None:
        self.findings.append(message)

    def read(self, relative: str) -> str:
        try:
            return (self.root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            self.finding(f"cannot read {relative}: {error}")
            return ""

    def check_required_files(self) -> None:
        for relative in REQUIRED_FILES:
            if not (self.root / relative).is_file():
                self.finding(f"required ARA file missing: {relative}")

    @staticmethod
    def _link_destination(raw_destination: str) -> str:
        destination = raw_destination.strip()
        if destination.startswith("<") and ">" in destination:
            return destination[1 : destination.index(">")]
        return destination.split(maxsplit=1)[0]

    def check_paper_links(self) -> None:
        paper_relative = "ara/PAPER.md"
        paper = self.read(paper_relative)
        paper_directory = self.root / "ara"
        for match in MARKDOWN_LINK.finditer(paper):
            destination = self._link_destination(match.group(1))
            if (
                not destination
                or destination.startswith("#")
                or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination)
            ):
                continue
            path_text = destination.split("#", 1)[0].split("?", 1)[0]
            if path_text and not (paper_directory / path_text).exists():
                self.finding(
                    f"{paper_relative} links to '{destination}', which does not exist"
                )

    def parse_claims(self) -> dict[str, dict[str, str]]:
        claims: dict[str, dict[str, str]] = {}
        current_claim: str | None = None
        current_field: str | None = None

        for line_number, line in enumerate(
            self.read("ara/logic/claims.md").splitlines(), start=1
        ):
            heading = CLAIM_HEADING.match(line)
            if heading:
                claim_id = heading.group(1)
                if claim_id in claims:
                    self.finding(
                        "ara/logic/claims.md:"
                        f"{line_number}: duplicate claim ID '{claim_id}'"
                    )
                claims.setdefault(claim_id, {})
                current_claim = claim_id
                current_field = None
                continue

            if line.startswith("## "):
                self.finding(
                    "ara/logic/claims.md:"
                    f"{line_number}: malformed or stray claim heading {line!r}"
                )
                current_claim = None
                current_field = None
                continue

            if current_claim is None:
                continue

            field = FIELD.match(line)
            if field:
                field_name = field.group(1)
                if field_name in claims[current_claim]:
                    self.finding(f"claim {current_claim} repeats field '{field_name}'")
                claims[current_claim][field_name] = field.group(2).strip()
                current_field = field_name
                continue

            if current_field and line.startswith("  ") and line.strip():
                previous = claims[current_claim][current_field]
                claims[current_claim][current_field] = (
                    f"{previous} {line.strip()}".strip()
                )
                continue

            if not line.strip() or not line.startswith("  "):
                current_field = None

        return claims

    def check_claim_fields(self, claims: dict[str, dict[str, str]]) -> None:
        known_fields = set(REQUIRED_CLAIM_FIELDS) | set(OPTIONAL_CLAIM_FIELDS)
        for claim_id, fields in claims.items():
            for required in REQUIRED_CLAIM_FIELDS:
                if required not in fields:
                    self.finding(
                        f"claim {claim_id} is missing required field '{required}'"
                    )
            for unknown in sorted(set(fields) - known_fields):
                self.finding(f"claim {claim_id} has unknown field '{unknown}'")

    def check_claim_statuses(self, claims: dict[str, dict[str, str]]) -> None:
        for claim_id, fields in claims.items():
            words = fields.get("Status", "").split()
            if not words:
                continue
            disposition = words[0].strip(".,;:").lower()
            if disposition not in STATUS_WORDS:
                self.finding(
                    f"claim {claim_id} has unknown status disposition '{disposition}'"
                )

    def check_claim_dependencies(self, claims: dict[str, dict[str, str]]) -> None:
        for claim_id, fields in claims.items():
            for dependency in re.findall(r"\bC\d+\b", fields.get("Dependencies", "")):
                if dependency == claim_id:
                    self.finding(f"claim {claim_id} depends on itself")
                elif dependency not in claims:
                    self.finding(
                        f"claim {claim_id} depends on undefined claim '{dependency}'"
                    )

    @staticmethod
    def _proof_entries(proof: str) -> tuple[str, ...]:
        return tuple(
            part.strip().strip("`\"'")
            for part in proof.strip().strip("[]").split(",")
            if part.strip()
        )

    def check_claim_proofs(self, claims: dict[str, dict[str, str]]) -> None:
        for claim_id, fields in claims.items():
            existing_path = False
            for entry in self._proof_entries(fields.get("Proof", "")):
                if COMMIT_REFERENCE.fullmatch(entry):
                    continue
                if not entry.startswith(PATH_ROOTS):
                    continue
                path_text = entry.split("::", 1)[0]
                if (self.root / path_text).exists():
                    existing_path = True
                else:
                    self.finding(
                        f"claim {claim_id} cites missing proof path '{path_text}'"
                    )

            status_words = fields.get("Status", "").split()
            disposition = status_words[0].lower() if status_words else ""
            if disposition in {"supported", "refuted"} and not existing_path:
                self.finding(
                    f"claim {claim_id} is {disposition} but cites no existing "
                    "repository proof path"
                )

    def check_staging_ids(self, claims: dict[str, dict[str, str]]) -> None:
        observations = self.read("ara/staging/observations.yaml")
        known_observations = set(
            re.findall(
                r'^\s*-\s*id:\s*"?(\bO\d+\b)"?\s*$',
                observations,
                flags=re.MULTILINE,
            )
        )
        for claim_id, fields in claims.items():
            for observation in re.findall(r"\bO\d+\b", fields.get("From staging", "")):
                if observation not in known_observations:
                    self.finding(
                        f"claim {claim_id} references undefined staging "
                        f"observation '{observation}'"
                    )

    def check_readme_discovery(self) -> None:
        if "ara/logic/claims.md" not in self.read("README.md"):
            self.finding("README.md does not mention ara/logic/claims.md")

    def run(self) -> list[str]:
        self.check_required_files()
        self.check_paper_links()
        claims = self.parse_claims()
        self.claim_count = len(claims)
        if not claims:
            self.finding("ara/logic/claims.md defines no claims")
        self.check_claim_fields(claims)
        self.check_claim_statuses(claims)
        self.check_claim_dependencies(claims)
        self.check_claim_proofs(claims)
        self.check_staging_ids(claims)
        self.check_readme_discovery()
        return self.findings


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checker = AraChecker(root)
    findings = checker.run()
    if findings:
        print(f"check_ara: {len(findings)} problem(s):", file=sys.stderr)
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1
    print(f"check_ara: OK ({checker.claim_count} claims)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
