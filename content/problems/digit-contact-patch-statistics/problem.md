# Estimate Contact Patch Statistics

A contact candidate mask can be summarized by its area, center and spread in the image. These are geometric image statistics, so preserve pixel conventions and explicitly mark an absent region rather than inventing a center.

## Contract

`mask` is Boolean `(B, H, W)`, with `1 <= B <= 128` and `1 <= H, W <= 64`. Return a dictionary containing:

- `area`: int64 `(B,)`, number of selected pixels.
- `centroid`: float64 `(B, 2)` in `(x=column, y=row)` order.
- `covariance`: float64 `(B, 2, 2)`, the population mean of centered coordinate outer products over selected pixels.
- `bounds`: int64 `(B, 4)` in `(xmin, ymin, xmax_exclusive, ymax_exclusive)` order.

Integer coordinates denote pixel centers. A single pixel has zero covariance. An empty region has area 0, NaN centroid and covariance, and all bounds equal to -1. Aggregate all selected pixels; do not split connected components. Area is a pixel count, centroid uses pixels and covariance uses squared pixels. No physical surface-area or force conversion is implied.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Example 1

Mask [[False, True], [False, True]] yields area 2, centroid [1, 0.5], covariance [[0, 0], [0, 0.25]] and bounds [1, 0, 2, 2].

## Example 2

One selected pixel at row 2, column 3 yields centroid [3, 2], zero covariance and bounds [3, 2, 4, 3]. An empty mask uses NaN centroid/covariance and -1 bounds.
