# Worked examples

1. With identity transform, plane scan point `[[0.,0.,2.]]`, anchor `[[0.,0.,0.]]` and normal `[[0.,0.,1.]]`, the signed plane residual is `[2.]` meters. Line scan point `[[0.,1.,0.]]`, endpoints `[[0.,0.,0.]]` and `[[2.,0.,0.]]` give line distance `[1.]` meter.
2. Keep the plane point and anchor but negate the normal: plane residual is `[-2.]`. Reversing a line's endpoint order leaves its nonnegative distance unchanged.
