---
name: novel-idea-generation
description: Generate, challenge, and rank novel methods, algorithms, and product ideas using failure analysis, structural transformations, and cross-field transfer.
---

# Novel Idea Generation

Use when the repository needs new methods rather than only known solutions.

## Inputs

Gather:

- demonstrated failure modes,
- expensive or unstable steps,
- discarded information,
- mismatches between theory and implementation,
- hardware or data constraints,
- assumptions made by current methods,
- relevant research notes.

## Idea operators

Apply several of these deliberately:

- remove or weaken an assumption,
- invert the problem,
- formulate the dual,
- replace discrete with continuous or the reverse,
- replace global with local or the reverse,
- replace deterministic with stochastic or the reverse,
- move computation offline or online,
- preserve information currently discarded,
- turn a heuristic into an objective or constraint,
- replace learned components with analytic ones or the reverse,
- exploit modern hardware characteristics,
- separate representation from optimization,
- use uncertainty or confidence explicitly,
- construct a cheap approximation with a refinement path.

## Cross-field transfer

For the problem structure, ask:

- Which other fields solve an analogous problem?
- What terminology do they use?
- Which assumptions differ?
- Which mechanism transfers directly?
- Which part requires adaptation?
- Why might the transfer not have been tried?

Possible fields include geometry processing, graphics, robotics, control,
signal processing, statistical physics, information theory, optimization,
databases, distributed systems, computational biology, and numerical analysis.

## Novelty discipline

Do not claim novelty until `research-methods` has checked:

- terminology variants,
- adjacent fields,
- recent related work,
- known implementations.

Classify each idea as:

- new,
- transferred,
- combined,
- simplified,
- independently rediscovered,
- unclear.

## Cheapest falsification

Every serious idea must state the smallest test that could invalidate it.

## Ranking

Rank qualitatively by:

```text
priority =
information gain
× potential impact
× plausibility
÷ implementation cost
```

## Artifact

Record serious ideas in `.agents/state/ideas.md` using the template that file
provides.

Select no more than a small number of ideas for active testing.
