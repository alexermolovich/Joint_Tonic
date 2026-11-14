# Detect Phase Misalignment in a Motion Clip

Two phases close to opposite ends of a cyclic clip can still describe nearly the same point in the motion. Measure the shortest circular error instead of subtracting clip fractions as ordinary linear coordinates.

## Contract

`observed_phase` and `reference_phase` are real `(B, T)`, with `1 <= B <= 128`, `1 <= T <= 256` and phase values in `[0, 1)`. `valid` is a Boolean array of the same shape; `threshold` is a scalar in `[0, 0.5]` clip fractions.

Compute signed circular error as `((observed - reference + 0.5) % 1) - 0.5`, in `[-0.5, 0.5)`. The half-cycle tie is represented as -0.5. Return a dictionary with `error` (float64 `(B, T)`, NaN at invalid samples), `misaligned` (Boolean `(B, T)`, true only for valid samples whose absolute error strictly exceeds the threshold), `mean_absolute` (float64 `(B,)`, mean over each row's valid samples, or NaN when absent) and `counts` (int64 `(B,)`).

Samples refer to aligned moments in the same cyclic clip. This original diagnostic does not align clips, solve time warping or establish successful pose tracking.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Example 1

Observed phase [[0.99]], reference [[0.01]], valid [[True]] and threshold 0.03 give error [[-0.02]], misaligned [[False]], mean_absolute [0.02] and counts [1].

## Example 2

Observed [[0.5]] versus reference [[0]] gives error [[-0.5]]. At threshold 0.5 the sample is not misaligned. An invalid sample instead has NaN error.
