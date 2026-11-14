# Compare Drift Across Sensor Configurations

## Intuition

A sensor configuration can appear better simply because it loses tracking on difficult frames. Compare all configurations on exactly the same timestamps, and make the resulting coverage loss visible.

## Mathematics and conventions

Let $X_{cn}\in\mathbb R^3$ be configuration $c$ position and $Y_n\in\mathbb R^3$ reference position at matched timestamp $n$, all in the same world frame and meters. Availability $V_{cn}$ gives common support $M_n=\bigwedge_c V_{cn}$. For $K=\sum_n M_n>0$,
$$e_{cn}=\|X_{cn}-Y_n\|_2,\qquad \operatorname{RMSE}_c=\sqrt{\frac1K\sum_{n:M_n}e_{cn}^2}.$$
Report the final common timestamp's error and improvement $\Delta_c=\operatorname{RMSE}_{b}-\operatorname{RMSE}_c$, where $b$ is the supplied baseline index. All three metrics are meters. The winning index minimizes RMSE with lower-index ties. Missing support gives NaN errors and aggregates, and winner -1. No posthoc spatial alignment is performed: caller-provided common coordinates are part of the contract.

## Visual computation trace

```text
config 0 validity: 1 1 0 1
config 1 validity: 1 0 1 1
common support:   1 0 0 1
both errors use timestamps 0 and 3; endpoint means timestamp 3
```

## Worked examples

1. Reference positions are [[0,0,0],[1,0,0]]. Configuration 0 equals reference; configuration 1 adds [1,0,0] at both times. With all entries valid and baseline 1, RMSE and endpoint errors are [0,1] meters, improvement [1,0], and best index 0.
2. Valid masks [[True,False],[False,True]] have no common sample. Count is 0, best is -1, and every error/aggregate is NaN.

## Why this matters on a robot

Comparing one system on easy frames and another on all frames rewards tracking failure. Common-support evaluation prevents that bias but can discard much of the trajectory; always report its count. Absolute position error alone does not isolate cumulative drift.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1901.03642). [aligned-trajectory-position-error](/problems/aligned-trajectory-position-error)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
