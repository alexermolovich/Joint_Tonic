import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def fuse_bev(current, history, history_valid, gate, reset):
    x=_array(current,3);h=_array(history,3);v=_array(history_valid,2,"b");g=_array(gate,2)
    if not (1<=x.shape[0]<=128 and 1<=x.shape[1]<=128 and 1<=x.shape[2]<=64) or h.shape!=x.shape or v.shape!=x.shape[:2] or g.shape!=v.shape or np.any(g<0) or np.any(g>1) or type(reset) is not bool:raise ValueError("Fusion contract")
    effective=np.where(v & (not reset),g,0.)[:,:,None]
    return (1-effective)*x+effective*h
