---
name: experiment-design
description: Design, execute, and interpret falsifiable and reproducible experiments with baselines, controls, metrics, and decision rules.
---

# Experiment Design

Use whenever a repository decision depends on empirical evidence.

## Required elements

Every experiment must define:

- hypothesis,
- baseline,
- independent variables,
- controlled variables,
- datasets or inputs,
- metrics,
- expected outcomes,
- falsification condition,
- reproduction command,
- decision rule.

## Design principles

- Test the mechanism, not only the final metric.
- Prefer the cheapest experiment that resolves the uncertainty.
- Start with synthetic or analytically tractable cases when possible.
- Include at least one strong baseline.
- Separate tuning data from evaluation data.
- Save machine-readable raw outputs.
- Record environment, versions, seeds, and hardware when relevant.
- Preserve negative results that prevent repeated dead ends.

## Artifact

Create `docs/experiments/<experiment>.md`:

```markdown
# Experiment: <name>

## Hypothesis
## Baseline
## Independent Variables
## Controlled Variables
## Metrics
## Datasets or Inputs
## Procedure
## Expected Outcomes
## Falsification Condition
## Reproduction Command

## Results
### Raw Outputs
### Summary
### Comparison to Baseline
### Unexpected Observations
### Limitations
### Interpretation
### Decision
```

Place raw data under `experiments/results/` if that directory exists.

## Reviewer obligations

The Reviewer checks:

- whether the experiment isolates the claim,
- whether baselines are fair,
- whether metrics can hide failure,
- whether parameters were selected fairly,
- whether the result is reproducible,
- whether conclusions exceed the evidence.

A result may be accepted, rejected, refined, repeated, or inconclusive.
