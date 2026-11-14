# Measure Camera Reprojection Residuals

**Status: planned.** Compare where known 3D landmarks should appear with their measured image locations.

## Contract

Inputs: finite camera-frame points `(N,3)`, valid zero-skew pinhole matrix `K (3,3)`, and finite observed pixels `(N,2)`. Camera axes are x right, y down, z forward. Points are meters; intrinsics and image measurements use pixels. Inputs represent synchronized measurements and known correspondences.

Project points with `z>1e-8`. Return float64 residuals `(N,2)` using **observation minus prediction**, a bool validity vector `(N,)`, and per-point pixel RMSE. Invalid-depth rows have NaN residuals. Finite positive-depth points remain usable even outside an image; no image size is supplied.

RMSE is the square root of the mean **squared 2D residual norm** over valid rows. If none are valid, return `rmse=None`. Support `N=0`. Reject malformed intrinsics, shapes, nonfinite values, or complex inputs. Preserve inputs.

This diagnostic does not estimate calibration parameters or reject correspondences by an arbitrary error threshold.

See [examples](examples.md), [theory](theory.md), and [hints](hints.md).
