#!/usr/bin/env python3
"""Check that repository authority and skill discovery surfaces do not fork."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


REDIRECT_MARKER = "<!-- agent-kit: authority=AGENTS.md -->"
SKILL_ROOTS = (Path(".agents/skills"), Path(".claude/skills"))
FRONTMATTER_NAME = re.compile(r"^name:[ \t]*(.*?)[ \t]*$", re.MULTILINE)
CONTRACT_REFERENCE = re.compile(r"(?<![\w.-])AGENTS\.md(?![\w.-])")


class AuthorityEnvironmentError(RuntimeError):
    """The requested repository cannot be inspected reliably."""


def resolve_root(value: Path) -> Path:
    """Return an existing repository directory or raise an environment error."""

    try:
        root = value.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise AuthorityEnvironmentError(
            f"cannot resolve repository root {value}: {error}"
        ) from error
    if not root.is_dir():
        raise AuthorityEnvironmentError(f"repository root must be a directory: {value}")
    return root


def without_yaml_comments(text: str) -> str:
    """Remove YAML comments while preserving quoted ``#`` characters."""

    visible_lines = []
    for line in text.splitlines():
        visible = []
        quote: str | None = None
        escaped = False
        for index, character in enumerate(line):
            if quote == '"':
                visible.append(character)
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == quote:
                    quote = None
            elif quote == "'":
                visible.append(character)
                if character == quote:
                    quote = None
            elif character in {'"', "'"}:
                quote = character
                visible.append(character)
            elif character == "#" and (index == 0 or line[index - 1].isspace()):
                break
            else:
                visible.append(character)
        visible_lines.append("".join(visible))
    return "\n".join(visible_lines)


class AuthorityChecker:
    """Collect generic authority-surface findings for one repository."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.findings: list[str] = []
        self.skill_count = 0

    def finding(self, message: str) -> None:
        self.findings.append(message)

    def read_text(self, path: Path) -> str:
        relative = path.relative_to(self.root).as_posix()
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise AuthorityEnvironmentError(
                f"cannot read {relative}: {error}"
            ) from error

    def check_contract(self) -> None:
        agents = self.root / "AGENTS.md"
        if agents.is_symlink() or not agents.is_file():
            self.finding("AGENTS.md must be the physical repository contract file")

        claude = self.root / "CLAUDE.md"
        if not claude.exists() and not claude.is_symlink():
            return
        if claude.is_symlink():
            try:
                target = claude.resolve(strict=False)
                expected = agents.resolve(strict=False)
            except (OSError, RuntimeError) as error:
                raise AuthorityEnvironmentError(
                    f"cannot resolve CLAUDE.md: {error}"
                ) from error
            if target != expected:
                self.finding("CLAUDE.md symlink must resolve to AGENTS.md")
            return
        if not claude.is_file():
            self.finding("CLAUDE.md must be a file or a symlink to AGENTS.md")
            return

        lines = self.read_text(claude).splitlines()
        if REDIRECT_MARKER not in (line.strip() for line in lines):
            self.finding(
                "CLAUDE.md must symlink to AGENTS.md or contain the exact "
                f"redirect marker {REDIRECT_MARKER}"
            )

    @staticmethod
    def frontmatter_name(text: str) -> str | None:
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return None
        try:
            boundary = lines.index("---", 1)
        except ValueError:
            return None
        matches = FRONTMATTER_NAME.findall("\n".join(lines[1:boundary]))
        if len(matches) != 1:
            return None
        value = matches[0].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1].strip()
        return value or None

    def check_skill_directory(self, directory: Path) -> None:
        relative = directory.relative_to(self.root).as_posix()
        if directory.is_symlink():
            self.finding(f"skill directory must be physical: {relative}")
            return
        skill_file = directory / "SKILL.md"
        if skill_file.is_symlink() or not skill_file.is_file():
            self.finding(f"skill directory has no physical SKILL.md: {relative}")
            return
        name = self.frontmatter_name(self.read_text(skill_file))
        if name != directory.name:
            shown = repr(name) if name is not None else "missing or ambiguous"
            self.finding(
                f"{relative}/SKILL.md frontmatter name is {shown}; "
                f"expected {directory.name!r}"
            )
        self.skill_count += 1

    def inspect_skill_root(self, root: Path) -> None:
        try:
            children = sorted(root.iterdir(), key=lambda path: path.name)
        except OSError as error:
            relative = root.relative_to(self.root).as_posix()
            raise AuthorityEnvironmentError(
                f"cannot enumerate {relative}: {error}"
            ) from error
        for child in children:
            if child.is_dir() or child.is_symlink():
                self.check_skill_directory(child)

    def check_skill_roots(self) -> None:
        roots = [self.root / relative for relative in SKILL_ROOTS]
        present = [path for path in roots if path.exists() or path.is_symlink()]
        physical = [path for path in present if path.is_dir() and not path.is_symlink()]

        for path in present:
            if not path.is_symlink() and not path.is_dir():
                relative = path.relative_to(self.root).as_posix()
                self.finding(f"skills root is not a directory: {relative}")

        if len(physical) != 1:
            shown = ", ".join(
                path.relative_to(self.root).as_posix() for path in physical
            )
            self.finding(
                "expected exactly one physical skills root under "
                f".agents/skills or .claude/skills; found {len(physical)}"
                + (f" ({shown})" if shown else "")
            )

        if len(present) == 2:
            aliases = [path for path in present if path.is_symlink()]
            if len(aliases) != 1 or len(physical) != 1:
                self.finding(
                    "when both skills roots exist, one must be a symlink to the other"
                )
            else:
                try:
                    alias_target = aliases[0].resolve(strict=False)
                    physical_target = physical[0].resolve(strict=False)
                except (OSError, RuntimeError) as error:
                    raise AuthorityEnvironmentError(
                        f"cannot resolve skills-root alias: {error}"
                    ) from error
                if alias_target != physical_target:
                    self.finding(
                        f"{aliases[0].relative_to(self.root).as_posix()} "
                        "must resolve to the physical skills root"
                    )

        for root in physical:
            self.inspect_skill_root(root)

    def check_codex_config(self) -> None:
        config = self.root / ".codex/config.yaml"
        if not config.exists() and not config.is_symlink():
            return
        if not config.is_file():
            self.finding(".codex/config.yaml must be a readable file when present")
            return
        visible_config = without_yaml_comments(self.read_text(config))
        if not CONTRACT_REFERENCE.search(visible_config):
            self.finding(".codex/config.yaml must reference the AGENTS.md contract")

    def run(self) -> list[str]:
        self.check_contract()
        self.check_skill_roots()
        self.check_codex_config()
        return self.findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check repository authority and skill discovery surfaces."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root to inspect (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return exit 1 for findings instead of warning-only exit 0",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        checker = AuthorityChecker(resolve_root(arguments.root))
        findings = checker.run()
    except AuthorityEnvironmentError as error:
        print(f"check_authority: configuration error: {error}", file=sys.stderr)
        return 2

    if findings:
        level = "ERROR" if arguments.strict else "WARNING"
        print(
            f"check_authority: {level} ({len(findings)} finding(s)):",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1 if arguments.strict else 0

    print(f"check_authority: OK ({checker.skill_count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
