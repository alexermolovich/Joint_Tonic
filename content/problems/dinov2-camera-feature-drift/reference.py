import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def feature_drift(reference, current):
    r=_array(reference,2);c=_array(current,2)
    if not (1<=len(r)<=4096 and 1<=len(c)<=4096 and 1<=r.shape[1]<=256) or c.shape[1]!=r.shape[1]:raise ValueError("Feature shape")
    shift=(c.mean(0)-r.mean(0))/np.sqrt(r.var(0)+1e-6)
    return shift,float(np.sqrt(np.mean(shift*shift)))
