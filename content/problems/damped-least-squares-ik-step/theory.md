# Stabilize Singular IK with Damped Least Squares

## Intuition

A pseudoinverse amplifies errors along nearly singular directions. Damping trades a little task-space residual for smaller joint motion, which is often preferable near a stretched or redundant arm.

## Mathematics and physical meaning

For normalized Jacobian $J\in\mathbb R^{M\times N}$, error $e\in\mathbb R^M$, and damping $\lambda>0$, solve
$$\Delta q=\arg\min_z\left(\|Jz-e\|_2^2+\lambda^2\|z\|_2^2\right).$$
With thin SVD $J=U\operatorname{diag}(\sigma_i)V^\top$, the solution is
$$\Delta q=V\operatorname{diag}\left(\frac{\sigma_i}{\sigma_i^2+\lambda^2}\right)U^\top e.$$
The returned residual is $J\Delta q-e$. A zero singular value contributes zero, while a small value no longer creates an unbounded reciprocal. Larger damping reduces motion but generally leaves more task error. Damping cannot resolve wrong frame conventions or collision constraints.

## Visual trace

| Singular value sigma, lambda=0.1 | Pseudoinverse gain | Damped gain |
|---|---|---|
| 1 | 1 | about 0.9901 |
| 0.001 | 1000 | about 0.09999 |
| 0 | truncated to 0 | 0 |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `jacobian=[[1,0],[0,0]], error=[2,3], damping=1` → correction `[1,0]`, residual `[-1,-3]`.
2. `jacobian=[[1,1]], error=[2], damping=1` → correction `[2/3,2/3]`, residual `[-2/3]`.

## Why this matters on a robot

The joint norm penalty assumes comparable coordinate scaling. Penalizing a prismatic metre and a revolute radian identically without a declared metric changes behavior under a unit conversion. This bounded numerical component does not guarantee collision-safe motion.

## Sources and prerequisites

- [Primary reference 1](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)

Damping must be at least 1e-9; smaller values raise ValueError. This lower bound avoids underflow in the squared damping term.
