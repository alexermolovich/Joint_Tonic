# Build a Joint-Space Smoothness Cost

Implement `smoothness_cost(path, weights)`.

Compute a discrete weighted joint-step cost and its exact gradient.

`path` is float64 `(T,D)` radians, `1<=T<=4096`, `1<=D<=16`; `weights` float64 `(D,)` are nonnegative inverse-radians-squared weights. Return `cost`: Python float sum over adjacent rows and joints of `weights*(path[t+1]-path[t])²`, and `gradient`: fresh float64 `(T,D)` derivative with respect to every joint sample. A single-row path has zero cost and gradient. This discrete cost assumes a fixed waypoint indexing convention: no time spacing is supplied or inferred, and it is not a velocity integral or a time-optimal objective. The diagonal weighting is a bounded original teaching choice.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Path `[[0.],[1.],[3.]]`, weight `[2.]` gives cost `10` and gradient `[[-4.],[-4.],[8.]]`.
2. Path `[[7.,-2.]]`, weights `[1.,3.]` gives cost zero and gradient `[[0.,0.]]`.

## Source and scope

[Primary source](https://rll.berkeley.edu/trajopt/ijrr/). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
