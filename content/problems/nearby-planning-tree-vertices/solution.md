# Solution

O(ND) time and memory. Compute one squared distance per row, filter by an inclusive radius, and preserve original index order.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Scalar outside contract")
    return float(x)

def nearby_vertices(vertices,query,weights,radius):
    v=_array(vertices,2);q=_array(query,1);w=_array(weights,1);r=_scalar(radius,0,1e6);n,d=v.shape
    if not 0<=n<=100000 or not 1<=d<=16 or q.shape!=(d,) or w.shape!=(d,) or np.any(w<1e-9):raise ValueError("metric contract")
    squared=np.sum((v-q)**2*w,axis=1);ids=np.flatnonzero(squared<=r*r).astype(np.int64)
    return ids,np.sqrt(squared[ids])
```
