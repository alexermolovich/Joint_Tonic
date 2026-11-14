# Worked examples

1. A `5x5` image whose rows are `[0.,0.25,0.5,0.75,1.]`, tile size `5`, threshold `0.1` yields coordinates `[[1,1]]` and score `[0.25]`. Every interior pixel ties; choose the earliest row-major one.
2. A constant `3x3` image, tile size `1`, threshold `0` returns empty coordinates of shape `(0,2)` and empty scores. Zero gradient does not exceed the threshold.
