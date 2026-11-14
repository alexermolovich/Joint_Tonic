# Solution

O(KHD) time and O(KHD) input validation footprint, with O(HD) outputs. Reduce only the rollout axis, clip each command, and copy the selected action before constructing the shifted plan.

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

def update_control_plan(controls,perturbations,weights,lower,upper):
    u=_array(controls,2);e=_array(perturbations,3);w=_array(weights,1);lo=_array(lower,1);hi=_array(upper,1);h,d=u.shape;k=len(e)
    if not 1<=h<=128 or not 1<=d<=16 or not 1<=k<=256 or e.shape!=(k,h,d) or w.shape!=(k,) or lo.shape!=(d,) or hi.shape!=(d,) or np.any(w<0) or abs(float(w.sum())-1)>1e-9 or np.any(lo>hi):raise ValueError("control plan contract")
    updated=np.clip(u+np.einsum('k,khd->hd',w,e),lo,hi)
    return dict(updated=updated,action=updated[0].copy(),next_plan=np.concatenate([updated[1:],updated[-1:]],axis=0))
```
