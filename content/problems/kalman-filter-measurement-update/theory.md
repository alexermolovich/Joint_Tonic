# One Kalman Filter Measurement Update

## Intuition

A sensor reading should move the estimate strongly only when it is trustworthy relative to the prior. The innovation measures disagreement; the gain distributes that disagreement over correlated state components.

## Mathematics and physical meaning

Define innovation $y=z-Hx$ in sensor units and innovation covariance $S=HPH^\top+R$ in squared sensor units. For state size $n$ and measurement size $m$, the gain $K\in\mathbb R^{n\times m}$ satisfies $KS=PH^\top$:
$$K=PH^\top S^{-1},\qquad x^+=x+Ky.$$
Let $I_n$ be the state identity matrix and $A=I_n-KH$. Use the Joseph form
$$P^+=APA^\top+KRK^\top.$$
This expression explicitly retains the uncertainty of the measurement. R positive definite makes S invertible even if prior P is singular. Independent zero-mean measurement noise and a linear observation model are assumed.

## Visual trace

| Scalar fusion stage | Value |
|---|---|
| Prior x=0, P=1; measurement z=2, R=1 | equal confidence |
| Innovation y | 2 |
| Innovation variance S | 2 |
| Gain K | 0.5 |
| Posterior x+, P+ | 1, 0.5 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `x=[0], P=[[1]], z=[2], H=[[1]], R=[[1]]` → `([1],[[0.5]])`.
2. `x=[3], P=[[0]], z=[10], H=[[1]], R=[[2]]` → `([3],[[0]])`; an exactly known prior receives zero gain.

## Why this matters on a robot

A measurement at the wrong timestamp violates the update assumptions even if the array shapes match. Ignoring covariance cross-terms prevents a position measurement from improving a correlated velocity estimate. Outlier gating is a separate component.

## Sources and prerequisites

- [Primary reference 1](https://www.cs.cmu.edu/~motionplanning/papers/sbp_papers/kalman/welch_intro_kalman.pdf)

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
