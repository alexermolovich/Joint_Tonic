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

def bound_trust_step(current,proposal,lower,upper,radius):
    q=_array(current,1);p=_array(proposal,1);lo=_array(lower,1);hi=_array(upper,1);r=_scalar(radius,0,100)
    if not 1<=len(q)<=64 or p.shape!=q.shape or lo.shape!=q.shape or hi.shape!=q.shape or np.any(lo>q) or np.any(q>hi):raise ValueError("joint bounds")
    step=np.clip(p,np.maximum(lo-q,-r),np.minimum(hi-q,r))
    return dict(step=step,next_configuration=q+step,clipped=p!=step)
