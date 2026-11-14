# Solution

Validate cumulative incumbent consistency per seed using the last observed solved state. Summarize each column, then form pairs only across adjacent columns where both entries are solved. O(SB+BS log S) time for medians and O(SB) temporary memory.

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

def compare_budgets(budgets,costs,observed,solved):
    b=_array(budgets,1,"i");c=_array(costs,2);obs=_array(observed,2,"b");ok=_array(solved,2,"b");s,n=c.shape
    if not 1<=len(b)<=128 or not 1<=s<=256 or n!=len(b) or obs.shape!=c.shape or ok.shape!=c.shape or np.any((b<1)|(b>10**9)) or np.any(np.diff(b)<=0) or np.any(c<0) or np.any(ok&~obs):raise ValueError("budget observations")
    for i in range(s):
        found=False;last=0.
        for j in range(n):
            if not obs[i,j]:continue
            if found and (not ok[i,j] or c[i,j]>last):raise ValueError("incumbent regression")
            if ok[i,j]:found=True;last=c[i,j]
    counts=obs.sum(axis=0,dtype=np.int64);rate=np.full(n,np.nan);np.divide(ok.sum(axis=0),counts,out=rate,where=counts>0)
    med=np.array([np.median(c[ok[:,j],j]) if ok[:,j].any() else np.nan for j in range(n)])
    pairs=ok[:,:-1]&ok[:,1:];pc=pairs.sum(axis=0,dtype=np.int64);gain=np.full(n-1,np.nan);np.divide(np.where(pairs,c[:,:-1]-c[:,1:],0).sum(axis=0),pc,out=gain,where=pc>0)
    return dict(counts=counts,success_rate=rate,median_solved_cost=med,paired_counts=pc,paired_improvement=gain)
```
