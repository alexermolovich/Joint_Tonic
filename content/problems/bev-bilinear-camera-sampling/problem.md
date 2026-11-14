# Sample Calibrated Multi-Camera Feature Maps

A projected location usually lies between feature-map cells. Bilinear sampling blends nearby cells while preserving a camera-specific validity decision. Projection and calibration are supplied by the caller; this function only gathers aligned visual evidence.

```python
def sample_camera_features(features, coordinates, valid):
    ...
```

## Function contract

Inputs: `features: float64(C, H, W, D)`, `coordinates: float64(C, N, 2)` and `valid: bool(C, N)`. Bounds: `1<=C<=8`, `1<=H, W<=64`, `1<=D<=32`, `0<=N<=4096`. The maximum feature tensor has 1, 048, 576 entries and is supported.

Coordinates `(u, v)` are already projected feature-map pixel-center indices. The caller has applied camera calibration and image-to-feature scaling. Use a query only when its mask is true and it lies in the closed range `0<=u<=W-1`, `0<=v<=H-1`. Bilinearly interpolate four neighbors using floor indices and upper neighbors clipped to the final row/column. Out-of-view or masked queries return exact zero.

Return `samples: float64(C, N, D)` and `used: bool(C, N)`. Validate every coordinate, including unused ones. Cameras are synchronized; no cross-camera attention normalization or physical-frame transform occurs here.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** One camera has a single-channel map `[[0, 2],[4, 6]]`. A valid point `(u=.5, v=.5)` samples value `3`, with `used=True`.

**Example 2.** For the same map, points `(1, 1)` and `(1.1, 1)` produce samples `6` and `0`. The returned used mask is `[True, False]`; the second point is outside.

## Source and scope

Original bounded component based on [2022-bevformer](https://arxiv.org/abs/2203.17270). BEV perception combines evidence from calibrated cameras. Using original image coordinates directly on a downsampled feature map selects the wrong evidence. An out-of-view point must not be clipped into a plausible border observation.
