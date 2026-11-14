# Aggregate Evaluation by Activity Slice

## Intuition

An overall activity accuracy can hide a class with almost no labeled examples. Keep one confusion matrix per dataset, expose true-class support, and average recall only over classes with evidence. Unlabeled samples remain missing rather than being assigned a fabricated class.

## Mathematics and physical contract

For dataset $d$, true class $a$ and predicted class $b$, observed-sample confusion count is
$$C_{dab}=\sum_i\mathbf1[d_i=d]\,m_i\,\mathbf1[y_i=a]\,\mathbf1[\widehat y_i=b].$$
Here $m_i$ is the Boolean observation mask and classes range from zero to $K-1$. True-class support is $n_{da}=\sum_bC_{dab}$ and recall $r_{da}=C_{daa}/n_{da}$ when supported. Macro recall averages $r_{da}$ only over classes with $n_{da}>0$; unsupported classes and datasets have NaN summaries. Counts and rates are dimensionless. This is a bounded classification diagnostic, not the official metric for every egocentric-video task.

## Worked pipeline and shape trace

```text
dataset0: true[0,0,1], predicted[0,1,0]
confusion rows true/columns predicted: [[1,1],[1,0]]
support[2,1] -> recall[.5,0] -> macro .25
unobserved labels are ignored even if their placeholder IDs are out of range
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Human activity datasets can support robot perception without providing executable robot commands. Class support makes representation failures visible, but recall alone cannot establish robot control quality or task completion.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
