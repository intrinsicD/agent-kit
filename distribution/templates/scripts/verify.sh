#!/bin/sh
# POSIX verification entry point for the installed agent workflow.

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir/.."

echo "[1/4] Workflow structure"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py

echo "[2/4] Authority surfaces"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_authority.py --root . --strict

echo "[3/4] Documentation links"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_doc_links.py --root . --strict

echo "[4/4] Documentation sync"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_docs_sync.py --root .

# TODO: repository-specific gates
