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

def sensor_readiness(present,timestamps,now,max_age,required):
    p=_array(present,2,"bool");s=_array(timestamps,2);t=_array(now,1);a=_array(max_age,1);r=_array(required,1,"bool")
    b,m=p.shape
    if not 1<=b<=64 or not 1<=m<=32 or s.shape!=p.shape or t.shape!=(b,) or a.shape!=(m,) or r.shape!=(m,) or any((x<0).any() for x in [s,t,a]):raise ValueError("invalid sensor contract")
    stale=p&((s>t[:,None])|(t[:,None]-s>a));usable=p&~stale
    return {'usable':usable,'stale':stale,'ready':((~r)|usable).all(axis=1)}
