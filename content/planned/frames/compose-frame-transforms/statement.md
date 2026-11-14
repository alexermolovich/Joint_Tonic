# Compose and Invert Coordinate Transforms

**Status: planned.** A camera is mounted on a robot base whose pose is known in the world. Produce the camera-to-world transform and its inverse without confusing the frame of each translation.

## Contract

Inputs are two finite, proper homogeneous matrices `T_ab` and `T_bc`, each `(4,4)`, plus their frame labels. The notation means **a-from-b**: multiplying `T_ab` by a column point in frame b expresses that point in frame a. Both transforms describe the same timestamp; translation uses meters.

Return a new `T_ac` and `T_ca`, each `(4,4)`. Compose in the order `T_ab @ T_bc`. Inversion must rotate the negative translation into the inverse frame. Preserve inputs.

Reject non-rigid transforms, nonfinite values, malformed shapes, different units/timestamps, or a middle frame that does not match. Frame-label compatibility is checked before numerical multiplication. Do not reinterpret a matrix whose labels are reversed.

## Expected capability

Trace a calibration chain and verify the inverse by transforming a point out and back. This exercise does not estimate calibration from observations.

See [worked inputs and outcomes](examples.md), [theory](theory.md), and [progressive hints](hints.md).
