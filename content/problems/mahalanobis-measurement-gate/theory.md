# Gate Measurements with Mahalanobis Distance

## Intuition

A metre of disagreement means different things for a precise camera and a noisy range sensor. Normalize residuals by uncertainty before deciding whether an observation is plausible.

## Mathematics and physical meaning

Each residual row $r_i\in\mathbb R^D$ has sensor units. Shared positive-definite covariance $S\in\mathbb R^{D\times D}$ includes correlations. Compute
$$d_i^2=r_i^\top S^{-1}r_i,\qquad a_i=\mathbf1[d_i^2\le\gamma].$$
$d_i^2$ and threshold $\gamma$ are dimensionless. If $S=LL^\top$ is a Cholesky factorization, solving $Lu_i=r_i$ gives $d_i^2=u_i^\top u_i$. This squared distance must not be compared against a threshold intended for the unsquared distance.

## Visual trace

| Residual, S=diag(4,1) | Normalized residual | Squared distance | Gate gamma=1 |
|---|---|---|---|
| [2,0] | [1,0] | 1 | accept |
| [0,2] | [0,2] | 4 | reject |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `residuals=[[2,0],[0,2]], covariance=diag([4,1]), threshold=1` → distances `[1,4]`, accepted `[True,False]`.
2. `residuals=[[0]], covariance=[[2]], threshold=0` → `([0],[True])`.

## Why this matters on a robot

Ignoring correlated uncertainty changes the gate’s orientation and can reject valid observations. A bad covariance can make every innovation look acceptable; this component checks algebraic validity, not whether the sensor noise model is calibrated.

## Sources and prerequisites

- [Primary reference 1](https://www.cs.cmu.edu/~motionplanning/papers/sbp_papers/kalman/welch_intro_kalman.pdf)

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
