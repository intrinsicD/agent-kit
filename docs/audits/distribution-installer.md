# Audit: Distribution Installer

## Scope

Self-audit of the Task 004 fixed distribution manifest, blank templates,
installer, documentation, and regressions before independent review.
Quantitative and performance concerns are not applicable.

## Findings

- The manifest is the only payload authority and names 22 fixed
  source/destination pairs. Its regression locks the complete mapping.
- Live operational state, historical records, ARA, source tests, the source
  README, and the installer itself are outside the target payload.
- Manifest paths are validated as relative, `.git` destinations and duplicate
  destinations are rejected, and payload sources must resolve to regular files
  inside agent-kit.
- Preflight gathers every exact destination and every file or symlink ancestor
  that blocks a destination. Installation starts only when that complete set is
  empty.
- Exclusive file creation prevents replacement after preflight. An injected
  copy failure confirms that only installer-created files and directories are
  rolled back while prior target content remains unchanged.
- The implementation has one direct command, uses only the Python standard
  library, and adds no configurable plugin, overwrite, update, or uninstall
  layer.
- The optional `results-audit` procedure is routed from the repository
  authority and task/experiment skills. Repository-specific audit rules remain
  explicitly local.

## Severity

No open critical, high, or medium findings. During self-audit, directory
creation tracking was tightened so a mid-copy failure cannot leave successfully
created parent directories behind; the failure path now has a regression.

## Evidence

All Python checks below used `PYTHONDONTWRITEBYTECODE=1`.

- `python3 tests/test_distribution.py -v`: 6 tests passed.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`: 36 tests passed.
- `python3 scripts/validate_agent_workflow.py`: 11 routed skills and 3 task
  archives validated.
- `ruff check scripts/install_agent_workflow.py
  scripts/validate_agent_workflow.py tests/test_distribution.py
  tests/test_agent_workflow.py`: all four changed Python paths passed lint.
- `ruff format --check scripts/install_agent_workflow.py
  tests/test_distribution.py`: both Task 004 Python files passed format
  validation.
- `ruff format --check scripts/validate_agent_workflow.py
  tests/test_agent_workflow.py`: both legacy files are reported as requiring
  formatting. The result is identical at setup commit `0a66c6f` and
  implementation commit `92148b4`; Task 004 did not introduce that formatting
  debt, and these unrelated files were not reformatted.
- `git diff --check` passed.

## Required Fixes

None identified by the Driver self-audit.

## Optional Improvements

None recommended within Task 004's fixed, non-overwriting install scope.

## Residual Risks

- Preflight assumes no concurrent process rewrites target paths. Exact files
  still use exclusive creation, but the installer is not an adversarial
  filesystem transaction.
- An uncatchable process termination can leave newly created payload paths.
  Existing target files remain protected, and a subsequent run reports those
  paths as collisions rather than overwriting them.
- This is a Driver self-audit and cannot supply the required independent
  acceptance verdict.

## Verdict

The implementation is ready for independent Reviewer falsification; it is not
yet accepted.
