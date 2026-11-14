# Worked code examples

Each snippet runs independently after implementing the named function in `solution.py`. Printed lists make the values explicit; the function itself returns NumPy arrays.

## Example 1: translate two camera points

```python
from solution import transform_points

T = [[1,0,0,1], [0,1,0,-2], [0,0,1,3], [0,0,0,1]]
result = transform_points(T, [[0,0,0], [2,1,-1]])
print(result.tolist())
print(result.shape, str(result.dtype))
```

Expected output:

```text
[[1.0, -2.0, 3.0], [3.0, -1.0, 2.0]]
(2, 3) float64
```

The camera origin maps to the translation. The second row keeps its relative displacement because the rotation is identity.

## Example 2: rotate, then translate

```python
from solution import transform_points

T = [[0,-1,0,1], [1,0,0,2], [0,0,1,0], [0,0,0,1]]
print(transform_points(T, [1,0,0]).tolist())
```

Expected output:

```text
[1.0, 3.0, 0.0]
```

The camera x-axis becomes the world y-axis before adding the world-frame translation. A single point retains shape `(3,)`.

## Example 3: shape is not enough to make a rigid transform

```python
import numpy as np
from solution import transform_points

try:
    transform_points(np.diag([2.,1.,1.,1.]), [0,0,0])
except ValueError as error:
    print(type(error).__name__)
```

Expected output:

```text
ValueError
```

Scaling one axis changes physical distances, so this matrix is rejected before transforming points.
