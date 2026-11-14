# Linearize a Signed-Distance Collision Penalty

Implement `linearized_collision_penalty(distances, jacobian, step, margin)`.

Evaluate a local first-order clearance model, hinge penalties, and one chosen subgradient.

`distances` float64 `(N,)` meters and `jacobian` float64 `(N,D)` meters/radian are sampled at one current joint configuration, `0<=N<=4096`, `1<=D<=16`. `step` float64 `(D,)` is a proposed joint increment in radians; `margin` is Python int/float `[0,100]` meters. Positive clearance means outside collision. Return `predicted`: float64 `(N,)` equal to distances+jacobian@step; `hinge`: float64 `(N,)` max(margin-predicted,0); `cost`: Python float sum(hinge); and `gradient`: float64 `(D,)` negative sum of Jacobian rows whose predicted clearance is strictly below margin. At exact equality choose subgradient zero. Empty pairs give empty predicted/hinge and zero cost/gradient. All outputs are fresh. The supplied Jacobian is not recomputed; the result describes the local model, not verified nonlinear scene clearance.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Distances `[0.02,0.08]`, Jacobian `[[1.],[-1.]]`, step `[0.01]`, margin `0.05`: predicted `[0.03,0.07]`, hinge `[0.02,0.]`, cost `0.02`, gradient `[-1.]`.
2. Distance `[0.05]`, Jacobian `[[2.]]`, step `[0.]`, margin `0.05`: hinge and cost zero, chosen gradient `[0.]` at the kink.

## Source and scope

[Primary source](https://rll.berkeley.edu/trajopt/ijrr/). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
