# Apply an SE(3) Transform to Batched Points

A depth camera reports a grasp point in its own coordinate frame. The robot planner needs that point in the world frame. Implement `transform_points(T, points)` to apply the supplied camera-to-world rigid transform to one point or a whole batch.

## Function contract

```python
def transform_points(T, points) -> np.ndarray:
    ...
```

- `T`: finite real numeric array-like of shape `(4, 4)`. Its upper-left block is a proper 3D rotation; its last column contains translation in meters. It maps **camera coordinates into world coordinates**.
- `points`: finite real numeric array-like, either one point `(3,)` or a row-batched array `(N, 3)`, including `(0, 3)`.
- Return a float64 NumPy array of the same shape as `points`, containing world-frame coordinates in meters. The output must not share writable storage with either input.
- Both frames are right-handed. The transform is static, and the points are synchronized with that calibration. No perspective division is needed.

Raise `ValueError` if either shape is invalid, any value is nonfinite, the bottom row differs from `[0,0,0,1]`, the rotation is not orthonormal, or its determinant is not +1. Use `atol=1e-7, rtol=0` for those three rigid-transform checks. Do not mutate inputs. Use vectorized NumPy operations across points.

## Example 1: translation

```python
T = [[1,0,0,1], [0,1,0,-2], [0,0,1,3], [0,0,0,1]]
points = [[0,0,0], [2,1,-1]]
# array([[1., -2., 3.], [3., -1., 2.]])
```

The camera origin is located at world position `(1,-2,3)`. Its second point is offset by `(2,1,-1)` from that origin.

## Example 2: rotation followed by translation

```python
T = [[0,-1,0,1], [1,0,0,2], [0,0,1,0], [0,0,0,1]]
points = [1,0,0]
# array([1., 3., 0.])
```

The rotation sends the camera x-axis to the world y-axis. Translation then moves `(0,1,0)` to `(1,3,0)`.

## Constraints

`0 <= N <= 100_000`; coordinate and translation magnitudes are at most `1e6`. Inputs are real numeric lists or arrays on CPU. A bare empty list is not a correctly shaped batch; use `np.empty((0,3))`.

## Hints

1. Extract the rotation and translation from `T` before applying them.
2. A row of coordinates uses the transpose of the column-vector rotation formula.
