# Bound a Sequential Convex Trust-Region Step

Implement `bound_trust_step(current, proposal, lower, upper, radius)`.

Project a proposed joint increment into a box trust region and position limits.

`current`, `proposal`, `lower`, `upper` are float64 `(D,)` radians, `1<=D<=64`, with lower<=current<=upper elementwise. Proposal is an increment, not an absolute configuration. `radius` is Python int/float in `[0,100]` radians. Intersect increment bounds `[-radius,radius]` with `[lower-current,upper-current]`, clip proposal to that intersection, and return a dict `step`: float64 `(D,)`, `next_configuration`: float64 `(D,)` current+step, and `clipped`: bool `(D,)` where proposal differs exactly from step. All outputs are independent. Radius0 yields zero step. Each joint is a rotational coordinate at the current planning iteration; no timestamp integration or angular wrapping is performed. This box projection bounds a proposed step; it does not solve a full constrained quadratic program or certify nonlinear constraints.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Current `[0.8,-0.8]`, proposal `[0.5,-0.5]`, lower `[-1.,-1.]`, upper `[1.,1.]`, radius `0.3` gives step approximately `[0.2,-0.2]`, next `[1.,-1.]`, and clipped `[True,True]`.
2. Current `[0.]`, proposal `[0.1]`, limits `[-1.]` to `[1.]`, radius `0` returns step `[0.]`, next `[0.]`, clipped `[True]`.

## Source and scope

[Primary source](https://rll.berkeley.edu/trajopt/ijrr/). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
