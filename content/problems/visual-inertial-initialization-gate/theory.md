# Validate a Visual-Inertial Initialization

## Intuition

A low residual is not enough to initialize a visual-inertial estimator. The same data can fit many scales or biases when motion is uninformative. Keep excitation, metric plausibility, bias bounds, and residual quality as separate inspectable checks.

## Mathematics and conventions

The supplied gauge-fixed Jacobian $J\in\mathbb R^{R\times D}$ is already whitened and parameter-scaled, hence dimensionless; residuals $r\in\mathbb R^R$ use the same eligible-row mask $M$. Let $n=\sum_iM_i$. For singular values $\sigma_k$ of $J_M$ and relative cutoff $\epsilon$,
$$q=\#\{k:\sigma_k>\epsilon\sigma_0\},\qquad \operatorname{RMS}=\sqrt{\frac1n\sum_{i:M_i}r_i^2}.$$
Set rank zero for an empty or zero Jacobian, and RMS NaN if $n=0$. Observability requires both $n\ge D$ and $q=D$. The positive metric scale $s$ is dimensionless. Gravity $g\in\mathbb R^3$ has world-frame m/s$^2$ units and magnitude error
$$e_g=\big|\|g\|_2-9.81\big|.$$
The remaining checks compare scale to its inclusive interval, $e_g$ to its m/s$^2$ tolerance, gyro-bias norm to a rad/s bound, accelerometer-bias norm to a m/s$^2$ bound, and RMS to its dimensionless limit. Acceptance is the conjunction of all six. This is a diagnostic over a supplied candidate, not an optimizer or a proof of nonlinear observability; gravity direction is deliberately not gated.

## Visual computation trace

| Candidate evidence | Check |
|---|---|
| Valid Jacobian rows | Full numerical rank with enough rows |
| Metric scale | Inside supplied interval |
| Gravity magnitude | Close to 9.81 m/s² |
| Gyro and accelerometer biases | Separate norm limits |
| Whitened residuals | RMS below supplied bound |
| All six flags | Candidate accepted |

## Worked examples

1. Scale 1, gravity [0,0,-9.81], zero biases, residual [0.2], valid [True], Jacobian [[1]], and limits [0.5,2,0.1,0.1,0.1,0.2,1e-6] pass all six checks. Rank is 1 and RMS is 0.2.
2. Jacobian rows [[1,0],[1,0]] have rank 1 despite two observations and zero residuals. The observability check fails, so the candidate is rejected even with a perfect residual fit.

## Why this matters on a robot

Stationary or repetitive motion can make scale unobservable while residuals remain small. Tight bias limits can also reject a valid but poorly calibrated sensor. Thresholds are explicit operational choices, not the paper’s complete initialization procedure.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2007.11898). [initialization-observability-rank](/problems/initialization-observability-rank)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
