# Assemble Obstacle and Prior Residuals

Implement `assemble_residuals(prior, clearances, margin, obstacle_sigma)`.

Assemble a least-squares vector from an already whitened motion prior and obstacle clearance samples.

`prior` is float64 `(P,)`, `0<=P<=65536`, dimensionless and already whitened. `clearances` is float64 `(N,)`, `0<=N<=65536`, signed surface-to-surface distances in meters in one fixed world; positive values mean separation. `margin` is a Python int/float in `[0,100]` meters. `obstacle_sigma` is a Python int/float in `[1e-6,1e6]` meters.

Compute obstacle residual `h=max(margin-clearances,0)/obstacle_sigma`. Return fresh float64 `residual (P+N,)` containing prior then h, and Python floats `prior_cost=0.5*sum(prior**2)`, `obstacle_cost=0.5*sum(h**2)`, `total_cost=prior_cost+obstacle_cost`, in a dictionary. Both empty arrays are allowed and give zero costs. Every supplied clearance is an observation; there is no missing-data mask. No robot geometry, distance field, prior whitening or derivative is inferred. The obstacle factor uses one independent isotropic weight; this is residual assembly, not trajectory optimization.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Prior `[2.]`, clearances `[0.1,0.5]`, margin `0.3`, sigma `0.2` give residual `[2.,1.,0.]`, prior cost `2`, obstacle cost `0.5`, total `2.5`.
2. Empty prior, clearance `[-0.1]`, margin `0`, sigma `0.1` give residual `[1.]` and total cost `0.5`.

## Source and scope

[Primary source](https://arxiv.org/abs/1707.07383). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
