# Solution

Build the augmented score matrix and unequal bin capacities, solve the fixed log-Sinkhorn recurrence, then compare the bin entry against real assignments. O(iterations*(N+1)*(M+1)) time and O(NM) memory.

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

def _logsumexp(x,axis):
    maximum=np.max(x,axis=axis,keepdims=True)
    return (maximum+np.log(np.sum(np.exp(x-maximum),axis=axis,keepdims=True))).squeeze(axis)

def _transport(s,a,b,iterations):
    u=np.zeros(len(a));v=np.zeros(len(b))
    for _ in range(iterations):
        u=np.log(a)-_logsumexp(s+v[None,:],1)
        v=np.log(b)-_logsumexp(s+u[:,None],0)
    return s+u[:,None]+v[None,:]

def _iterations(n):
    if type(n) is not int or not 1<=n<=200:raise ValueError("iterations contract")
    return n

def dustbin_assignment(scores,dustbin_score,iterations):
    s=_array(scores,2);bin_score=_scalar(dustbin_score,-100,100);count=_iterations(iterations);n,m=s.shape
    if not 1<=n<=128 or not 1<=m<=128 or np.any(np.abs(s)>100):raise ValueError("dustbin score contract")
    augmented=np.full((n+1,m+1),bin_score);augmented[:n,:m]=s;a=np.r_[np.ones(n),float(m)]/(n+m);b=np.r_[np.ones(m),float(n)]/(n+m)
    assignment=np.exp(_transport(augmented,a,b,count))*(n+m)
    return dict(assignment=assignment,row_unmatched=assignment[:n,m]>np.max(assignment[:n,:m],axis=1),column_unmatched=assignment[n,:m]>np.max(assignment[:n,:m],axis=0))
```
