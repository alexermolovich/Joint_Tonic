# Solution

O(D) time and output memory. Compute the three polynomials independently from the initial state; do not update acceleration before using its original value in velocity.

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

def integrate_jerk(position,velocity,acceleration,jerk,duration):
    q=_array(position,1);v=_array(velocity,1);a=_array(acceleration,1);j=_array(jerk,1);t=_scalar(duration,0,100)
    if not 1<=len(q)<=64 or v.shape!=q.shape or a.shape!=q.shape or j.shape!=q.shape:raise ValueError("joint shape")
    return dict(position=q+v*t+.5*a*t*t+j*t*t*t/6,velocity=v+a*t+.5*j*t*t,acceleration=a+j*t)
```
