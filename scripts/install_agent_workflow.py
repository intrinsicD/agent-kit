#!/usr/bin/env python3
"""Install the fixed agent-workflow payload without overwriting target files."""

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
import shutil
import sys


SOURCE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SOURCE_ROOT / "distribution/manifest.json"


class ManifestError(ValueError):
    """The fixed distribution manifest is malformed or unsafe."""


@dataclass(frozen=True)
class PayloadFile:
    source: Path
    destination: Path


def _relative_path(value, field):
    if not isinstance(value, str) or not value:
        raise ManifestError(f"{field} must be a nonempty string")
    if "\\" in value:
        raise ManifestError(f"{field} must use forward slashes: {value!r}")

    parts = value.split("/")
    if value.startswith("/") or any(part in {"", ".", ".."} for part in parts):
        raise ManifestError(f"{field} must be a safe relative path: {value!r}")
    return Path(*parts)


def load_payload(source_root=SOURCE_ROOT, manifest_path=MANIFEST_PATH):
    """Load and validate the fixed source-to-destination payload."""

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ManifestError(f"cannot read {manifest_path}: {error}") from error

    if not isinstance(manifest, dict) or set(manifest) != {"version", "files"}:
        raise ManifestError("manifest must contain only `version` and `files`")
    if manifest["version"] != 1:
        raise ManifestError("manifest version must be 1")
    if not isinstance(manifest["files"], list) or not manifest["files"]:
        raise ManifestError("manifest files must be a nonempty list")

    root = source_root.resolve()
    destinations = set()
    payload = []
    for index, row in enumerate(manifest["files"]):
        if not isinstance(row, dict) or set(row) != {"source", "destination"}:
            raise ManifestError(
                f"manifest file {index} must contain source and destination"
            )

        source_relative = _relative_path(row["source"], f"file {index} source")
        destination = _relative_path(row["destination"], f"file {index} destination")
        if destination.parts[0] == ".git":
            raise ManifestError(
                f"file {index} destination may not enter .git: {destination}"
            )
        if destination in destinations:
            raise ManifestError(f"duplicate destination: {destination}")
        destinations.add(destination)

        source = source_root / source_relative
        if source.is_symlink() or not source.is_file():
            raise ManifestError(f"payload source must be a regular file: {source}")
        if not source.resolve().is_relative_to(root):
            raise ManifestError(f"payload source escapes repository: {source}")
        payload.append(PayloadFile(source=source, destination=destination))

    return tuple(payload)


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
    """Copy a preflighted payload and roll back files created on copy failure."""

    created_files = []
    created_directories = []
    try:
        for entry in payload:
            destination = target / entry.destination
            missing = _missing_directories(destination.parent, target)
            for directory in missing:
                directory.mkdir()
                created_directories.append(directory)

            with entry.source.open("rb") as source_stream:
                with destination.open("xb") as destination_stream:
                    created_files.append(destination)
                    shutil.copyfileobj(source_stream, destination_stream)
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Install agent-kit's fixed clean payload into an existing target "
            "directory. Existing paths are never overwritten."
        )
    )
    parser.add_argument("target", type=Path, help="existing target repository")
    arguments = parser.parse_args(argv)

    try:
        payload = load_payload()
    except ManifestError as error:
        print(f"Agent workflow manifest is invalid: {error}", file=sys.stderr)
        return 2

    target = arguments.target.resolve()
    if not target.is_dir():
        print(
            f"Target must be an existing directory: {arguments.target}",
            file=sys.stderr,
        )
        return 2

    collisions = find_collisions(target, payload)
    if collisions:
        print(
            "Agent workflow installation refused; protected paths exist:",
            file=sys.stderr,
        )
        for collision in collisions:
            print(f"  - {collision.as_posix()}", file=sys.stderr)
        return 3

    try:
        install_payload(target, payload)
    except OSError as error:
        print(f"Agent workflow installation failed: {error}", file=sys.stderr)
        return 4

    print(f"Installed {len(payload)} agent workflow files into {target}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
