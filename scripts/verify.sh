#!/bin/sh
# POSIX verification entry point for agent-kit. Windows is not supported.

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir/.."

if ! command -v ruff >/dev/null 2>&1; then
    echo "verify: Ruff is required; run: python3 -m pip install -r requirements-dev.txt" >&2
    exit 2
fi

echo "[1/5] Ruff lint"
ruff check .

echo "[2/5] Ruff format"
ruff format --check .

echo "[3/5] Workflow structure"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_agent_workflow.py

echo "[4/5] ARA claim ledger"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_ara.py

echo "[5/5] Regression tests"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
