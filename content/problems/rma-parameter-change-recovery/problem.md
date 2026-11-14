# Evaluate Policy Recovery After a Parameter Change

Recovery requires a sustained window of measured good tracking after the environment changes. Removing missing samples before counting would falsely join observations that were never consecutive.

## Contract

`times` is real `(T,)`, strictly increasing in `[0, 1_000_000]` seconds. `errors` is real `(B, T)`, nonnegative and at most 1,000,000; `valid` is Boolean `(B, T)`. Bounds are `1 <= B <= 128`, `1 <= T <= 4096`. `change_index` is a built-in Python int in `[0, T)`, `hold_samples` is a built-in Python int in `[1, T]`, and `tolerance` is a scalar in `[0, 1_000_000]`.

The change occurs at `times[change_index]`. Find the earliest window start at or after that index whose next `hold_samples` records all exist, are valid, and have errors at most the tolerance. Missing records break the run; never compress them away.

Return a dictionary with `recovered` (Boolean `(B,)`), `index` (int64 `(B,)`, first qualifying start or -1), `delay` (float64 `(B,)`, start timestamp minus change timestamp, NaN if no run), `post_change_mean` (float64 `(B,)`, mean of all valid errors from the change onward, NaN if absent), and `counts` (int64 `(B,)`, number of those valid errors).

Delay reports the start of the verified stable window, although its evidence finishes later. Errors are dimensionless normalized tracking losses. This original diagnostic does not prove dynamical stability or reproduce the paper's benchmark.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Example 1

Times [0, 1, 2, 3], errors [[2, 0.2, 0.1, 0.1]], all valid, change index 1, tolerance 0.1 and hold length 2 yield recovered true, index 2, delay 1 second, post-change mean 0.4/3 and count 3.

## Example 2

If the record at time 2 is missing, no two consecutive valid samples meet the threshold. Recovery is false, index -1 and delay NaN, even though the final sample is good.
