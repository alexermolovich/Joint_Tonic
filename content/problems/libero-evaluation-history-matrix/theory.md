# Record a Continual-Learning Evaluation Matrix

## Intuition

A final score cannot show when a robot gained or lost a skill. Keep a matrix whose rows identify training stages and columns identify tasks, including evaluations before learning begins. Retried reports must not count the same trial twice.

## Mathematics and physical contract

For $K$ tasks, let $n_{ij}$ be the number of distinct evaluation IDs observed at stage $i\in\{0,\ldots,K\}$ on task column $j$. Let $k_{ij}$ count successful trials. The success estimate is
$$R_{ij}=\frac{k_{ij}}{n_{ij}}\quad\text{when }n_{ij}>0.$$
Missing cells are NaN, not zero. Stage zero evaluates the initial policy; stage $i$ follows training on the first $i$ tasks. Trials on not-yet-trained tasks are useful forward-transfer evidence. Counts and rates are dimensionless. Equal evaluation IDs must describe identical stage/task/outcome evidence, otherwise the history is contradictory.

## Worked pipeline and shape trace

```text
columns[a,b], stages[0,1,2]
e1(stage0,b,False) -> counts row0[0,1], rates[NaN,0]
e2(stage1,a,True) + retry e2 -> counts row1[1,0], rates[1,NaN]
no final trials -> row2 counts[0,0], rates[NaN,NaN]
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

A network retry should not improve a reported robot success rate by duplicating one successful trial. Missing historical evaluations remain a limitation even when the final task performance is strong.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
