# Solution

Compute the affine layer, apply ReLU, and reduce over the point axis. Time O(NDF); returned feature storage O(NF).

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def point_mlp(points, weights, bias):
    p=_array(points,2); w=_array(weights,2); b=_array(bias,1)
    if not (1<=p.shape[0]<=4096 and 1<=p.shape[1]<=128 and w.shape[0]==p.shape[1] and 1<=w.shape[1]<=128 and b.shape==(w.shape[1],)):
        raise ValueError("Incompatible point features")
    local=np.maximum(p@w+b,0.)
    return local,local.max(axis=0)
```
