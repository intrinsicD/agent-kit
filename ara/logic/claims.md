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

## C07: The accepted remediation closes all six audit findings
- **Statement**: At remediation completion commit `f198163`, all six findings
  from task 001 have committed fixes, task 002 has an independent `Accepted`
  verdict, all 31 workflow regression tests pass, and the repository validator
  accepts the active and archived task state.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: Reproduce any original audit failure at
  `f198163`, fail a committed workflow regression test there, or show that
  task 002 lacks an independent accepting verdict.
- **Proof**: [docs/audits/agent-workflow-audit.md, docs/tasks/002-fix-workflow-audit-findings.md, tests/test_agent_workflow.py, scripts/validate_agent_workflow.py]
- **Dependencies**: [C01, C02, C03, C04, C05, C06]
- **Tags**: remediation, independent-review, regression-tests
- **From staging**: O07

## C08: The tracked-tree installer is not a clean distribution boundary
- **Statement**: At agent-kit source
  `d8d649512f454c219dba55dd12f4d0398cb742e9`, the documented tracked-tree
  installer has 11 filesystem collisions with Prospect, 12 with StructSplat,
  11 with realtime-gs, and 12 with IntrinsicEngine at their inspected commits;
  its non-colliding payload also includes agent-kit's active state, completed
  tasks, audit, workflow test, and dated ARA history.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: The assessment's fixed-source commands fail to
  reproduce any stated collision count or show that the actual archive
  excludes all stated non-colliding history paths.
- **Proof**: [docs/research/cross-repository-agent-workflow-adoption.md, docs/tasks/003-cross-repository-agent-workflow-adoption.md]
- **Dependencies**: [C07]
- **Tags**: installation, distribution, collisions, history-contamination
- **From staging**: O08

## C09: Review practice exceeds target identity enforcement
- **Statement**: At the inspected commits, Prospect, StructSplat, realtime-gs,
  and IntrinsicEngine each contain a review norm and recorded independent or
  non-author review practice, but none has a general task validator that
  requires distinct proposer/reviewer labels together with valid terminal
  verdict state.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: Any inspected target lacks the recorded practice
  cited in the assessment, or a general target task validator at the inspected
  commit rejects equal proposer/reviewer labels and invalid terminal verdict
  state.
- **Proof**: [docs/research/cross-repository-agent-workflow-adoption.md, docs/tasks/003-cross-repository-agent-workflow-adoption.md]
- **Dependencies**: []
- **Tags**: independent-review, identity, validation, cross-repository
- **From staging**: O09

## C10: Three targets share stronger results-audit invariants
- **Statement**: At the inspected commits, Prospect, StructSplat, and
  realtime-gs each require a results-audit pattern covering claim disposition,
  raw recomputation, exact source/config binding, controls or accounting, and
  evidence scope; agent-kit's generic experiment-design and
  review-and-falsification skills do not require that complete result-audit
  structure.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: Fewer than three inspected target audit skills
  contain the stated common structure, or agent-kit's inspected generic skill
  pair already requires the complete structure.
- **Proof**: [docs/research/cross-repository-agent-workflow-adoption.md, docs/tasks/003-cross-repository-agent-workflow-adoption.md]
- **Dependencies**: []
- **Tags**: results-audit, evidence, reciprocal-integration
- **From staging**: O10

## C11: Task 004 implements a fixed clean distribution boundary
- **Statement**: At implementation commit `92148b4`, the installer copies only
  the manifest's 22 files into a fresh target; that target validates with 11
  skills and no task archives, retains its pre-existing Git HEAD, branch, and
  remote, and exact or blocking-ancestor collision fixtures exit nonzero
  without changing the target.
- **Status**: testing
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: Reproduce an undeclared installed file, leaked
  live/history artifact, overwritten collision, changed tested Git metadata,
  invalid fresh target, or failure to report all fixture collisions at
  `92148b4`.
- **Proof**: [tests/test_distribution.py, docs/audits/distribution-installer.md, 92148b4c19b84614301c03ff77b736de54cb65d7]
- **Dependencies**: [C08]
- **Tags**: installation, distribution, collisions, regression-tests
- **From staging**: O11

## C12: Task 004 adds the bounded generic results-audit procedure
- **Statement**: At implementation commit `92148b4`, agent-kit routes an
  optional `results-audit` skill that requires exact claim inventory, raw
  recomputation, source/config binding, controls and accounting checks,
  evidence-boundary classification, and explicit claim dispositions while
  leaving domain-specific rules local.
- **Status**: testing
- **Provenance**: ai-suggested
- **Crystallized via**: artifact-commitment
- **Falsification criteria**: Any stated generic invariant is absent from the
  installed skill, the skill is not routed or optional, or repository-specific
  policy is imposed as generic core at `92148b4`.
- **Proof**: [.agents/skills/results-audit/SKILL.md, AGENTS.md, tests/test_distribution.py, 92148b4c19b84614301c03ff77b736de54cb65d7]
- **Dependencies**: [C10]
- **Tags**: results-audit, reciprocal-integration, evidence
- **From staging**: O12

## C13: Task 004 did not introduce the two legacy Ruff format failures
- **Statement**: Running `ruff format --check
  scripts/validate_agent_workflow.py tests/test_agent_workflow.py` in archived
  checkouts of Task 004 setup commit `0a66c6f` and implementation commit
  `92148b4` exits 1 identically, names those same two files, and reports that
  two files would be reformatted.
- **Status**: supported
- **Provenance**: ai-suggested
- **Crystallized via**: empirical-resolution
- **Falsification criteria**: The exact command has a different exit status,
  file list, or summary at either fixed commit.
- **Proof**: [docs/audits/distribution-installer.md, .agents/state/current-task.md, 0b1bd0ac1389db6b2790698996815aaafa7bf22b]
- **Dependencies**: []
- **Tags**: formatting, evidence-scope, regression-baseline
- **From staging**: O13
