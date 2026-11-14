# Evaluate a Bounded Continuous-Control Reward

## Intuition

A tolerance reward distinguishes a target interval from a smoothly decaying neighborhood around it. Inside the interval the score is exactly one. A margin specifies a physical distance, and its configured value specifies the reward at that distance.

## Mathematics and physical contract

For coordinate $x$ and inclusive target interval $[l,u]$, distance is $d(x)=\max(l-x,0,x-u)$. The values $x,l,u$ and margin $m$ share one physical unit. With dimensionless $v\in[10^{-6},1-10^{-6}]$, define
$$r(x)=\begin{cases}\mathbf1[d(x)=0],&m=0,\\\exp\!\left(\log(v)\,\min(d(x)/m,10^6)^2\right),&m>0.\end{cases}$$
This Gaussian family gives $r=1$ at distance zero and $r=v$ at distance $m$. The normalized-distance cap makes extremely small positive margins well-defined in float64; at that cap the exponential underflows to zero. It does not change ordinary representable rewards. Only this bounded Gaussian family is implemented.

## Worked pipeline and shape trace

```text
target interval [0,1], margin1, value_at_margin0.5
x:        -1   0   1   2
distance:  1   0   0   1
reward:   .5   1   1  .5
zero margin -> hard inclusive interval membership
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Using millimeters for values and meters for the margin changes the reward landscape by three orders of magnitude. A smooth reward is a training signal, not proof of a physically safe state.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2018-deepmind-control-suite](https://github.com/google-deepmind/dm_control/blob/main/dm_control/utils/rewards.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
