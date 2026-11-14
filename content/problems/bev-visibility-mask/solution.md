# Solution

Combine three broadcast comparisons. Time and returned storage O(CN).

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def bev_visibility(uv, depth, image_sizes):
    u=_array(uv,3);z=_array(depth,2);s=_array(image_sizes,2,"i")
    if u.shape[2:]!=(2,) or not 1<=u.shape[0]<=16 or u.shape[1]>4096 or z.shape!=u.shape[:2] or s.shape!=(u.shape[0],2) or np.any(s<1) or np.any(s>100000):raise ValueError("Shape or size")
    return (z>1e-6)&(u[:,:,0]>=0)&(u[:,:,0]<s[:,1,None])&(u[:,:,1]>=0)&(u[:,:,1]<s[:,0,None])
```
