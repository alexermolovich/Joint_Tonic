# Pull Back a Local Motion Metric

## Intuition

A changing task map contributes acceleration even when joint acceleration is zero. Pulling a desired task acceleration backward must account for that contribution before assigning a joint-space policy.

## Mathematics and conventions

For $J,\dot J\in\mathbb R^{T\times D}$, joint velocity $v\in\mathbb R^D$, task natural force $f\in\mathbb R^T$, and positive-semidefinite metric $M\in\mathbb R^{T\times T}$,

$$M_q=J^TMJ,\qquad f_q=J^T(f-M\dot Jv).$$

This follows the task acceleration relation $\ddot x=J\ddot q+\dot Jv$. The correction $\dot Jv$ has units 1/s² in these normalized coordinates. The two output tensors have shapes $D\times D$ and $D$. The supplied force must already contain the leaf policy's own terms; this operation performs only the coordinate pullback.

## Visual computation trace

| Operation | Scalar example |
| --- | --- |
| Task-map curvature | Jdot*v = 3 |
| Metric-weighted curvature | M*3 = 12 |
| Corrected natural force | 20-12 = 8 |
| Joint pullback | J*8 = 16 |

## Worked examples

1. J=`[[2.]]`, Jdot=`[[1.]]`, joint velocity `[3.]`, metric `[[4.]]`, force `[20.]` give pulled metric `[[16.]]` and force `[16.]`: subtract the task curvature contribution `4*1*3=12` before multiplying by J.T.
2. With the same inputs but Jdot=`[[0.]]`, pulled metric remains `[[16.]]`, while force becomes `[40.]`.

## Why this matters on a robot

Dropping the Jdot term changes the commanded motion under nonlinear task maps. A coordinate scaling change also requires consistent Jacobians and metrics; arbitrary leaf policies do not inherit a stability guarantee.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1811.07049). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
