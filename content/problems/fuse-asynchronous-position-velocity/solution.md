# Solution

Validate the event stream, then perform fixed-size prediction and Joseph update per event. O(N) time and output memory; no interpolation of the measurements.

```python
import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def _cov(value, n, positive=False):
    a=_real(value)
    if a.shape!=(n,n) or not np.allclose(a,a.T,rtol=0,atol=1e-10): raise ValueError("Invalid covariance shape or symmetry")
    a=(a+a.T)/2
    eig,vectors=np.linalg.eigh(a)
    if np.any(eig< -1e-10) or (positive and np.any(eig<=1e-10)): raise ValueError("Invalid covariance spectrum")
    return (vectors*np.maximum(eig,0))@vectors.T if np.any(eig<0) else a

def fuse_async_sensors(x, P, start_time, events, variances, spectral_density):
    x,t,events,var,q=map(_real,(x,start_time,events,variances,spectral_density))
    if x.shape!=(2,) or t.ndim!=0 or events.ndim!=2 or events.shape[1]!=3 or var.shape!=(len(events),) or np.any(var<=1e-10) or q.ndim!=0 or q<0: raise ValueError("Invalid fusion inputs")
    if np.any(events[:,0]<t) or np.any(np.diff(events[:,0])<0) or np.any(~np.isin(events[:,1],[0,1])): raise ValueError("Invalid event times or kinds")
    P=_cov(P,2); x=x.copy(); means=np.empty((len(events),2)); covs=np.empty((len(events),2,2))
    for i,((stamp,kind,value),noise) in enumerate(zip(events,var)):
        dt=stamp-t; F=np.array([[1.,dt],[0.,1.]])
        Q=q*np.array([[dt**3/3,dt**2/2],[dt**2/2,dt]])
        x=F@x; P=F@P@F.T+Q; j=int(kind); K=P[:,j]/(P[j,j]+noise)
        x=x+K*(value-x[j]); H=np.eye(2)[j]; A=np.eye(2)-np.outer(K,H)
        P=A@P@A.T+noise*np.outer(K,K); P=(P+P.T)/2
        means[i],covs[i]=x,P; t=stamp
    return means,covs
```
