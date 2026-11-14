# Compute a Forward and Backward Transfer Matrix

## Intuition

Transfer compares evaluations taken at meaningful points in a learning sequence. A task can improve before it is trained, degrade after it was learned, or retain its best observed performance. Keep these effects separate and expose incomplete history.

## Mathematics and physical contract

Let $R\in[0,1]^{(K+1)\times K}$ contain success rates and $M$ its Boolean observation mask. Task $j$ is learned at stage $j+1$, using zero-based task indices. For supported comparisons define
$$F_j=R_{j,j}-R_{0,j}\quad(j\ge1),\qquad B_j=R_{K,j}-R_{j+1,j}\quad(j<K-1).$$
Forward transfer $F_j$ compares pre-training performance to the initial policy. Backward transfer $B_j$ compares final performance to immediate acquisition. Forgetting is
$$G_j=\max_{i=j+1,\ldots,K}R_{i,j}-R_{K,j}\quad(j<K-1).$$
Require every post-learning stage in that maximum to be observed. Including the final stage makes $G_j\ge0$. All differences are dimensionless success-rate differences. Inapplicable or incomplete entries are NaN; each aggregate averages only supported entries. This explicitly chosen protocol is not asserted to match every LIBERO metric variant.

## Worked pipeline and shape trace

```text
stages: initial [.1,.2] -> after task0 [.8,.4] -> final [.6,.9]
forward task1=.4-.2=.2
backward task0=.6-.8=-.2; forgetting task0=max(.8,.6)-.6=.2
final mean=(.6+.9)/2=.75; other transfer entries are NaN
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

A robot may gain a new manipulation skill while losing an old one. Reporting only final mean success hides that regression. A missing intermediate stage also prevents claiming that the largest forgetting event was measured.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
