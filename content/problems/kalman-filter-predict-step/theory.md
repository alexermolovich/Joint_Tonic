# One Kalman Filter Predict Step

## Intuition

When no new observation arrives, the robot still moves and its uncertainty evolves. The state transition transports the mean; transporting uncertainty requires applying that transition on both covariance axes.

## Mathematics and physical meaning

Let $x\in\mathbb R^n$ be the state mean, $P\in\mathbb R^{n\times n}$ its covariance, $F$ the interval transition and $Q$ zero-mean process-noise covariance, independent of the prior error. Then
$$x^-=Fx,\qquad P^-=FPF^\top+Q.$$
For $x=[p,v]^\top$ with position $p$ in metres and velocity $v$ in metres/second, $F=\begin{bmatrix}1&\Delta t\\0&1\end{bmatrix}$. The entries of $P$ consequently have units m², m²/s, and m²/s². Superscript minus denotes prediction before a measurement, not subtraction.

## Visual trace

| Stage, dt=1 s | Position mean (m) | Velocity mean (m/s) | Covariance |
|---|---|---|---|
| Prior | 0 | 2 | identity |
| Transport, Q=0 | 2 | 2 | [[2,1],[1,1]] |
| Add Q=diag(0.1,0.2) | 2 | 2 | [[2.1,1],[1,1.2]] |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `x=[0,2], P=eye(2), F=[[1,1],[0,1]], Q=diag([0.1,0.2])` → `([2,2], [[2.1,1],[1,1.2]])`.
2. `x=[3], P=[[2]], F=[[1]], Q=[[0]]` → `([3],[[2]])`.

## Why this matters on a robot

Dropping F.T produces an asymmetric object that cannot represent uncertainty. Reusing Q from a different sensor period makes the filter overconfident or noisy. This is a linear prediction component, not a complete localization system.

## Sources and prerequisites

- [Primary reference 1](https://www.cs.cmu.edu/~motionplanning/papers/sbp_papers/kalman/welch_intro_kalman.pdf)

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
