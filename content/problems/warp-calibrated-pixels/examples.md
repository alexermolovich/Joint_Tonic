# Worked examples

1. Source/target intrinsics `[2.,2.,0.,0.]`, identity transform, source pixel `[[1.,0.]]`, inverse depth `[0.5]`, target size `[4,4]` give point `[[1.,0.,2.]]`, pixel `[[1.,0.]]`, visible `[True]`.
2. Add target-from-source translation `[1.,0.,0.]` to the same example. The target point becomes `[[2.,0.,2.]]` and pixel `[[2.,0.]]`, still visible.
