#!/usr/bin/env python3
"""Check local Markdown links under the repository's bounded document roots."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote


SCAN_FILES = (Path("AGENTS.md"), Path("README.md"))
SCAN_DIRECTORIES = (
    Path("docs"),
    Path(".agents/state"),
    Path(".agents/skills"),
)
FENCE_OPEN = re.compile(r"^[ ]{0,3}(`{3,}|~{3,}).*$")
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^)\n]+)\)")
REFERENCE_LINK = re.compile(
    r"^[ ]{0,3}\[[^\]\n]+\]:[ \t]*(<[^>\n]+>|\S+)",
    re.MULTILINE,
)
EXTERNAL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


class DocumentLinkEnvironmentError(RuntimeError):
    """The requested repository or Markdown corpus cannot be read reliably."""


def resolve_root(value: Path) -> Path:
    try:
        root = value.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise DocumentLinkEnvironmentError(
            f"cannot resolve repository root {value}: {error}"
        ) from error
    if not root.is_dir():
        raise DocumentLinkEnvironmentError(
            f"repository root must be a directory: {value}"
        )
    return root


def visible_markdown_lines(text: str):
    """Yield line numbers and content outside fenced Markdown code blocks."""

    fence_character: str | None = None
    fence_length = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        if fence_character is not None:
            closing = re.fullmatch(
                rf"[ ]{{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[^\S\n]*",
                line,
            )
            if closing:
                fence_character = None
                fence_length = 0
            continue

        opening = FENCE_OPEN.match(line)
        if opening:
            marker = opening.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            continue
        yield line_number, line


def link_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<"):
        boundary = value.find(">")
        return value[1:boundary] if boundary >= 0 else value
    return value.split(maxsplit=1)[0]


class DocumentLinkChecker:
    """Collect unresolved or escaping Markdown links for one repository."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.findings: list[str] = []
        self.file_count = 0
        self.link_count = 0

    def finding(self, message: str) -> None:
        self.findings.append(message)

    def discover(self) -> tuple[Path, ...]:
        found: set[Path] = set()
        for relative in SCAN_FILES:
            path = self.root / relative
            if path.is_file():
                found.add(path)
            elif path.exists() or path.is_symlink():
                self.finding(f"Markdown scan path is not a file: {relative}")

        for relative in SCAN_DIRECTORIES:
            directory = self.root / relative
            if not directory.exists() and not directory.is_symlink():
                continue
            if not directory.is_dir():
                self.finding(f"Markdown scan root is not a directory: {relative}")
                continue
            try:
                candidates = directory.rglob("*.md")
                for path in candidates:
                    if path.is_file():
                        found.add(path)
            except OSError as error:
                raise DocumentLinkEnvironmentError(
                    f"cannot enumerate {relative}: {error}"
                ) from error
        return tuple(
            sorted(found, key=lambda path: path.relative_to(self.root).as_posix())
        )

    def read_text(self, path: Path) -> str:
        relative = path.relative_to(self.root).as_posix()
        try:
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise DocumentLinkEnvironmentError(
                f"cannot resolve {relative}: {error}"
            ) from error
        if not resolved.is_relative_to(self.root):
            self.finding(f"Markdown file escapes repository root: {relative}")
            return ""
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise DocumentLinkEnvironmentError(
                f"cannot read {relative}: {error}"
            ) from error

    def check_destination(
        self,
        source: Path,
        line_number: int,
        raw_destination: str,
    ) -> None:
        destination = link_destination(raw_destination)
        if (
            not destination
            or destination.startswith(("#", "//"))
            or EXTERNAL_SCHEME.match(destination)
        ):
            return

        local_text = destination.split("#", 1)[0].split("?", 1)[0]
        if not local_text:
            return
        local_text = unquote(local_text)
        candidate = (
            self.root / local_text.lstrip("/")
            if local_text.startswith("/")
            else source.parent / local_text
        )
        try:
            resolved = candidate.resolve(strict=False)
        except (OSError, RuntimeError) as error:
            raise DocumentLinkEnvironmentError(
                f"cannot resolve link {destination!r}: {error}"
            ) from error

        relative_source = source.relative_to(self.root).as_posix()
        prefix = f"{relative_source}:{line_number}: link {destination!r}"
        if not resolved.is_relative_to(self.root):
            self.finding(f"{prefix} escapes repository root")
        elif not candidate.exists():
            self.finding(f"{prefix} does not exist")

    def check_file(self, path: Path) -> None:
        text = self.read_text(path)
        for line_number, line in visible_markdown_lines(text):
            matches = [
                *(match.group(1) for match in INLINE_LINK.finditer(line)),
                *(match.group(1) for match in REFERENCE_LINK.finditer(line)),
            ]
            for destination in matches:
                self.link_count += 1
                self.check_destination(path, line_number, destination)
        self.file_count += 1

    def run(self) -> list[str]:
        for path in self.discover():
            self.check_file(path)
        return self.findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check local links in the bounded repository Markdown corpus."
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
        checker = DocumentLinkChecker(resolve_root(arguments.root))
        findings = checker.run()
    except DocumentLinkEnvironmentError as error:
        print(f"check_doc_links: configuration error: {error}", file=sys.stderr)
        return 2

    if findings:
        level = "ERROR" if arguments.strict else "WARNING"
        print(
            f"check_doc_links: {level} ({len(findings)} finding(s)):",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1 if arguments.strict else 0

    print(
        f"check_doc_links: OK ({checker.file_count} Markdown files, "
        f"{checker.link_count} links)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
