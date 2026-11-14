# Monitor Frozen-Feature Drift Across Camera Domains

## Intuition

A frozen encoder provides a stable measurement space. A shift of one feature unit is serious for a stable channel and ordinary for a highly variable one, so compare mean changes relative to reference variability.

## Math and shape trace

Let $R\in\mathbb R^{N\times D}$ be reference embeddings and $C\in\mathbb R^{M\times D}$ current embeddings. Channel $j$ has reference mean $\mu_j$, current mean $\nu_j$, and population variance $s_j^2=N^{-1}\sum_i(R_{ij}-\mu_j)^2$.
$$z_j=\frac{\nu_j-\mu_j}{\sqrt{s_j^2+10^{-6}}},\qquad S=\sqrt{D^{-1}\sum_j z_j^2}.$$
The stabilizer has squared-feature units and imposes a scale floor of 0.001 feature units. $z$ and $S$ are dimensionless; $S$ is an RMS channel shift, not a calibrated probability or statistical test.

| Stage | Shape | Purpose |
|---|---|---|
| Reference moments | D | Baseline variability |
| Current mean | D | Current operating domain |
| Standardized shift | D | Diagnose affected channels |
| RMS | scalar | Summarize magnitude without sign cancellation |

For reference [0,2], $\mu=1,s^2=1$. Current [1,3] has $\nu=2$, so $z=1/\sqrt{1.000001}$. Pooling signed shifts before squaring could cancel a positive shift in one channel against a negative shift in another.

## Why this matters on a robot

Lighting, camera replacement or changed scenes can shift representations before task failures become obvious. Stable means do not prove stable distributions: covariance or tail changes can escape this diagnostic. Keep the encoder and preprocessing versions fixed and investigate task impact separately.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2304.07193). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
