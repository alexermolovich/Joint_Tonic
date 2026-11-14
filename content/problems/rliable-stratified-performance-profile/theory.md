# Bootstrap a Stratified Performance Profile

## Intuition

A performance profile asks what fraction of runs clear each score threshold. Resample training runs inside each task so every replicate retains the same task mixture. Supplying the index table makes the random choices explicit and reproducible.

## Mathematics and physical contract

Let $X\in\mathbb R^{M\times N}$ contain normalized task/run scores, and $\tau_q$ be threshold $q$ for $0\le q<Q$. The profile uses a strict comparison:
$$p_q=\frac{1}{MN}\sum_{m=0}^{M-1}\sum_{n=0}^{N-1}\mathbf1[X_{mn}>\tau_q].$$
For supplied indices $I\in\{0,\ldots,N-1\}^{B\times M\times N}$, replicate $b$ uses $X^{*(b)}_{mn}=X_{m,I_{bmn}}$ and the same profile formula. $B$ is the replicate count; all scores and thresholds are dimensionless. The task set is fixed. This procedure does not resample tasks, create confidence intervals, or establish a nominal coverage probability.

## Worked pipeline and shape trace

```text
task0 [0,2] -- indices[1,1] --> [2,2]
task1 [10,12] -- indices[0,0] --> [10,10]
thresholds[2,10]: original profile[0.5,0.25], replicate[0.5,0]
indices(B,M,N) -> sampled(M,N) per replicate -> output(B,Q)
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Frames from the same rollout are not independent training seeds. Resampling frames as if they were independent runs can produce misleadingly stable evaluation plots. Threshold equality also matters when sparse rewards create ties.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2021-rliable-statistical-precipice](https://arxiv.org/abs/2108.13264). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
