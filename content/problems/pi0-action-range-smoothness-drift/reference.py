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

def action_drift(actions,timestamps,lower,upper,max_speed,baseline_rate):
    a=_array(actions,2);t=_array(timestamps,1);lo,hi,v,base=[_array(x,1) for x in [lower,upper,max_speed,baseline_rate]];n,d=a.shape
    if not 1<=n<=4096 or not 1<=d<=32 or t.shape!=(n,) or any(x.shape!=(d,) for x in [lo,hi,v,base]) or (t<0).any() or (np.diff(t)<=0).any() or (lo>hi).any() or (v<0).any() or (base<0).any() or (base>1).any():raise ValueError("monitor contract")
    r=(a<lo)|(a>hi);s=np.zeros_like(r);s[1:]=np.abs(np.diff(a,axis=0))/np.diff(t)[:,None]>v;rate=(r|s).mean(axis=0)
    return {'range_violation':r,'speed_violation':s,'rate':rate,'drift':rate-base}
