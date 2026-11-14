# Solution

Maintain log-potentials instead of repeatedly scaling an exponentiated extreme matrix. Each iteration performs one row and one column log-sum-exp. O(iterations*N*M) time and O(NM+N+M) memory.

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

def sinkhorn_assignments(log_scores,row_mass,column_mass,iterations):
    s=_array(log_scores,2);a=_array(row_mass,1);b=_array(column_mass,1);n=_iterations(iterations)
    if not all(1<=v<=128 for v in s.shape) or np.any(np.abs(s)>100) or a.shape!=(s.shape[0],) or b.shape!=(s.shape[1],) or np.any((a<1e-9)|(a>1)) or np.any((b<1e-9)|(b>1)) or abs(a.sum()-1)>1e-9 or abs(b.sum()-1)>1e-9:raise ValueError("transport marginal contract")
    a=a/a.sum();b=b/b.sum();logp=_transport(s,a,b,n);p=np.exp(logp)
    return dict(log_transport=logp,transport=p,row_error=float(np.max(np.abs(p.sum(axis=1)-a))),column_error=float(np.max(np.abs(p.sum(axis=0)-b))))
```
