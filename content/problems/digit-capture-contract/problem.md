# Validate a Tactile Image Capture Contract

A usable tactile frame needs reliable capture metadata as well as pixels. Report clock gaps, dropped identifiers, changed exposure and optical saturation separately so an operator can identify the failing part of the capture pipeline.

## Contract

`frames` must be a NumPy uint8 array `(N, H, W, 3)`, where `0 <= N <= 64` and `1 <= H, W <= 64`. `timestamps` is real `(N,)` in `[0, 1_000_000]` seconds, `frame_ids` is integer `(N,)` in `[0, 1_000_000]`, and `exposure_us` is real `(N,)` in `[1, 1_000_000]` microseconds. `expected_exposure_us` is a scalar in the same exposure range; `max_gap` is a scalar in `[1e-6, 100]` seconds. Records come from one sensor and clock, in acquisition order; report anomalies without reordering them.

Return a dictionary containing:

- `flags`: Boolean `(N, 4)`, ordered bad time step, discontinuous frame ID, exposure shift, saturation.
- `usable`: Boolean `(N,)`, true where no flag is set.
- `saturation_fraction`: float64 `(N,)`, the fraction of all channel values equal to 0 or 255.
- `ready`: Python bool, true only when at least one frame exists and every frame is usable.

The first row has false time/ID flags. Later rows have a bad time flag when the timestamp difference is nonpositive or exceeds `max_gap`; an ID flag when the identifier increment differs from one. Exposure shifts are flagged when `abs(exposure - expected) > 0.05*expected`. Saturation is flagged when its fraction is strictly greater than 0.95. Equality at the positive gap, exposure and saturation thresholds passes. Empty capture is not ready.

Malformed input formats raise ValueError. These original operational thresholds are quality heuristics, not DIGIT contact detection or force calibration.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Example 1

One RGB frame [128, 128, 128] of size 1 by 1, timestamp 0, ID 0, exposure 1000 and expected exposure 1000 yields no flags, usable [True], saturation fraction [0] and ready True.

## Example 2

Two normal frames at times [0, 0.2], IDs [0, 2] and max_gap 0.1 produce timing and ID flags on the second frame. If that frame contains only 255, its saturation flag is also true.
