#!/usr/bin/env python3
"""Install and inspect agent-kit's non-overwriting workflow payload."""

from dataclasses import dataclass
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import sys


SOURCE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SOURCE_ROOT / "distribution/manifest.json"
RECEIPT_PATH = Path(".agents/kit-install.json")
RECEIPT_VERSION = 1
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


class ReceiptError(ValueError):
    """An install receipt is malformed or unsafe to inspect."""


@dataclass(frozen=True)
class PayloadFile:
    source: Path
    destination: Path
    group: str = "core"
    user_owned: bool = False


@dataclass(frozen=True)
class DistributionManifest:
    version: int
    sha256: str
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
        raw_manifest = manifest_path.read_bytes()
        manifest = json.loads(raw_manifest.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
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
            if destination == RECEIPT_PATH:
                raise ManifestError(
                    f"{label} destination is reserved for the install receipt"
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

    return DistributionManifest(
        version=manifest["version"],
        sha256=hashlib.sha256(raw_manifest).hexdigest(),
        groups=groups,
    )


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
    destinations = [entry.destination for entry in planned]
    if len(destinations) != len(set(destinations)):
        raise ManifestError("rendered payload contains duplicate destinations")
    return tuple(planned)


def _normalized_groups(manifest, groups):
    normalized = tuple(dict.fromkeys(groups))
    if not normalized or normalized[0] != "core":
        raise ManifestError("selected groups must begin with core")
    select_payload(manifest, normalized)
    return normalized


def _utc_timestamp():
    return (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )


def _sha256(content):
    return hashlib.sha256(content).hexdigest()


def _receipt_content(manifest, plan, groups, slug, installed_at):
    immutable_files = {
        entry.destination.as_posix(): _sha256(entry.content)
        for entry in plan
        if not entry.user_owned
    }
    user_owned_templates = sorted(
        entry.destination.as_posix() for entry in plan if entry.user_owned
    )
    receipt = {
        "receipt_version": RECEIPT_VERSION,
        "manifest": {
            "version": manifest.version,
            "sha256": manifest.sha256,
        },
        "config": {
            "slug": slug,
            "prefix": f"{slug}-" if slug is not None else "",
            "groups": list(groups),
        },
        "installed_at": installed_at,
        "immutable_files": dict(sorted(immutable_files.items())),
        "user_owned_templates": user_owned_templates,
    }
    return (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_install_plan(manifest, groups=("core",), slug=None, installed_at=None):
    """Render selected files and append the generated ownership receipt."""

    normalized_groups = _normalized_groups(manifest, groups)
    payload = select_payload(manifest, normalized_groups)
    rendered = render_payload(payload, slug)
    receipt = PlannedFile(
        source=None,
        destination=RECEIPT_PATH,
        content=_receipt_content(
            manifest,
            rendered,
            normalized_groups,
            slug,
            installed_at or _utc_timestamp(),
        ),
    )
    return (*rendered, receipt)


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


def _plan_kind(entry):
    if entry.destination == RECEIPT_PATH:
        return "receipt"
    if entry.user_owned:
        return "user-template"
    return "immutable"


def format_preflight(plan, collisions):
    """Return a deterministic, relative-path-only preflight report."""

    lines = [f"Write plan ({len(plan)} files):"]
    lines.extend(
        f"  - {_plan_kind(entry)}: {entry.destination.as_posix()}" for entry in plan
    )
    lines.append("Collision report:")
    if collisions:
        lines.extend(f"  - {collision.as_posix()}" for collision in collisions)
    else:
        lines.append("  - none")
    return "\n".join(lines)


def _receipt_path(value, field):
    try:
        path = _relative_path(value, field)
    except ManifestError as error:
        raise ReceiptError(str(error)) from error
    if path.parts[0] == ".git" or path == RECEIPT_PATH:
        raise ReceiptError(f"{field} is reserved or unsafe: {path}")
    return path


def _validate_receipt(document):
    required = {
        "receipt_version",
        "manifest",
        "config",
        "installed_at",
        "immutable_files",
        "user_owned_templates",
    }
    if not isinstance(document, dict) or set(document) != required:
        raise ReceiptError(
            "receipt must contain receipt_version, manifest, config, "
            "installed_at, immutable_files, and user_owned_templates"
        )
    if (
        type(document["receipt_version"]) is not int
        or document["receipt_version"] != RECEIPT_VERSION
    ):
        raise ReceiptError(f"receipt_version must be {RECEIPT_VERSION}")

    manifest = document["manifest"]
    if not isinstance(manifest, dict) or set(manifest) != {"version", "sha256"}:
        raise ReceiptError("receipt manifest must contain version and sha256")
    if type(manifest["version"]) is not int or manifest["version"] != 2:
        raise ReceiptError("receipt manifest version must be 2")
    if not isinstance(manifest["sha256"], str) or not re.fullmatch(
        r"[0-9a-f]{64}", manifest["sha256"]
    ):
        raise ReceiptError("receipt manifest sha256 must be lowercase hexadecimal")

    config = document["config"]
    if not isinstance(config, dict) or set(config) != {"slug", "prefix", "groups"}:
        raise ReceiptError("receipt config must contain slug, prefix, and groups")
    slug = config["slug"]
    if slug is not None:
        try:
            validate_slug(slug)
        except ValueError as error:
            raise ReceiptError(f"receipt config has invalid slug: {error}") from error
    expected_prefix = f"{slug}-" if slug is not None else ""
    if config["prefix"] != expected_prefix:
        raise ReceiptError("receipt config prefix does not match slug")
    groups = config["groups"]
    if (
        not isinstance(groups, list)
        or not groups
        or any(
            not isinstance(group, str) or not GROUP_PATTERN.fullmatch(group)
            for group in groups
        )
        or len(groups) != len(set(groups))
        or groups[0] != "core"
    ):
        raise ReceiptError(
            "receipt config groups must be unique valid names beginning with core"
        )

    installed_at = document["installed_at"]
    if not isinstance(installed_at, str):
        raise ReceiptError("receipt installed_at must be an ISO-8601 string")
    try:
        timestamp = datetime.fromisoformat(installed_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ReceiptError("receipt installed_at must be an ISO-8601 string") from error
    if timestamp.tzinfo is None:
        raise ReceiptError("receipt installed_at must include a timezone")

    immutable = document["immutable_files"]
    if not isinstance(immutable, dict) or not immutable:
        raise ReceiptError("receipt immutable_files must be a nonempty object")
    immutable_paths = set()
    for value, digest in immutable.items():
        path = _receipt_path(value, "immutable file path")
        if path in immutable_paths:
            raise ReceiptError(f"duplicate immutable file path: {path}")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ReceiptError(f"invalid sha256 for immutable file: {path}")
        immutable_paths.add(path)

    templates = document["user_owned_templates"]
    if not isinstance(templates, list):
        raise ReceiptError("receipt user_owned_templates must be a list")
    template_paths = []
    for value in templates:
        path = _receipt_path(value, "user-owned template path")
        if path in template_paths:
            raise ReceiptError(f"duplicate user-owned template path: {path}")
        if path in immutable_paths:
            raise ReceiptError(f"receipt path has conflicting ownership: {path}")
        template_paths.append(path)
    return document


def _has_blocking_ancestor(target, relative):
    current = target
    for part in relative.parts[:-1]:
        current /= part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            return True
    return False


def load_receipt(target):
    """Load a regular-file receipt, returning None when it is absent."""

    path = target / RECEIPT_PATH
    if _has_blocking_ancestor(target, RECEIPT_PATH):
        raise ReceiptError(f"install receipt has an unsafe ancestor: {RECEIPT_PATH}")
    if not path.exists() and not path.is_symlink():
        return None
    if path.is_symlink() or not path.is_file():
        raise ReceiptError(f"install receipt must be a regular file: {RECEIPT_PATH}")
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReceiptError(f"cannot read install receipt: {error}") from error
    return _validate_receipt(document)


def _immutable_status(target, relative, expected_digest):
    if _has_blocking_ancestor(target, relative):
        return "MODIFIED"
    path = target / relative
    if not path.exists() and not path.is_symlink():
        return "MISSING"
    if path.is_symlink() or not path.is_file():
        return "MODIFIED"
    try:
        actual_digest = _sha256(path.read_bytes())
    except OSError:
        return "MODIFIED"
    return "OK" if actual_digest == expected_digest else "MODIFIED"


def _is_present(path):
    return path.exists() or path.is_symlink()


def doctor_from_receipt(target, receipt):
    """Print receipt-backed integrity and presence results; return finding count."""

    findings = 0
    ok_count = 0
    modified_count = 0
    missing_count = 0
    print("Receipt: PRESENT")
    config = receipt["config"]
    slug = config["slug"] if config["slug"] is not None else "none"
    print(
        "Configuration: "
        f"slug={slug}; prefix={config['prefix'] or 'none'}; "
        f"groups={','.join(config['groups'])}"
    )
    print("Immutable payload:")
    for relative, expected_digest in receipt["immutable_files"].items():
        status = _immutable_status(target, Path(relative), expected_digest)
        print(f"  {status} {relative}")
        if status == "OK":
            ok_count += 1
        elif status == "MODIFIED":
            modified_count += 1
            findings += 1
        else:
            missing_count += 1
            findings += 1

    present_templates = 0
    missing_templates = 0
    print("User-owned templates:")
    for relative in receipt["user_owned_templates"]:
        status = "PRESENT" if _is_present(target / Path(relative)) else "MISSING"
        print(f"  {status} {relative}")
        if status == "PRESENT":
            present_templates += 1
        else:
            missing_templates += 1
            findings += 1

    print(
        "Summary: "
        f"{ok_count} OK, {modified_count} MODIFIED, {missing_count} MISSING; "
        f"{present_templates} templates PRESENT, "
        f"{missing_templates} templates MISSING"
    )
    return findings


def _fallback_skill_path(target, destination):
    token = _skill_token(destination)
    if token is None:
        return destination if _is_present(target / destination) else None

    if _is_present(target / destination):
        return destination
    skill_root = target / ".agents/skills"
    if not skill_root.is_dir() or skill_root.is_symlink():
        return None
    for candidate in sorted(skill_root.glob(f"*-{token}/SKILL.md")):
        directory_name = candidate.parent.name
        slug = directory_name[: -(len(token) + 1)]
        try:
            validate_slug(slug)
        except ValueError:
            continue
        if _is_present(candidate):
            return candidate.relative_to(target)
    return None


def doctor_without_receipt(target, manifest):
    """Print bounded core presence checks when install configuration is unknown."""

    print("Receipt: MISSING (install configuration unknown)")
    print("Fallback core presence checks:")
    for entry in select_payload(manifest):
        actual = _fallback_skill_path(target, entry.destination)
        if actual is None:
            print(f"  MISSING {entry.destination.as_posix()}")
        elif actual == entry.destination:
            print(f"  PRESENT {entry.destination.as_posix()}")
        else:
            print(f"  PRESENT {actual.as_posix()} (for {entry.destination.as_posix()})")
    print("Summary: receipt missing; integrity and selected profiles are unknown")


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
    install.add_argument(
        "--dry-run",
        action="store_true",
        help="print the complete plan and collision report without writing",
    )
    doctor = commands.add_parser(
        "doctor",
        help="inspect an installation without changing the target",
    )
    doctor.add_argument("target", type=Path, help="existing target repository")
    return parser


def _validated_target(target):
    try:
        resolved = target.resolve()
    except (OSError, RuntimeError) as error:
        raise ValueError(
            f"Target cannot be resolved safely: {target}: {error}"
        ) from error
    if not resolved.is_dir():
        raise ValueError(f"Target must be an existing directory: {target}")
    return resolved


def _run_install(arguments):
    try:
        slug = validate_slug(arguments.slug) if arguments.slug is not None else None
        manifest = load_manifest()
        plan = build_install_plan(
            manifest,
            _selected_groups(arguments.profile),
            slug,
        )
        target = _validated_target(arguments.target)
    except (ManifestError, ValueError) as error:
        print(f"Agent workflow configuration is invalid: {error}", file=sys.stderr)
        return 2

    collisions = find_collisions(target, plan)
    if arguments.dry_run:
        print(format_preflight(plan, collisions))
        return 1 if collisions else 0

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

    print(
        f"Installed {len(plan) - 1} agent workflow payload files "
        f"and receipt into {target}."
    )
    return 0


def _run_doctor(arguments):
    try:
        target = _validated_target(arguments.target)
        receipt = load_receipt(target)
        if receipt is None:
            manifest = load_manifest()
    except (ManifestError, ReceiptError, ValueError) as error:
        print(f"Agent workflow doctor cannot inspect target: {error}", file=sys.stderr)
        return 2

    if receipt is None:
        doctor_without_receipt(target, manifest)
        return 1
    return 1 if doctor_from_receipt(target, receipt) else 0


def main(argv=None):
    arguments = _build_parser().parse_args(argv)
    if arguments.command == "install":
        return _run_install(arguments)
    if arguments.command == "doctor":
        return _run_doctor(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")


if __name__ == "__main__":
    sys.exit(main())
