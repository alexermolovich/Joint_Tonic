# Sample a Progressive-Shrinking Curriculum

## Intuition

Sampling the smallest configurations immediately can change shared-weight training. A staged curriculum gradually makes more architecture choices eligible while keeping the selection reproducible.

## Eligibility before randomness

Let D,W,K be decreasing depth, width and kernel lists. At phase p, legal sets are D_p=D if p>=3 else its first entry; W_p=W if p>=2; K_p=K if p>=1. For independent fractions u_j in[0,1), select

$$a_j=A_{p,j}[\lfloor u_j|A_{p,j}|\rfloor].$$

The tuple axes j=0,1,2 mean depth,width,kernel. Drawing a fixed count×3 matrix makes the random-number consumption explicit even for a singleton axis. NumPy2.2.4 PCG64 is the pinned stream, and no global random state is read or changed.

## Visual: expanding eligible architectures

| Phase | Depths | Widths | Kernels |
|---:|---|---|---|
| 0 | largest | largest | largest |
| 1 | largest | largest | all |
| 2 | largest | all | all |
| 3 | all | all | all |

This original eligibility diagram is also the text alternative. It specifies this teaching schedule, not a full training recipe.

## Why this matters on a robot

A reproducible architecture distribution supports comparisons across edge budgets. A failure mode is sampling a width early that the declared training phase has not enabled. Architecture sampling alone says nothing about trained quality; extracted models still require calibration and evaluation.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
