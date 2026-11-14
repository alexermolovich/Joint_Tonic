# Worked code examples

The snippets print lists from the returned NumPy arrays. `nan` is the invalid-pixel marker specified by the contract.

## Example 1: projection and the right boundary

```python
from solution import project_points

K = [[100,0,50], [0,100,40], [0,0,1]]
pixels, depths, valid = project_points(
    [[0,0,2], [1,-0.5,2]], K, (100,80)
)
print(pixels.tolist())
print(depths.tolist())
print(valid.tolist())
```

Expected output:

```text
[[50.0, 40.0], [100.0, 15.0]]
[2.0, 2.0]
[True, False]
```

The second point has positive depth but lands at `u=width`, outside the image. Its coordinates are retained rather than clipped.

## Example 2: behind the camera and on the top-left corner

```python
from solution import project_points

K = [[100,0,50], [0,100,40], [0,0,1]]
pixels, depths, valid = project_points(
    [[0,0,-1], [-1,-0.8,2]], K, (100,80)
)
print(pixels.tolist())
print(depths.tolist())
print(valid.tolist())
```

Expected output:

```text
[[nan, nan], [0.0, 0.0]]
[-1.0, 2.0]
[False, True]
```

Negative depth has no forward-facing projection. The included left/top boundary is valid.

## Example 3: an empty point batch stays aligned

```python
import numpy as np
from solution import project_points

pixels, depths, valid = project_points(
    np.empty((0,3)), np.eye(3), (10,10)
)
print(pixels.shape, depths.shape, valid.shape)
```

Expected output:

```text
(0, 2) (0,) (0,)
```

An empty batch is a valid array with explicit coordinate dimensions, not a malformed bare list.
