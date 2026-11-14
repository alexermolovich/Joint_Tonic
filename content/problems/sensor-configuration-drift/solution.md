# Solution

Intersect availability first, then compute Euclidean errors and aggregates on that shared support. Time/storage O(CN).

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x,low,high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def compare_drift(estimated, reference, valid, baseline):
    x=_array(estimated,3);ref=_array(reference,2);mask=_array(valid,2,"b");c,n,d=x.shape
    if not 1<=c<=64 or not 1<=n<=8192 or c*n>262144 or d!=3 or ref.shape!=(n,3) or mask.shape!=(c,n) or type(baseline) is not int or not 0<=baseline<c:raise ValueError("drift comparison contract")
    common=np.all(mask,axis=0);count=int(common.sum());errors=np.full((c,n),np.nan);rmse=np.full(c,np.nan);endpoint=np.full(c,np.nan)
    if count:
        errors[:,common]=np.linalg.norm(x[:,common]-ref[common],axis=2);rmse=np.sqrt(np.mean(errors[:,common]**2,axis=1));endpoint=errors[:,np.flatnonzero(common)[-1]].copy()
    return dict(common=common,count=count,errors=errors,rmse=rmse,endpoint=endpoint,improvement=rmse[baseline]-rmse,best=int(np.argmin(rmse)) if count else -1)
```
