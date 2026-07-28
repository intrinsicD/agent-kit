# Repository State

## Project Objective

Provide a lightweight, skill-based operating system for repositories developed
by two collaborating agents, with durable task state, sequential
Driver/Reviewer handoffs, independent falsification, and reproducible evidence.

## Working System

- Ten reusable skills are present and match the routing in `AGENTS.md`.
- The repository includes task/state templates, durable documentation
  locations, a worked example, and an installation/state validator.
- The baseline validator runs successfully on the current repository.

## Experimental Components

- The full branch lifecycle has not been validated end to end.
- Operating-state enforcement is incomplete and must not be treated as a
  concurrency or approval lock.

## Known Failures

The independently reviewed
[workflow audit](../../docs/audits/agent-workflow-audit.md) records six
demonstrated failures:

- the installation command copies `.git/` into an existing target;
- documented Handoff Log headings conflict with the validator;
- invalid approval and turn states pass validation;
- rejected branch closeout has no documented safe path;
- partial and malformed archived state can bypass validation; and
- the illustrative task is treated as operational history.

## Important Decisions

None recorded.

## Current Metrics

- Routed skills: 10.
- Independently reproduced protocol/validator mismatches: 11 of 11 tested.
- Audit findings: 1 Critical, 3 High, 2 Medium.
- Independent audit verdict: Accepted with follow-up.

## Immediate Next Step

Replace the destructive installation command before recommending or
distributing the kit.

## Last Completed Task

- Task ID: 001
- Driver: codex-a
- Reviewer: codex-b
