# Validated Backlog

Only add work that has evidence, a clear motivation, or an accepted dependency.

- [x] Installer v2: slug prefixing, dry-run, doctor, and manifest groups
  - Motivation: Multi-repository sessions expose unprefixed skill-name
    collisions, while the current installer cannot preview or diagnose an
    installation.
  - Priority: High
  - Dependencies: Verification foundation (accepted task 006)
  - Evidence: `docs/research/maturity-program-plan.md` plan 006;
    independently accepted as `docs/tasks/007-installer-v2.md`
  - Suggested skills: `task-orchestration`, `implementation`, `code-audit`,
    `handoff`, `repo-organization`
- [ ] Generic validator pack and target CI template
  - Motivation: Fresh targets receive structural validation but no single gate
    command or CI wiring.
  - Priority: High
  - Dependencies: Installer v2
  - Evidence: `docs/research/maturity-program-plan.md` plan 007
  - Suggested skills: `task-orchestration`, `implementation`, `code-audit`,
    `handoff`, `repo-organization`
- [ ] Task-tree profile
  - Motivation: A one-file backlog stops scaling once a target accumulates
    multiple workstreams, but active-task authority must remain singular.
  - Priority: Medium
  - Dependencies: Installer v2
  - Evidence: `docs/research/maturity-program-plan.md` plan 008
  - Suggested skills: `task-orchestration`, `repo-organization`,
    `implementation`, `review-and-falsification`, `handoff`
- [ ] Evidence profile and skill-text hardening
  - Motivation: Targets cannot install a blank checked claim ledger, and three
    generic epistemic rules observed across sibling repositories are absent.
  - Priority: Medium
  - Dependencies: Installer v2
  - Evidence: `docs/research/maturity-program-plan.md` plan 009
  - Suggested skills: `task-orchestration`, `implementation`, `results-audit`,
    `handoff`, `repo-organization`
- [ ] Growth loop and process-audit skill
  - Motivation: Installed workflows need a bounded way to turn recurring
    failures into executable memory and retire checks that stop earning rent.
  - Priority: Medium
  - Dependencies: Installer v2, generic validator pack, evidence profile
  - Evidence: `docs/research/maturity-program-plan.md` plan 010
  - Suggested skills: `task-orchestration`, `implementation`,
    `review-and-falsification`, `handoff`, `repo-organization`
