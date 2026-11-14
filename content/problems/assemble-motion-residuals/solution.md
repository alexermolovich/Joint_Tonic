# Solution

Compute the hinge, divide by sigma once, concatenate in the required order, and retain the separate costs for diagnostics. O(P+N) time and memory.

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

def assemble_residuals(prior,clearances,margin,obstacle_sigma):
    p=_array(prior,1);d=_array(clearances,1);e=_scalar(margin,0,100);s=_scalar(obstacle_sigma,1e-6,1e6)
    if len(p)>65536 or len(d)>65536:raise ValueError("factor count")
    h=np.maximum(e-d,0)/s;pc=float(.5*np.dot(p,p));oc=float(.5*np.dot(h,h))
    return dict(residual=np.concatenate([p,h]),prior_cost=pc,obstacle_cost=oc,total_cost=pc+oc)
```
