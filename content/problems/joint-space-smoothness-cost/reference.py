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

def smoothness_cost(path,weights):
    q=_array(path,2);w=_array(weights,1);t,d=q.shape
    if not 1<=t<=4096 or not 1<=d<=16 or w.shape!=(d,) or np.any(w<0):raise ValueError("path contract")
    delta=np.diff(q,axis=0);g=np.zeros_like(q);edge=2*delta*w;g[:-1]-=edge;g[1:]+=edge
    return dict(cost=float(np.sum(delta*delta*w)),gradient=g)
