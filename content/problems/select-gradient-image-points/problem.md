# Select High-Gradient Image Points

Implement `select_gradient_points(image, tile_size, threshold)`.

Select spatially distributed image points with strong central-difference intensity gradients.

`image` is float64 `(H,W)`, `3<=H,W<=1024`, `H*W<=1_000_000`, intensities in `[0,1]`. `tile_size` is a Python int in `[1,128]`; `threshold` a Python int/float in `[0,1]`. Pixel centers use integer `(x=column,y=row)` coordinates, x right and y down. Gradients are intensity per pixel.

For each interior pixel compute `dx=(image[y,x+1]-image[y,x-1])/2`, `dy=(image[y+1,x]-image[y-1,x])/2`, score `sqrt(dx**2+dy**2)`. Exclude the outermost pixel border. Partition the full image into tiles starting at `(0,0)`, with height/width tile_size; partial edge tiles remain. Within each tile choose at most one interior pixel, the highest score strictly greater than threshold. Exact ties choose the smallest row-major image index.

Return a dictionary with fresh int64 `coordinates (K,2)` in `(x,y)` order and float64 `scores (K,)`; emit selected points in tile row-major order. Empty selections are valid. This original fixed-tile selector illustrates spatial gradient coverage; it is not DSO's exact adaptive, multiscale pixel-selection algorithm.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. A `5x5` image whose rows are `[0.,0.25,0.5,0.75,1.]`, tile size `5`, threshold `0.1` yields coordinates `[[1,1]]` and score `[0.25]`. Every interior pixel ties; choose the earliest row-major one.
2. A constant `3x3` image, tile size `1`, threshold `0` returns empty coordinates of shape `(0,2)` and empty scores. Zero gradient does not exceed the threshold.

## Source and scope

[Primary source](https://arxiv.org/abs/1607.02565). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
