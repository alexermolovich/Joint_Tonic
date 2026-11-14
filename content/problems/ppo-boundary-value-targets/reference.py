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

def boundary_value_targets(rewards,next_values,terminated,truncated,valid,gamma,lam):
    r=_array(rewards,2);v=_array(next_values,2);d=_array(terminated,2,"bool");c=_array(truncated,2,"bool");m=_array(valid,2,"bool");g=_scalar(gamma,0,1);l=_scalar(lam,0,1)
    if not 1<=r.shape[0]<=32 or not 1<=r.shape[1]<=1024 or any(x.shape!=r.shape for x in [v,d,c,m]) or (d&c).any() or ((d|c)&~m).any() or ((~m[:,:-1])&m[:,1:]).any():raise ValueError("rollout boundary contract")
    out=np.zeros_like(r)
    for t in range(r.shape[1]-1,-1,-1):
        carry=v[:,t]
        if t+1<r.shape[1]:carry=np.where(m[:,t+1]&~d[:,t]&~c[:,t],out[:,t+1],carry)
        out[:,t]=np.where(m[:,t],r[:,t]+g*(~d[:,t])*((1-l)*v[:,t]+l*carry),0.)
    return out
