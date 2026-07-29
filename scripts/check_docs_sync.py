#!/usr/bin/env python3
"""Check configurable documentation obligations for a repository change set."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tomllib


RULES_PATH = Path("docs-sync-rules.toml")


class DocumentationSyncConfigurationError(RuntimeError):
    """The repository root or TOML rule document is invalid."""


class ChangeSetUnavailable(RuntimeError):
    """No reliable changed-file set can be established."""


@dataclass(frozen=True)
class Rule:
    triggers: tuple[str, ...]
    one_of: tuple[str, ...]
    reason: str


def resolve_root(value: Path) -> Path:
    try:
        root = value.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise DocumentationSyncConfigurationError(
            f"cannot resolve repository root {value}: {error}"
        ) from error
    if not root.is_dir():
        raise DocumentationSyncConfigurationError(
            f"repository root must be a directory: {value}"
        )
    return root


def validate_globs(value: object, field: str, index: int) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(pattern, str) or not pattern.strip() for pattern in value)
    ):
        raise DocumentationSyncConfigurationError(
            f"rule {index} {field} must be a nonempty list of nonempty strings"
        )
    patterns = tuple(pattern.strip() for pattern in value)
    for pattern in patterns:
        if (
            "\\" in pattern
            or pattern.startswith("/")
            or any(part in {"", ".", ".."} for part in pattern.split("/"))
        ):
            raise DocumentationSyncConfigurationError(
                f"rule {index} {field} has unsafe repository glob {pattern!r}"
            )
    return patterns


def load_rules(root: Path) -> tuple[Rule, ...]:
    path = root / RULES_PATH
    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise DocumentationSyncConfigurationError(
            f"cannot read {RULES_PATH}: {error}"
        ) from error
    if not isinstance(document, dict) or set(document) - {"rule"}:
        raise DocumentationSyncConfigurationError(
            f"{RULES_PATH} may contain only [[rule]] entries"
        )
    rows = document.get("rule", [])
    if not isinstance(rows, list):
        raise DocumentationSyncConfigurationError(
            f"{RULES_PATH} rule must be an array of tables"
        )

    rules = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or set(row) != {"trigger", "one_of", "reason"}:
            raise DocumentationSyncConfigurationError(
                f"rule {index} must contain only trigger, one_of, and reason"
            )
        reason = row["reason"]
        if not isinstance(reason, str) or not reason.strip():
            raise DocumentationSyncConfigurationError(
                f"rule {index} reason must be a nonempty string"
            )
        rules.append(
            Rule(
                triggers=validate_globs(row["trigger"], "trigger", index),
                one_of=validate_globs(row["one_of"], "one_of", index),
                reason=reason.strip(),
            )
        )
    return tuple(rules)


def normalize_changed_path(value: str) -> str:
    value = value.removeprefix("./")
    if (
        not value
        or "\\" in value
        or value.startswith("/")
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise DocumentationSyncConfigurationError(
            f"changed file must be a safe repository-relative path: {value!r}"
        )
    return PurePosixPath(value).as_posix()


def run_git(root: Path, arguments: list[str], *, binary: bool = False):
    try:
        return subprocess.run(
            ["git", "-C", str(root), *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=not binary,
            check=False,
        )
    except OSError as error:
        raise ChangeSetUnavailable(f"cannot run git: {error}") from error


def changed_files_from_base(root: Path, base: str) -> tuple[str, ...]:
    worktree = run_git(root, ["rev-parse", "--show-toplevel"])
    if worktree.returncode != 0:
        raise ChangeSetUnavailable("repository is not a Git work tree")
    try:
        top = Path(worktree.stdout.strip()).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ChangeSetUnavailable(
            f"cannot resolve Git work-tree root: {error}"
        ) from error
    if top != root:
        raise ChangeSetUnavailable(f"--root must be the Git work-tree root ({top})")

    merge_base = run_git(root, ["merge-base", "HEAD", base])
    if merge_base.returncode != 0 or not merge_base.stdout.strip():
        detail = merge_base.stderr.strip() or f"cannot resolve base {base!r}"
        raise ChangeSetUnavailable(detail)

    difference = run_git(
        root,
        ["diff", "--name-only", "-z", f"{merge_base.stdout.strip()}..HEAD"],
        binary=True,
    )
    if difference.returncode != 0:
        detail = difference.stderr.decode("utf-8", errors="replace").strip()
        raise ChangeSetUnavailable(detail or "cannot compute changed files")
    try:
        names = difference.stdout.decode("utf-8").split("\0")
    except UnicodeDecodeError as error:
        raise ChangeSetUnavailable("Git returned a non-UTF-8 changed path") from error
    return tuple(sorted({normalize_changed_path(name) for name in names if name}))


def glob_regex(pattern: str) -> re.Pattern[str]:
    """Compile repository globs where ``*`` stops at `/` and ``**`` does not."""

    pieces = ["^"]
    index = 0
    while index < len(pattern):
        if pattern[index : index + 3] == "**/":
            pieces.append("(?:[^/]+/)*")
            index += 3
        elif pattern[index : index + 2] == "**":
            pieces.append(".*")
            index += 2
        elif pattern[index] == "*":
            pieces.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            pieces.append("[^/]")
            index += 1
        else:
            pieces.append(re.escape(pattern[index]))
            index += 1
    pieces.append("$")
    return re.compile("".join(pieces))


def matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(glob_regex(pattern).fullmatch(path) for pattern in patterns)


def evaluate(rules: tuple[Rule, ...], changed: tuple[str, ...]) -> list[str]:
    findings = []
    for index, rule in enumerate(rules, start=1):
        triggered = sorted(path for path in changed if matches_any(path, rule.triggers))
        if not triggered or any(matches_any(path, rule.one_of) for path in changed):
            continue
        findings.append(
            f"rule {index} triggered by {', '.join(triggered)}; "
            f"expected one of {', '.join(rule.one_of)}. {rule.reason}"
        )
    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check documentation-sync rules for a repository change set."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root containing docs-sync-rules.toml",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail on findings and on an unavailable changed-file set",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--files",
        nargs="+",
        metavar="PATH",
        help="explicit repository-relative changed files",
    )
    source.add_argument(
        "--base",
        help="Git ref to merge with HEAD before computing the changed files",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        root = resolve_root(arguments.root)
        rules = load_rules(root)
        if not rules:
            print("check_docs_sync: OK (0 rules)")
            return 0

        if arguments.files is not None:
            changed = tuple(
                sorted({normalize_changed_path(value) for value in arguments.files})
            )
        elif arguments.base is not None:
            changed = changed_files_from_base(root, arguments.base)
        else:
            raise ChangeSetUnavailable("no changed-file source; pass --files or --base")
        findings = evaluate(rules, changed)
    except DocumentationSyncConfigurationError as error:
        print(f"check_docs_sync: configuration error: {error}", file=sys.stderr)
        return 2
    except ChangeSetUnavailable as error:
        if arguments.strict:
            print(f"check_docs_sync: configuration error: {error}", file=sys.stderr)
            return 2
        print(f"check_docs_sync: SKIPPED ({error})", file=sys.stderr)
        return 0

    if findings:
        level = "ERROR" if arguments.strict else "WARNING"
        print(
            f"check_docs_sync: {level} ({len(findings)} finding(s)):",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1 if arguments.strict else 0

    print(f"check_docs_sync: OK ({len(rules)} rules, {len(changed)} changed files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
