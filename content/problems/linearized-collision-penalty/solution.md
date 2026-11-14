# Solution

O(ND) time and memory. Compute the affine clearance prediction, select strictly active hinges, then sum their negative Jacobian rows.

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

def linearized_collision_penalty(distances,jacobian,step,margin):
    d=_array(distances,1);j=_array(jacobian,2);s=_array(step,1);m=_scalar(margin,0,100)
    if not 0<=len(d)<=4096 or not 1<=len(s)<=16 or j.shape!=(len(d),len(s)):raise ValueError("linearization contract")
    predicted=d+j@s;hinge=np.maximum(m-predicted,0);gradient=-j[predicted<m].sum(axis=0)
    return dict(predicted=predicted,hinge=hinge,cost=float(hinge.sum()),gradient=gradient)
```
