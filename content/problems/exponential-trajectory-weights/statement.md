# Normalize Exponential Trajectory Cost Weights

Implement `trajectory_weights(costs, valid, temperature)`.

Convert supplied corrected rollout costs into stable normalized weights.

`costs` float64 `(N,)`, `valid` bool `(N,)`, `1<=N<=16384`, with at least one valid entry. Costs use one common caller-defined cost unit. `temperature` is Python int/float in `[1e-6,1e6]` in the same units. For valid entries use `exp(-(cost-min_valid_cost)/temperature)` and normalize over valid entries; invalid weights are exactly zero. Return dict `weights`: fresh float64 `(N,)`, `effective_samples`: Python float `1/sum(weights²)`, and `best_index`: Python int, lowest original index attaining the minimum valid cost. Invalid entries must still satisfy numeric validation. These are supplied corrected MPPI rollout costs, including any required control/importance terms; the exercise does not derive those terms or run a dynamics model. There is no spatial frame or time integration in this reduction.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Costs `[0.,log(3)]`, both valid, temperature1 gives weights `[0.75,0.25]`, effective samples `1.6`, best index0.
2. Costs `[2.,-100.,2.]`, validity `[True,False,True]`, temperature1 gives weights `[0.5,0.,0.5]`, effective samples2, best index0.

## Source and scope

[Primary source](https://arxiv.org/abs/1509.01149). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
