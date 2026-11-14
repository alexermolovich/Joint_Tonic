# Validate Layer Output Error After Smoothing

## Intuition

A small average error can conceal one corrupted token. Report both row-level error and total relative error, and make the release rule explicit rather than inferring it from a pleasing average.

## Mathematics and conventions

For reference $Y$ and approximation $\widehat Y$ in $\mathbb R^{N\times D}$, set $E=\widehat Y-Y$.
$$r_i=\sqrt{D^{-1}\sum_k E_{ik}^2},\quad m_i=\max_k|E_{ik}|,\quad\rho=\frac{\|E\|_F}{\max(\|Y\|_F,10^{-12})}.$$
The tolerance $\tau$ has the same dimensionless feature units as $Y$. Row $i$ fails exactly when $m_i>\tau$. The floor defines a finite diagnostic for zero reference tensors; it is not a statistical confidence interval or a task-success guarantee.

## Shape and numerical trace

```text
error rows [0,1] and [0,0] -> RMSE[sqrt(.5),0] -> maxima[1,0] -> tolerance1 passes both; total error norm1/reference norm5=.2.
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

A single visual token can encode a rare obstacle. Global averaging can hide its quantization regression; this gate exposes affected rows but does not replace closed-loop safety evaluation.

## Source and prerequisites

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
