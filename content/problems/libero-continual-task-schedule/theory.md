# Build a Continual-Learning Task Sequence

## Intuition

A continual-learning experiment is defined partly by its task order and demonstration budget. Record the exact selected demonstrations and evaluation seeds before training so a later result can be attributed to the same protocol.

## Mathematics and physical contract

Let $\pi=(\pi_1,\ldots,\pi_K)$ be a permutation of $K$ task identities, and $D_j$ the set of available demonstration IDs for task $j$. For per-task budget $b$, define $S_j$ as the first $\min(b,|D_j|)$ elements of sorted $D_j$. After stage $i$, cumulative new demonstration count is
$$C_i=\sum_{h=1}^{i}|S_{\pi_h}|.$$
Counts and IDs are dimensionless; IDs identify immutable trajectories, not timestamps. Demonstration sets are disjoint across tasks. Evaluation seed IDs may recur because the same randomization identifier can be used under different task definitions. This deliberately simple selection policy is reproducible, not an optimized curriculum.

## Worked pipeline and shape trace

```text
available a:[3,1], b:[9]; order[b,a]; budget1
stage1 b -> demos[9], evaluation seeds[1,2], cumulative1
stage2 a -> demos[1], evaluation seeds[8], cumulative2
future task demonstrations do not appear in an earlier stage
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Changing task order or silently using more demonstrations can create an apparent learning improvement. This schedule does not certify that the named trajectories were collected independently or that a seed recreates a simulator state across versions.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
