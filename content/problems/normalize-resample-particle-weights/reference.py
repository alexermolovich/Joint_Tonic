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

def resample_particles(weights, offset):
    w,u=map(_real,(weights,offset))
    if w.ndim!=1 or not 1<=len(w)<=100000 or np.any(w<0) or w.max()<=0 or u.ndim!=0 or not 0<=u<1: raise ValueError("Invalid weights or offset")
    scaled=w/w.max(); p=scaled/scaled.sum(); c=np.cumsum(p); c[-1]=1.
    positions=np.minimum((float(u)+np.arange(len(w)))/len(w),np.nextafter(1.,0.))
    return p,np.searchsorted(c,positions,side="right").astype(np.int64)
