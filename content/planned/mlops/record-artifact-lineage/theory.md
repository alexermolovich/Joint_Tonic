# Record Dataset, Transform, Model, and Evaluator Lineage

## Intuition

A score without the evaluated model, transform and data identities is hard to reproduce. A lineage record answers which declared ingredients contributed to a target artifact. It traverses upstream inputs, the opposite direction from a change-impact query.

## Ancestor closure

Let P(v) be the set of direct parent IDs consumed by artifact v. Starting from target q, build

$$
A_0=\{q\},\qquad
A_{k+1}=A_k\cup\bigcup_{v\in A_k}P(v).
$$

The graph is finite, so the sequence reaches a fixed point A. Each ID in A contributes one row containing its declared kind and digest. Acyclicity is a separate validation rule: the closure could terminate with a visited set on a cycle, but such a graph does not describe an allowed immutable production history here.

A digest identifies supplied content; an artifact ID identifies a metadata entity. Two acquisitions may have equal bytes and different provenance. Therefore this task deduplicates IDs, never hashes.

## Visual: direction of provenance

| Consumer | Direct parents | Contribution to score ancestry |
|---|---|---|
| score | policy, data | Start with score, then add both |
| policy | data, norm | Add norm; data already present |
| norm | data | No new ID |
| data | none | Stop |

This table is the static dependency trace and text alternative. Reading parents gives score → policy → norm → data, while production influence runs in the reverse direction. Final output is sorted by ID for reproducible comparison.

## Why this matters on a robot

A policy may be evaluated with one normalization or calibration version and deployed with another. Lineage helps reveal that mismatch when the relevant metadata edges exist. It cannot recover an omitted dependency, prove a digest truthful, or determine that an artifact is licensed. The next verification stage checks actual bytes and runtime identities.

## Check your understanding

1. Why include target itself?
2. Why can two equal digests produce two rows?

## Sources and prerequisites

TFX motivates coordinating versioned pipeline artifacts. The graph schema and returned ancestry record are original teaching choices, not a universal TFX metadata API. Supplied digests are recorded but not verified against bytes in this component. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/), Section2.2: platform design and pipeline anatomy. Prerequisites: [training-pipeline-topological-order](/problems/training-pipeline-topological-order); no Python or mathematics tutorial is assumed.
