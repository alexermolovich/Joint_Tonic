import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def detector_frontier(accuracy, latency_ms, budget_ms):
    a=_array(accuracy,1);l=_array(latency_ms,1)
    if l.shape!=a.shape or len(a)>2048 or np.any(a<0) or np.any(a>1) or np.any(l<=0) or type(budget_ms) not in (int,float) or not 0<budget_ms<=1e6:raise ValueError("Benchmark contract")
    dominated=np.any((a[:,None]>=a[None,:])&(l[:,None]<=l[None,:])&((a[:,None]>a[None,:])|(l[:,None]<l[None,:])),axis=0)
    feasible=np.flatnonzero(l<=budget_ms)
    best=min(feasible,key=lambda i:(-a[i],l[i],int(i))) if len(feasible) else -1
    return np.flatnonzero(~dominated).astype(np.int64),int(best)
