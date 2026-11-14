# Evaluate Sim-to-Real Release Evidence

## Intuition

An aggregate transfer score can hide a failure concentrated in one physical condition. Stratified scenarios make those conditions visible, while explicit observation masks distinguish a failed trial from a trial that was never measured.

## Deterministic factor coverage

Row $i$ has bucket $s_i=i\bmod4$. Independent uniform draws $u_{i0},u_{i1}\in[0,1)$ from the pinned PCG64 generator map into friction $\mu_i$ and lighting gain $g_i$:

$$\mu_i=0.4+0.4(\lfloor s_i/2\rfloor+u_{i0}),\qquad g_i=0.5+0.5((s_i\bmod2)+u_{i1}).$$

Both factors are dimensionless. This enumerates four joint-factor strata; it does not claim coverage of all robot or sensor variations. The same row identity is retained across simulator, replay, shadow, and real-domain columns.

## Rates, uncertainty and transfer gaps

For $n>0$ observed independent Bernoulli trials and success proportion $\hat p$, use $z=1.959963984540054$:

$$c=\frac{\hat p+z^2/(2n)}{1+z^2/n},\quad h=\frac{z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n},\quad CI=[\max(0,c-h),\min(1,c+h)].$$

The interval is a per-domain nominal 95% Wilson interval, not a simultaneous guarantee across every slice. Pooling heterogeneous stratum probabilities makes this an approximate descriptive summary; exact nominal coverage is not guaranteed for the stratified mixture. Repeated correlated rollouts invalidate its independent-trial interpretation. A bucket transfer gap is $\hat p_{sim}-\hat p_{real}$; a negative gap is an improvement.

| Evidence | Example 1 | Example 2 |
| --- | --- | --- |
| Real mean | 1 | 0.75 |
| Worst real bucket | 1 | 0 |
| Maximum sim-real gap | 0 | 1 |
| Verdict | promote | hold |

## Why this matters on a robot

The failure bucket may correspond to low friction under dim light, even when the average looks acceptable. Unknown buckets must remain unknown. These synthetic domain labels exercise release bookkeeping; they do not constitute real-robot transfer evidence. Record actual sampling, repeated-episode dependence, calibration, and outcome provenance before applying the same logic outside the exercise.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1703.06907). [seeded-visual-randomization](/problems/seeded-visual-randomization) · [stratify-visual-factors](/problems/stratify-visual-factors) · [scenario-coverage-confidence](/problems/scenario-coverage-confidence)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
