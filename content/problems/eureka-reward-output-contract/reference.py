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

def validate_reward_output(rewards,components,valid,reward_bound,atol):
    def evidence(value,rank):
        try:a=np.asarray(value)
        except (TypeError,ValueError,OverflowError) as e:raise ValueError("invalid evidence") from e
        if a.ndim!=rank or a.dtype.kind not in 'iuf' or a.size>1000000:raise ValueError("real evidence required")
        a=a.astype(np.float64)
        if (np.abs(a[np.isfinite(a)])>1e6).any():raise ValueError("finite evidence bounds")
        return a
    r=evidence(rewards,1);c=evidence(components,2);m=_array(valid,1,"bool");bound=_scalar(reward_bound,0,1e6);tol=_scalar(atol,0,1)
    if len(r)>4096 or c.shape[0]!=len(r) or not 1<=c.shape[1]<=32 or m.shape!=r.shape:raise ValueError("reward output contract")
    finite=np.isfinite(r)&np.isfinite(c).all(axis=1);safe_r=np.where(finite,r,0.);safe_c=np.where(finite[:,None],c,0.)
    bounded=finite&(np.abs(safe_r)<=bound)&(np.abs(safe_c)<=bound).all(axis=1);consistent=finite&(np.abs(safe_r-safe_c.sum(axis=1))<=tol);accepted=m&bounded&consistent
    return {'finite':finite,'bounded':bounded,'consistent':consistent,'accepted':accepted,'all_valid_accepted':bool(accepted[m].all()),'invalid_count':int((m&~accepted).sum())}
