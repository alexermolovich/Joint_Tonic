# Worked examples

1. Zero query/window descriptors with S=3 yield uniform probability 1/9. With pixel_scale `[1.,1.]`, the offset is `[0.,0.]` and covariance `[[2/3,0],[0,2/3]]`. Scale `[2.,3.]` changes it to `[[8/3,0],[0,6]]`.
2. D=1, query 1, a `3x3` window with center value log(8) and all others zero gives center probability 1/2 and every other cell 1/16. Its offset is zero and covariance is `[[0.375,0],[0,0.375]]` at unit scale.
