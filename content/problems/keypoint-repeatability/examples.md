# Worked examples

1. Identity warp, source points `[[0.,0.],[2.,0.]]`, target `[[0.,0.]]`, both image sizes `[3,3]`, threshold 0: source correctness `[True,False]`, target correctness `[True]`, repeatability `2/3`.
2. The same image sizes with one point `[0.,0.]` in each image and target-from-source x translation +3 have no shared support. Both eligibility flags are False and repeatability is NaN.
