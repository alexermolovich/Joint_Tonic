import numpy as np

def _array(value, ndim=None, kind="real"):
    try: a=np.asarray(value)
    except (ValueError,TypeError,OverflowError) as e: raise ValueError("invalid array") from e
    if ndim is not None and a.ndim!=ndim: raise ValueError("invalid rank")
    if a.size>1000000: raise ValueError("array too large")
    if kind=="bool":
        if a.dtype.kind!='b': raise ValueError("boolean array required")
        return a.copy()
    if kind=="int":
        if a.dtype.kind not in 'iu': raise ValueError("integer array required")
    elif a.dtype.kind not in 'iuf': raise ValueError("real numeric array required")
    if not np.isfinite(a).all() or (np.abs(a.astype(np.float64))>1e6).any(): raise ValueError("invalid numeric values")
    return a.astype(np.int64 if kind=="int" else np.float64)

def _scalar(x,low=0,high=1e6,integer=False):
    if isinstance(x,(bool,np.bool_)) or not isinstance(x,(int,float,np.integer,np.floating)): raise ValueError("numeric scalar required")
    if integer and not isinstance(x,(int,np.integer)): raise ValueError("integer scalar required")
    if not low<=x<=high or not np.isfinite(x): raise ValueError("scalar outside bounds")
    return int(x) if integer else float(x)

def teleop_quality_flags(times,joints,observed,lower,upper,max_speed):
    t=_array(times,1);q=_array(joints,2);obs=_array(observed,1,"bool");lo=_array(lower,1);hi=_array(upper,1);speed=_array(max_speed,1)
    if not 1<=len(t)<=4096 or not 1<=q.shape[1]<=64 or q.shape[0]!=len(t) or obs.shape!=t.shape or any(v.shape!=(q.shape[1],) for v in [lo,hi,speed]) or (np.diff(t)<=0).any() or (lo>=hi).any() or (speed<=0).any(): raise ValueError("unaligned or invalid quality inputs")
    jump=np.zeros(len(t),dtype=bool)
    jump[1:]=(np.abs(np.diff(q,axis=0))/np.diff(t)[:,None]>speed).any(axis=1)
    return {'missing':~obs,'out_of_range':((q<lo)|(q>hi)).any(axis=1),'speed_jump':jump}
