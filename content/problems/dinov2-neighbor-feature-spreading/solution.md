# Reference solution

Normalize rows, compute pairwise Euclidean distances, mask the diagonal to infinity, choose the smallest-index minimum, then clamp only the logarithm argument.

Reusable visual features should distinguish different scenes before a robot policy consumes them. Accidentally selecting each feature as its own neighbor makes every distance zero and destroys the intended learning signal.

```python
import numpy as np
import math

def array(x, ndim, dtype=np.float64):
    if not isinstance(x,np.ndarray) or x.dtype != np.dtype(dtype) or x.ndim != ndim or x.size>2000000:
        raise ValueError("Invalid array type, dtype, rank or size")
    if dtype != np.bool_ and (not np.isfinite(x).all() or np.any(np.abs(x.astype(float))>1e6)):
        raise ValueError("Nonfinite or out-of-range data")
    return x

def check(ok):
    if not ok: raise ValueError("Contract violation")

def real(x, low, high):
    check(type(x) in (int,float) and math.isfinite(x) and low<=x<=high)
    return x

def integer(x, low, high):
    check(type(x) is int and low<=x<=high)
    return x

def neighbor_spreading(features, epsilon):
    array(features,2);real(epsilon,1e-8,.1)
    n,d=features.shape;check(2<=n<=128 and 1<=d<=64)
    norm=np.linalg.norm(features,axis=1,keepdims=True);check(np.all(norm>=1e-9))
    unit=features/norm;distance=np.linalg.norm(unit[:,None]-unit[None],axis=-1)
    np.fill_diagonal(distance,np.inf);neighbors=np.argmin(distance,axis=1).astype(np.int64)
    distances=distance[np.arange(n),neighbors]
    return dict(loss=float(-np.log(np.maximum(distances,epsilon)).mean()),distances=distances,neighbors=neighbors)
```
