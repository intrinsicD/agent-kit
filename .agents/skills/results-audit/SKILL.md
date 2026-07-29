---
name: results-audit
description: Independently audit quantitative or empirical results before promoting claims by recomputing raw evidence, checking provenance, controls, accounting, scope, and explicit dispositions.
---

# Results Audit

Use this optional research profile after an experiment or quantitative evidence
session and before promoting an empirical, causal, generality, capability,
retention, or performance claim. It complements `experiment-design` and the
task-level verdict from `review-and-falsification`; it does not replace either.

The audit should be performed by a Reviewer who did not produce the result when
the claim is substantial. A referee stance alone does not establish identity,
so record the reviewed commit and the Driver/Reviewer labels in the task
handoff.

## 1. Inventory exact claims

Build a table before interpreting the result:

| ID | Exact claim | Evidence class and scope | Raw evidence | Source/data/config binding | Current disposition |
| --- | --- | --- | --- | --- | --- |

Include every quantitative, causal, generality, capability, retention, and
performance statement in the changed artifact and its public summaries. A
claim without an explicit scope or inspectable raw source is already a finding.

## 2. Bind provenance and execution

For every result, record and verify:

- reviewed commit, branch, and dirty/untracked source state;
- exact reproduction command and executed entry point;
- input, dataset, split, model, evaluator, and configuration identities;
- dependency versions, seeds, environment, and hardware when relevant; and
- hashes or another stable binding for result-bearing sources and artifacts.

If the run was dirty, preserve the exact executed diff or source snapshot.
Prose, remembered values, and a green unit test do not bind a numeric claim to
the code and data that produced it.

## 3. Recompute from raw evidence

Recompute the reported metrics and decision rule from raw rows, tensors, logs,
or persisted artifacts rather than copying the report. Verify:

- formulas, units, signs, denominators, and aggregation order;
- pairing, sample unit, missing/error rows, exclusions, and repeated runs;
- thresholds, intervals, effect sizes, and success counts; and
- agreement between machine-readable evidence and every prose/table summary.

If raw evidence is absent or cannot be reopened, narrow the claim to the
evidence that can actually be checked.

## 4. Audit chronology, isolation, and controls

Confirm the hypothesis, primary metric, baseline, inputs/splits, budgets,
stopping rule, falsification rule, and decision threshold were fixed before
the evaluated outcome was consumed. Check that:

- tuning and evaluation data are disjoint where the claim requires it;
- baselines and positive/negative controls exercise the intended mechanism;
- controls preserve relevant budgets, marginals, and code paths;
- no secondary metric rescues a failed primary rule; and
- no threshold, seed, arm, exclusion, or branch was retuned after the result.

Record exploratory or post-hoc work honestly instead of relabeling it as
confirmatory.

## 5. Audit accounting and statistics

Recompute the resource scope the claim names: samples, steps, evaluations,
calls, bytes, wall time, memory, or other budgets. Preserve paired structure
and do not count correlated rows, restarts, or repeated measurements as
independent samples.

Performance claims also require the execution mode, build, hardware,
synchronization, warmup, repeats, and aggregation rule. Uncontrolled or
contended timing is context, not comparative performance evidence.

## 6. Classify the evidence boundary

State exactly what ran and what did not. Keep these distinctions explicit:

- synthetic, fixture, development, held-out, or externally representative;
- structural validation, reference path, or exercised production path;
- CPU, accelerator, backend, and device coverage;
- in-process reload versus fresh-process restoration; and
- local mechanism evidence versus end-to-end capability or generality.

List unavailable or unopened evidence. Do not let a stronger neighboring test
silently widen the audited claim.

## 7. Dispose of every claim

Assign one disposition to every claim row:

- **confirm** — raw evidence, provenance, controls, and wording survive;
- **narrow** — rewrite to the endpoint and scope the evidence supports;
- **refute** — the frozen result contradicts the claim;
- **retire** — remove a claim that lacks usable support or is no longer valid;
- **unresolved** — name the missing evidence and cheapest decisive check.

Apply matching corrections to all claim surfaces in the same change. Preserve
negative, failed, and superseded evidence; do not overwrite history to make the
latest result appear clean.

## 8. Report

Store the durable audit under the repository's existing evidence authority, or
under `docs/audits/` when no more specific authority exists. Include:

- the claim table and final dispositions;
- reviewed source/data/config identities;
- commands run and independent recomputations;
- control, accounting, and statistical findings;
- corrections made to claim surfaces;
- unopened or unavailable evidence and why;
- explicit limitations and follow-up checks; and
- a one-sentence verdict stating only what the result establishes.

Domain-specific requirements remain local extensions. Complete-stream rate
accounting, protected experiment custody, calibrated viewer receipts, or
checkpoint semantics are examples, not generic core rules.

## Hard prohibitions

- Tune the protocol after seeing the evaluated outcome.
- Treat a report renderer, schema check, or test written by the producing
  session as independent semantic recomputation.
- Promote development, fixture, structural, or reference-only evidence into a
  broader capability claim.
- Delete failed/missing rows or let a secondary endpoint rescue a failed
  primary decision.
- Report remembered numbers without reopening their raw source.
