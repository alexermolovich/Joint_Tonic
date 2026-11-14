# Measure Cross-Robot Prediction Error

## Intuition

Large images and long episodes contribute more pixel residuals. A pooled pixel error answers a different question from giving every robot episode equal weight. Aggregate chunks into episodes first, then show both summaries for each robot.

## Mathematics and physical contract

Chunk $i$ supplies summed squared normalized-pixel residual $s_i$ and pixel/channel sample count $n_i$. Group by robot $r$ and episode $e$: $S_{re}=\sum_i s_i$ and $N_{re}=\sum_i n_i$ over matching chunks. For positive-support episode set $E_r$,
$$P_r=\frac{\sum_eS_{re}}{\sum_eN_{re}},\qquad Q_r=\frac{1}{|E_r|}\sum_{e\in E_r}\frac{S_{re}}{N_{re}}.$$
$P_r$ weights pixel samples; $Q_r$ weights episodes equally. Residuals are dimensionless squared intensity differences, bounded per sample by one. A zero-support robot remains visible with zero counts and NaN means. Episode identity is the pair (robot ID, episode ID), preventing collisions across robot namespaces.

## Worked pipeline and shape trace

```text
robot0 episode1: sumerror1/pixels1 -> MSE1
robot0 episode2: sumerror0/pixels9 -> MSE0
pooled pixel MSE1/10=.1; equal episode MSE(1+0)/2=.5
chunks -> robot/episode totals -> two robot-level weighting policies
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Cross-robot datasets often have different video resolutions and episode lengths. A lower pooled error can reflect those support differences rather than better transfer. This report does not establish that test robots were held out during training.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
