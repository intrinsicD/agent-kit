#!/usr/bin/env python3
"""Install and inspect agent-kit's non-overwriting workflow payload."""

from dataclasses import dataclass
import argparse
import io
import json
from pathlib import Path
import re
import shutil
import sys


SOURCE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SOURCE_ROOT / "distribution/manifest.json"
SKILL_TOKENS = (
    "code-audit",
    "experiment-design",
    "handoff",
    "implementation",
    "novel-idea-generation",
    "productization",
    "repo-organization",
    "research-methods",
    "results-audit",
    "review-and-falsification",
    "task-orchestration",
)
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
GROUP_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
INLINE_CODE_PATTERN = re.compile(r"`([^`\n]+)`")
SKILL_TOKEN_PATTERN = re.compile(
    r"(?<![a-z0-9-])("
    + "|".join(
        re.escape(token) for token in sorted(SKILL_TOKENS, key=len, reverse=True)
    )
    + r")(?![a-z0-9-])"
)


class ManifestError(ValueError):
    """The distribution manifest or a selected payload is malformed or unsafe."""


@dataclass(frozen=True)
class PayloadFile:
    source: Path
    destination: Path
    group: str = "core"
    user_owned: bool = False


@dataclass(frozen=True)
class DistributionManifest:
    version: int
    groups: dict[str, tuple[PayloadFile, ...]]


@dataclass(frozen=True)
class PlannedFile:
    source: Path | None
    destination: Path
    content: bytes
    user_owned: bool = False


def _relative_path(value, field):
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{field} must be a nonempty string")
    if "\\" in value:
        raise ManifestError(f"{field} must use forward slashes: {value!r}")

    parts = value.split("/")
    if value.startswith("/") or any(part in {"", ".", ".."} for part in parts):
        raise ManifestError(f"{field} must be a safe relative path: {value!r}")
    return Path(*parts)


def load_manifest(source_root=SOURCE_ROOT, manifest_path=MANIFEST_PATH):
    """Load and validate the versioned, named-group distribution manifest."""

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ManifestError(f"cannot read {manifest_path}: {error}") from error

    if not isinstance(manifest, dict) or set(manifest) != {"version", "groups"}:
        raise ManifestError("manifest must contain only `version` and `groups`")
    if type(manifest["version"]) is not int or manifest["version"] != 2:
        raise ManifestError("manifest version must be 2")
    if not isinstance(manifest["groups"], dict) or not manifest["groups"]:
        raise ManifestError("manifest groups must be a nonempty object")
    if "core" not in manifest["groups"]:
        raise ManifestError("manifest groups must include `core`")

    root = source_root.resolve()
    destinations = set()
    sources = set()
    groups = {}
    for group, rows in manifest["groups"].items():
        if not isinstance(group, str) or not GROUP_PATTERN.fullmatch(group):
            raise ManifestError(f"invalid group name: {group!r}")
        if not isinstance(rows, list) or not rows:
            raise ManifestError(f"manifest group {group!r} must be a nonempty list")

        entries = []
        for index, row in enumerate(rows):
            label = f"group {group!r} file {index}"
            if not isinstance(row, dict) or set(row) != {"source", "destination"}:
                raise ManifestError(
                    f"manifest {label} must contain source and destination"
                )

            source_relative = _relative_path(row["source"], f"{label} source")
            destination = _relative_path(row["destination"], f"{label} destination")
            if destination.parts[0] == ".git":
                raise ManifestError(
                    f"{label} destination may not enter .git: {destination}"
                )
            if destination in destinations:
                raise ManifestError(f"duplicate destination: {destination}")
            if source_relative in sources:
                raise ManifestError(f"duplicate source: {source_relative}")
            destinations.add(destination)
            sources.add(source_relative)

            source = source_root / source_relative
            if source.is_symlink() or not source.is_file():
                raise ManifestError(f"payload source must be a regular file: {source}")
            if not source.resolve().is_relative_to(root):
                raise ManifestError(f"payload source escapes repository: {source}")
            entries.append(
                PayloadFile(
                    source=source,
                    destination=destination,
                    group=group,
                    user_owned=source_relative.parts[:2]
                    == ("distribution", "templates"),
                )
            )
        groups[group] = tuple(entries)

    return DistributionManifest(version=manifest["version"], groups=groups)


def select_payload(manifest, groups=("core",)):
    """Return the stable union of named groups, rejecting unknown names."""

    selected = []
    seen = set()
    for group in groups:
        if group in seen:
            continue
        if group not in manifest.groups:
            raise ManifestError(f"unknown payload group: {group}")
        seen.add(group)
        selected.extend(manifest.groups[group])
    return tuple(selected)


def load_payload(
    source_root=SOURCE_ROOT, manifest_path=MANIFEST_PATH, groups=("core",)
):
    """Compatibility helper returning the selected manifest payload."""

    return select_payload(load_manifest(source_root, manifest_path), groups)


def validate_slug(slug):
    """Validate and return a skill namespace slug."""

    if not isinstance(slug, str) or len(slug) > 24 or not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            "slug must match ^[a-z][a-z0-9-]*$ and be at most 24 characters"
        )
    return slug


def _skill_token(destination):
    parts = destination.parts
    if (
        len(parts) == 4
        and parts[:2] == (".agents", "skills")
        and parts[2] in SKILL_TOKENS
        and parts[3] == "SKILL.md"
    ):
        return parts[2]
    return None


