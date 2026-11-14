# Worked examples

## One cloud, two points

local=[[[1,2],[3,4]]], global_features=[[10,20,30]], float64. Output [[[1,2,10,20,30],[3,4,10,20,30]]]. The same cloud context is repeated, not interleaved.

## Keep clouds independent

local=[[[1]],[[2]]], global_features=[[10,11],[20,21]], float32. Output [[[1,10,11]],[[2,20,21]]]. Cloud0 never receives cloud1's context.
