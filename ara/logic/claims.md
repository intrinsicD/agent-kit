# Claims

## C01: Installation command overwrites target Git metadata
- **Statement**: Running the documented `cp -r agent-kit/. target-repository/`
  command against an existing Git repository copies the kit's `.git/` content
  and can replace the target's remote, active branch, and HEAD.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: A clean reproduction of the documented command
  preserves the destination's Git metadata or demonstrably excludes `.git/`.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: installation, git, destructive-copy
- **From staging**: O01

## C02: Documented review markup conflicts with validation
- **Statement**: The handoff and review skills' level-two `## Review` template
  is parsed outside the Handoff Log and causes an otherwise accepted task to
  fail validation.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: An accepted fixture using the exact documented
  level-two review template passes the current validator.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: handoff, markdown-schema, validator
- **From staging**: O02

## C03: Approval and turn invariants are not enforced
- **Statement**: The validator accepts protocol-invalid approval and turn
  states, including self-approved Accepted work, identical role labels, and
  review headings without a verdict.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: The current validator rejects every invalid
  approval and transition fixture recorded in the audit.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: state-machine, independent-review, validator
- **From staging**: O03

## C04: Rejected branches lack a documented safe closeout path
- **Statement**: When a task branch contains rejected changes, the documented
  workflow provides no safe path that both preserves the rejection archive on
  the default branch and avoids merging the rejected implementation.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: A documented, reproducible sequence archives the
  rejected task on the default branch without transferring rejected changes.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: git, rejected-task, lifecycle
- **From staging**: O04

## C05: Partial and malformed state can bypass validation
- **Statement**: A blank-title active task with invalid populated fields and a
  filename-valid but structurally malformed archive both pass the current
  validator.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: The current validator rejects both reproduced
  malformed-state fixtures.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: state-integrity, archives, validator
- **From staging**: O05

## C06: The illustrative task is treated as operational history
- **Statement**: On a fresh kit, role fallback and archive counting include
  `000-example-task.md` despite its explicit non-history designation.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: Fresh-install role fallback, archive counts, and
  task-id selection explicitly exclude the illustrative task.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/001-agent-workflow-audit.md]
- **Dependencies**: []
- **Tags**: role-assignment, example-data, task-history
- **From staging**: O06
