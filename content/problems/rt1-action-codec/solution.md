# Solution approach

Validate integer settings before converting arrays. Convert actions and bounds to float64, then check the last action dimension against the bound vectors. Require finite numbers and strictly positive finite widths.

Apply np.clip, scale by the per-dimension width, floor the bin positions, and clamp to bins−1. Convert indices to int64 before adding the reserved offset. Reconstruct physical values from the unoffset indices plus 0.5.

Each element is visited a constant number of times, so time and output memory are O(number of action elements). Leading batch axes are handled by broadcasting; the last dimension always means action channels.

At an exact upper bound, scaled=1 would otherwise yield index bins. Do not use np.round: the contract defines left-closed bins with floor. Do not mutate actions when clipping.
