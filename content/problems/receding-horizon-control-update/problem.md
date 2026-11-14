# Update a Receding-Horizon Control Sequence

Implement `update_control_plan(controls, perturbations, weights, lower, upper)`.

Apply a weighted rollout perturbation, bound the control sequence, and recede by one step.

`controls` float64 `(H,D)`, `1<=H<=128`, `1<=D<=16`, and `perturbations` float64 `(K,H,D)`, `1<=K<=256`, contain joint-velocity commands in radians/second for a fixed caller-declared control period. `weights` float64 `(K,)` are nonnegative and their sum must differ from1 by at most1e-9; use the supplied weights as-is without renormalizing. `lower,upper` float64 `(D,)` are command limits in radians/second, lower<=upper. Controls may start outside the limits; clipping happens after adding the weighted update. Compute `updated=clip(controls+sum_k(weights[k]*perturbations[k]),lower,upper)`. Return dict `updated`: fresh float64 `(H,D)`, `action`: fresh `(D,)` copy of updated first row, `next_plan`: fresh `(H,D)` containing updated rows1..H-1 followed by a repeat of updated's last row. H1 repeats its sole row. Outputs must not alias each other or inputs. This returns a proposed action only; it does not execute the action or step a robot. Clipping and last-row padding are explicit teaching policies, not a preservation claim for every MPPI theoretical guarantee.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Controls `[[0.],[1.]]`, perturbations `[[[2.],[0.]],[[0.],[2.]]]`, weights `[0.25,0.75]`, limits `[-1.]` to `[2.]`: updated `[[0.5],[2.]]`, action `[0.5]`, next plan `[[2.],[2.]]`.
2. One-step control `[[3.]]`, one zero perturbation, weight `[1.]`, limits `[-1.]` to `[1.]`: updated `[[1.]]`, action `[1.]`, next plan `[[1.]]`, all independent arrays.

## Source and scope

[Primary source](https://arxiv.org/abs/1509.01149). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
