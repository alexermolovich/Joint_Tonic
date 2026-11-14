# Solution

Compute masked sums and valid counts per view; report two metrics and their independent threshold gate. O(VN) time and O(VN) temporary storage.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def pose_diagnostics(pixel_residuals, color_residuals, valid, pixel_limit, color_limit):
    p=_array(pixel_residuals,3);c=_array(color_residuals,3);v=_array(valid,2,"b")
    if p.shape[2:]!=(2,) or not 1<=len(p)<=32 or p.shape[1]>4096 or c.shape!=(*p.shape[:2],3) or v.shape!=p.shape[:2] or np.any(np.abs(c)>1):raise ValueError("Residual shape/range")
    for x,hi in ((pixel_limit,1e6),(color_limit,1.)):
        if type(x) not in (int,float) or not 0<=x<=hi:raise ValueError("Threshold")
    n=v.sum(1);den=np.maximum(n,1)
    pr=np.sqrt(np.sum(np.sum(p*p,axis=2)*v,axis=1)/den)
    cr=np.sqrt(np.sum(np.sum(c*c,axis=2)*v,axis=1)/(3*den))
    return dict(pixel_rmse=pr,color_rmse=cr,observed=n>0,flagged=(n>0)&((pr>pixel_limit)|(cr>color_limit)))
```