def _rewrite_inline_skill_names(text, prefix):
    def rewrite_span(match):
        return (
            "`"
            + SKILL_TOKEN_PATTERN.sub(
                lambda token: prefix + token.group(0), match.group(1)
            )
            + "`"
        )

    return INLINE_CODE_PATTERN.sub(rewrite_span, text)


def _rewrite_frontmatter_name(text, token, prefix):
    if not text.startswith("---\n"):
        raise ManifestError(f"skill {token!r} has no YAML frontmatter")
    boundary = text.find("\n---", 4)
    if boundary < 0:
        raise ManifestError(f"skill {token!r} has unterminated YAML frontmatter")

    frontmatter = text[:boundary]
    pattern = re.compile(rf"(?m)^name:[ \t]*{re.escape(token)}[ \t]*$")
    rewritten, count = pattern.subn(f"name: {prefix}{token}", frontmatter)
    if count != 1:
        raise ManifestError(
            f"skill {token!r} must have exactly one matching frontmatter name"
        )
    return rewritten + text[boundary:]


def render_payload(payload, slug=None):
    """Render destinations and bounded skill naming surfaces for installation."""

    prefix = ""
    if slug is not None:
        prefix = f"{validate_slug(slug)}-"

    planned = []
    for entry in payload:
        try:
            content = entry.source.read_bytes()
        except OSError as error:
            raise ManifestError(
                f"cannot read payload source {entry.source}: {error}"
            ) from error

        token = _skill_token(entry.destination)
        destination = entry.destination
        if prefix:
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ManifestError(
                    f"payload source is not UTF-8 text: {entry.source}"
                ) from error
            text = _rewrite_inline_skill_names(text, prefix)
            if token is not None:
                text = _rewrite_frontmatter_name(text, token, prefix)
                destination = Path(".agents", "skills", f"{prefix}{token}", "SKILL.md")
            content = text.encode("utf-8")

        planned.append(
            PlannedFile(
                source=entry.source,
                destination=destination,
                content=content,
                user_owned=entry.user_owned,
            )
        )
    return tuple(planned)


def find_collisions(target, payload):
    """Return every protected destination or blocking ancestor in the target."""

    collisions = set()
    for entry in payload:
        destination = target / entry.destination
        if destination.exists() or destination.is_symlink():
            collisions.add(entry.destination)

        parent = destination.parent
        while parent != target:
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                collisions.add(parent.relative_to(target))
                break
            parent = parent.parent

    return tuple(sorted(collisions, key=lambda path: path.as_posix()))


def _missing_directories(parent, target):
    missing = []
    current = parent
    while current != target and not current.exists():
        missing.append(current)
        current = current.parent
    return tuple(reversed(missing))


def install_payload(target, payload):
    """Write a preflighted plan exclusively and roll back installer-owned paths."""

    created_files = []
    created_directories = []
    try:
        for entry in payload:
            destination = target / entry.destination
            missing = _missing_directories(destination.parent, target)
            for directory in missing:
                directory.mkdir()
                created_directories.append(directory)

            with destination.open("xb") as destination_stream:
                created_files.append(destination)
                shutil.copyfileobj(io.BytesIO(entry.content), destination_stream)
            if entry.source is not None:
                shutil.copystat(entry.source, destination, follow_symlinks=False)
    except BaseException:
        for path in reversed(created_files):
            path.unlink(missing_ok=True)
        for path in reversed(created_directories):
            try:
                path.rmdir()
            except OSError:
                pass
        raise


def _selected_groups(profiles):
    return ("core", *profiles)


def _build_parser():
    parser = argparse.ArgumentParser(
        description="Install or inspect agent-kit's workflow payload."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    install = commands.add_parser(
        "install",
        help="install into an existing target without overwriting any path",
    )
    install.add_argument("target", type=Path, help="existing target repository")
    naming = install.add_mutually_exclusive_group(required=True)
    naming.add_argument("--slug", help="prefix every distributed skill name")
    naming.add_argument(
        "--no-prefix",
        action="store_true",
        help="explicitly keep the upstream skill names",
    )
    install.add_argument(
        "--profile",
        action="append",
        default=[],
        metavar="GROUP",
        help="add a named manifest group (repeatable; core is always included)",
    )
    return parser


def _validated_target(target):
    resolved = target.resolve()
    if not resolved.is_dir():
        raise ValueError(f"Target must be an existing directory: {target}")
    return resolved


def _run_install(arguments):
    try:
        slug = validate_slug(arguments.slug) if arguments.slug is not None else None
        manifest = load_manifest()
        payload = select_payload(manifest, _selected_groups(arguments.profile))
        plan = render_payload(payload, slug)
        target = _validated_target(arguments.target)
    except (ManifestError, ValueError) as error:
        print(f"Agent workflow configuration is invalid: {error}", file=sys.stderr)
        return 2

    collisions = find_collisions(target, plan)
    if collisions:
        print(
            "Agent workflow installation refused; protected paths exist:",
            file=sys.stderr,
        )
        for collision in collisions:
            print(f"  - {collision.as_posix()}", file=sys.stderr)
        return 1

    try:
        install_payload(target, plan)
    except OSError as error:
        print(f"Agent workflow installation failed: {error}", file=sys.stderr)
        return 1

    print(f"Installed {len(plan)} agent workflow files into {target}.")
    return 0


def main(argv=None):
    arguments = _build_parser().parse_args(argv)
    if arguments.command == "install":
        return _run_install(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")


if __name__ == "__main__":
    sys.exit(main())
