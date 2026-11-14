# Solve IK with a Jacobian Pseudoinverse

## Intuition

Forward kinematics predicts where joints put the tool; the Jacobian predicts how a small joint change moves it. Repeatedly solve that local linear approximation and re-evaluate the nonlinear geometry.

## Mathematics and physical meaning

With link lengths $L_1,L_2$ and angles $q_1,q_2$, endpoint $p$ is
$$p=\begin{bmatrix}L_1\cos q_1+L_2\cos(q_1+q_2)\\L_1\sin q_1+L_2\sin(q_1+q_2)\end{bmatrix}.$$
The position Jacobian in metres/radian is
$$J=\begin{bmatrix}-L_1\sin q_1-L_2\sin(q_1+q_2)&-L_2\sin(q_1+q_2)\\L_1\cos q_1+L_2\cos(q_1+q_2)&L_2\cos(q_1+q_2)\end{bmatrix}.$$
For target $g$ in metres, let $e=g-p$ and $\Delta q=J^+e$, using singular-value cutoff $10^{-12}$ relative to the largest singular value. If $\|\Delta q\|_2>s$, scale it to norm $s$ where $s$ is max_step. Update $q\leftarrow q+\Delta q$. This local method can stall at singular configurations or unreachable targets; a false convergence flag is a valid outcome.

## Visual trace

| Iteration stage | Quantity | Purpose |
|---|---|---|
| Forward model | p(q) | current tool location |
| Residual | target-p | task-space correction |
| Pseudoinverse | J+ residual | local joint change |
| Step bound | norm <= max_step | limit linearization jump |
| Re-evaluate | new p(q) | check actual error |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `lengths=[1,1], initial_q=[0,pi/2], target=[1,1], max_iterations=20, tolerance=1e-6, max_step=0.5` returns the initial q, True, and a one-element near-zero error history.
2. `lengths=[1,1], initial_q=[0,0], target=[3,0], max_iterations=2, tolerance=1e-6, max_step=0.5` returns `[0,0]`, False, errors `[1,1,1]`; the straight arm cannot move outward.

## Why this matters on a robot

A singular arm may have no first-order motion toward a target even when other configurations are useful. Never mistake iteration exhaustion for success. Collision-aware branch selection and damped updates are separate lessons.

## Sources and prerequisites

- [Primary reference 1](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)

Each link length must be at least 1e-9 metres; smaller values raise ValueError.
