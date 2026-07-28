# Claims

## Scope and remediation

Claims C01-C06 describe the repository at audited baseline `ffbf949`. Task 002
remediated all six findings, received an independent `Accepted` verdict at
`c879ad7`, and was merged at `b444f6c`; see
`docs/tasks/002-fix-workflow-audit-findings.md`. A `supported` status below
means the historical baseline claim is supported, not that the defect remains
present.

## C01: Installation command overwrites target Git metadata
- **Statement**: At baseline `ffbf949`, running the then-documented
  `cp -r agent-kit/. target-repository/` command against an existing Git
  repository copied the kit's `.git/` content and could replace the target's
  remote, active branch, and HEAD.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: A clean reproduction from baseline `ffbf949`
  preserves the destination's Git metadata or demonstrably excludes `.git/`.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: installation, git, destructive-copy
- **From staging**: O01

## C02: Documented review markup conflicts with validation
- **Statement**: At baseline `ffbf949`, the handoff and review skills'
  level-two `## Review` template was parsed outside the Handoff Log and caused
  an otherwise accepted task to fail validation.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: An accepted fixture using the exact documented
  level-two review template passes the validator from baseline `ffbf949`.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: handoff, markdown-schema, validator
- **From staging**: O02

## C03: Approval and turn invariants are not enforced
- **Statement**: The validator at baseline `ffbf949` accepted protocol-invalid
  approval and turn states, including self-approved Accepted work, identical
  role labels, and review headings without a verdict.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: The validator at baseline `ffbf949` rejects every
  invalid approval and transition fixture recorded in the audit.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: state-machine, independent-review, validator
- **From staging**: O03

## C04: Rejected branches lack a documented safe closeout path
- **Statement**: At baseline `ffbf949`, when a task branch contained rejected
  changes, the documented workflow provided no safe path that both preserved
  the rejection archive on the default branch and avoided merging the rejected
  implementation.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: The workflow at baseline `ffbf949` documents a
  reproducible sequence that archives the rejected task on the default branch
  without transferring rejected changes.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: git, rejected-task, lifecycle
- **From staging**: O04

## C05: Partial and malformed state can bypass validation
- **Statement**: At baseline `ffbf949`, a blank-title active task with invalid
  populated fields and a filename-valid but structurally malformed archive
  both passed the validator.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: The validator at baseline `ffbf949` rejects both
  reproduced malformed-state fixtures.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: state-integrity, archives, validator
- **From staging**: O05

## C06: The illustrative task is treated as operational history
- **Statement**: On a fresh kit at baseline `ffbf949`, role fallback and
  archive counting included `000-example-task.md` despite its explicit
  non-history designation.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: At baseline `ffbf949`, fresh-install role
  fallback, archive counts, and task-id selection explicitly exclude the
  illustrative task.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: role-assignment, example-data, task-history
- **From staging**: O06
