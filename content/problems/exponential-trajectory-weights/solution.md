# Solution

O(N) time and memory. Mask before finding the stabilizing minimum; an invalid low-cost rollout must not affect normalization or best-index selection.

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

def trajectory_weights(costs,valid,temperature):
    c=_array(costs,1);mask=_array(valid,1,"b");t=_scalar(temperature,1e-6,1e6)
    if not 1<=len(c)<=16384 or mask.shape!=c.shape or not mask.any():raise ValueError("rollout support")
    best=int(np.argmin(np.where(mask,c,np.inf)));w=np.zeros_like(c);w[mask]=np.exp(-(c[mask]-c[best])/t);w/=w.sum()
    return dict(weights=w,effective_samples=float(1/np.sum(w*w)),best_index=best)
```
