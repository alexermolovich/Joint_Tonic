# Project Camera Points into Pixels

Your robot has a calibrated pinhole camera. Implement `project_points(points, K, image_size)` to find each 3D point's image coordinates, retain its depth, and identify points that project inside the image.

## Contract

```python
def project_points(points, K, image_size):
    # Return (pixels, depths, valid)
    ...
```

- `points`: finite real numeric `(N,3)` array in **camera optical coordinates**, in meters. x points right, y down, z forward. Support `N=0`.
- `K`: finite real `(3,3)` zero-skew pinhole intrinsics `[[fx,0,cx],[0,fy,cy],[0,0,1]]`. Both focal lengths must be positive. Check the fixed entries with `atol=1e-9,rtol=0`. Principal point may lie outside the image.
- `image_size`: `(width,height)` of positive integer values; booleans are invalid.
- `pixels`: new float64 `(N,2)` array, in `(u,v)` order, measured in pixels. For `z<=1e-8`, set **both** coordinates to `NaN`. For larger depths, project even if the result lies outside the image.
- `depths`: new float64 `(N,)` array containing original z, including nonpositive z.
- `valid`: bool `(N,)`; true exactly when `z>1e-8`, `0<=u<width`, and `0<=v<height`.

Do not mutate inputs or return writable aliases of them. Raise `ValueError` for invalid shapes, intrinsics, image size, complex data, or nonfinite values. Distortion, occlusion, and camera motion are excluded.

## Example 1: center and image edge

```python
K = [[100,0,50], [0,100,40], [0,0,1]]
points = [[0,0,2], [1,-0.5,2]]
image_size = (100,80)
# pixels: [[50.,40.], [100.,15.]]
# depths: [2.,2.]
# valid: [True,False]
```

The second point lands exactly at `u=width`, outside the half-open pixel range.

## Example 2: behind and in front of the camera

```python
points = [[0,0,-1], [-1,-0.8,2]]
# Same K and image_size
# pixels: [[nan,nan], [0.,0.]]
# depths: [-1.,2.]
# valid: [False,True]
```

The left/top boundary is included. A negative depth has no forward-facing pixel projection under this contract.

## Constraints and hints

`0<=N<=100_000`; coordinate magnitudes <=1e6; positive depths used in division exceed 1e-8. Intrinsic magnitudes <=1e6. Use vectorized masked division, then a separate bounds test. Width controls u; height controls v.
