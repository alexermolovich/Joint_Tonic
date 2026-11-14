# Reject Unmatched Features with Dustbins

Implement `dustbin_assignment(scores, dustbin_score, iterations)`.

Give unmatched image features their own transport capacity and diagnose dustbin-dominant assignments.

`scores` is float64 `(N,M)`, `1<=N,M<=128`, absolute values <=100. `dustbin_score` is a Python int/float in `[-100,100]`; `iterations` is a Python int in `[1,200]`. Scores and masses are dimensionless.

Augment scores to `(N+1,M+1)` by filling the final row and column, including their shared corner, with dustbin_score. Row masses are `[1,...,1,M]/(N+M)`; column masses are `[1,...,1,N]/(N+M)`. Starting from zero log-potentials, perform exactly iterations row-then-column log-Sinkhorn updates as in the prerequisite. Multiply the resulting unit-mass transport matrix by `(N+M)`.

Return this fresh float64 matrix as `assignment`, plus bool `row_unmatched (N,)` when that row's dustbin-column value is strictly greater than every real-column value, and bool `column_unmatched (M,)` analogously for the dustbin row. Ties favor real feature indices, so equality does not mean unmatched. This diagnostic rejects dustbin-dominant rows/columns; it does not extract reciprocal matches. Fixed iteration count can leave row-mass residuals; no automatic convergence or geometric verification is implied.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One source and one target feature, real score 0 and dustbin score 0: every entry of the `2x2` assignment is 0.5. Both unmatched flags are False because the real and dustbin values tie.
2. One source and one target, real score -2 and dustbin score 0, 100 iterations: real-real and dustbin-corner values approach `1/(1+e)`; the two off-diagonal values approach `e/(1+e)`. Both feature unmatched flags are True.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
