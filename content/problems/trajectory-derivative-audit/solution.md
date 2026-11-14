# Solution

O(ND) time and memory. Stack derivative orders explicitly, compare absolute magnitudes, and preserve the difference between no evidence and evidence below the limit.

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

def audit_derivatives(velocity,acceleration,jerk,limits):
    v=_array(velocity,2);a=_array(acceleration,2);j=_array(jerk,2);lim=_array(limits,2);n,d=v.shape
    if not 0<=n<=4096 or not 1<=d<=16 or a.shape!=v.shape or j.shape!=v.shape or lim.shape!=(3,d) or np.any(lim<1e-9):raise ValueError("derivative contract")
    values=np.abs(np.stack([v,a,j],axis=0));violations=(values>lim[:,None,:]).transpose(1,2,0).copy();ratio=np.max(values,axis=1)/lim if n else np.zeros((3,d))
    return dict(violations=violations,max_ratio=ratio,passed=bool(n and not violations.any()))
```
