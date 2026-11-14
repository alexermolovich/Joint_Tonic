# Compute a Masked Action Flow-Matching Loss

## Intuition

A flow model learns how to move a noisy action toward a demonstration. Under the declared noise-to-data path its target is the clean action minus noise; unsupported embodiment channels must contribute neither loss nor gradient.

## Mathematical mechanism

With A clean actions and E supplied noise, $$X_\tau=(1-\tau)E+\tau A,\quad U=A-E,\quad\mathcal L=\frac{\sum M(V-U)^2}{\sum M},\quad \frac{\partial\mathcal L}{\partial V}=\frac{2M(V-U)}{\sum M}.$$ Define loss and derivative as zero if the denominator vanishes. V,A,E share B,H,D; M is Boolean support. Flow time tau is dimensionless; target sign matches integration from noise toward data. Per-example losses use their own counts and are not equally averaged to obtain the global loss.

## Visual computation trace

| Entry | prediction V | target A-E | valid | squared error |
|---|---|---|---|---|
| 0 | 0 | 2 | yes | 4 |
| 1 | 9 | 5 | no | excluded |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

prediction=[[[0,9]]],clean=[[[3,7]]],noise=[[[1,2]]],valid=[[[True,False]]] gives target[2,5], loss4,per_example[4],gradient[[[-4,0]]].

## Why this matters on a robot

Aggregating incompatible robot channels or source types can hide a failing embodiment. Keep provenance, masks and per-slice results visible throughout training and evaluation.

## Physical contract and limits

Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Noise-to-data flow matching with an explicit support mask; this captures the GR00T action objective family, not DDPM noise prediction or the complete published training recipe.

Source: [primary paper](https://arxiv.org/abs/2503.14734). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.

## Source convention

[GR00T N1 v1, Section 2.1](https://arxiv.org/html/2503.14734v1#S2.SS1) prints the target noise-minus-action alongside a noise-to-data interpolation. This exercise explicitly chooses the derivative of its stated path, action-minus-noise. It therefore teaches a self-consistent flow objective and does not claim numeric compatibility with that printed target or with released weights.
