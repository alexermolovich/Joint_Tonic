# Normalize Assignments with Sinkhorn Iterations

Implement `sinkhorn_assignments(log_scores, row_mass, column_mass, iterations)`.

Normalize a positive transport assignment by alternating row and column updates in log space.

`log_scores` is float64 `(N,M)`, `1<=N,M<=128`, entries with absolute magnitude <=100. `row_mass (N,)` and `column_mass (M,)` are float64, each entry in `[1e-9,1]`; each vector sum must be within absolute tolerance 1e-9 of 1, then normalize each vector to sum exactly 1 numerically. `iterations` is a Python int in `[1,200]`.

Initialize row and column log-potentials to zero. Repeat exactly the requested number of iterations, updating all rows first and all columns second: `u=log(a)-logsumexp(S+v,axis=columns)`, then `v=log(b)-logsumexp(S+u,axis=rows)`. Inputs already contain entropy-scaled logits; no additional temperature is applied.

Return a dictionary: `log_transport (N,M)=S+u[:,None]+v[None,:]`, `transport (N,M)=exp(log_transport)`, and Python floats `row_error=max(abs(transport.sum(1)-a))`, `column_error=max(abs(transport.sum(0)-b))`. Use stable log-sum-exp. The final update enforces column marginals up to floating error; row marginals may still have residual error after finite iterations. Do not silently iterate to convergence.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Zero `2x2` logits with row/column masses `[0.5,0.5]` give transport `[[0.25,0.25],[0.25,0.25]]` after one iteration.
2. Zero `2x2` logits with row masses `[0.75,0.25]` and column masses `[0.5,0.5]` give `[[0.375,0.375],[0.125,0.125]]`. Its logarithm is returned separately.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
