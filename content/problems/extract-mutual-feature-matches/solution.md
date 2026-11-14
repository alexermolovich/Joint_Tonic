# Solution

Choose row and column maxima on the real block, apply reciprocal-index and strict confidence gates, and scatter accepted pairs into original-index labels. O(NM) time and O(N+M) auxiliary memory.

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

def mutual_matches(assignment,threshold):
    p=_array(assignment,2);tau=_scalar(threshold,0,1e6);n=p.shape[0]-1;m=p.shape[1]-1
    if not 0<=n<=1024 or not 0<=m<=1024 or n*m>262144 or np.any(p<0):raise ValueError("mutual assignment contract")
    ma=np.full(n,-1,np.int64);mb=np.full(m,-1,np.int64);ca=np.zeros(n);cb=np.zeros(m);pairs=np.empty((0,2),np.int64)
    if n and m:
        real=p[:n,:m];j=np.argmax(real,axis=1);i=np.argmax(real,axis=0);rows=np.arange(n);valid=(i[j]==rows)&(real[rows,j]>tau);selected=rows[valid];targets=j[valid];ma[selected]=targets;mb[targets]=selected;ca[selected]=real[selected,targets];cb[targets]=ca[selected];pairs=np.column_stack([selected,targets])
    return dict(matches_source=ma,matches_target=mb,confidence_source=ca,confidence_target=cb,pairs=pairs)
```
