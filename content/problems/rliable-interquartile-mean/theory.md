# Compute an Interquartile Mean Benchmark Score

## Intuition

A few exceptionally lucky or unlucky training seeds can dominate an ordinary mean. Pool equally represented tasks, remove a fixed number of extreme scores on each side, and summarize the remaining evidence. This does not guarantee that every task improved.

## Mathematics and physical contract

Let $X\in\mathbb R^{M\times N}$ hold dimensionless normalized returns, with $M$ tasks and $N$ independent training runs per task. Flatten and sort its $K=MN$ entries to obtain $z_0\le\cdots\le z_{K-1}$. Define $k=\lfloor K/4\rfloor$. The finite-sample aggregate is
$$\operatorname{IQM}(X)=\frac{1}{K-2k}\sum_{i=k}^{K-k-1}z_i.$$
The floor convention matters: three observations lose zero entries. Scores must already be normalized onto a meaningful common scale; the exercise does not normalize incompatible reward functions.

## Worked pipeline and shape trace

```text
8 pooled scores: 0 1 | 2 3 4 5 | 6 100
remove 2 low and 2 high -> retained sum14/count4 -> 3.5
shape(M,N) -> sorted(K,) -> scalar
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Robot training is expensive, so evaluation often has few seeds. Reporting a trimmed average without its sample size can conceal how little trimming actually occurred. Never interpret this aggregate as a collision or safety rate.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2021-rliable-statistical-precipice](https://github.com/google-research/rliable/blob/master/rliable/metrics.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
