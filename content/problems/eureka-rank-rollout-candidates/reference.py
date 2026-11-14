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

def rank_reward_candidates(success,safety_violation,valid,min_trials,max_violation_rate):
    s=_array(success,2,"bool");v=_array(safety_violation,2,"bool");m=_array(valid,2,"bool")
    if type(min_trials) is not int:raise ValueError("built-in trial count")
    low=_scalar(min_trials,1,4096,True);limit=_scalar(max_violation_rate,0,1)
    if not 1<=len(s)<=128 or s.shape[1]>4096 or v.shape!=s.shape or m.shape!=s.shape:raise ValueError("rollout shape")
    n=m.sum(axis=1,dtype=np.int64);sr=np.divide((m&s).sum(axis=1),n,out=np.full(len(s),np.nan),where=n>0);vr=np.divide((m&v).sum(axis=1),n,out=np.full(len(s),np.nan),where=n>0);eligible=(n>=low)&(vr<=limit);ids=np.flatnonzero(eligible);order=ids[np.lexsort((ids,-n[ids],vr[ids],-sr[ids]))]
    return {'count':n,'success_rate':sr,'violation_rate':vr,'eligible':eligible,'order':order,'selected':int(order[0]) if len(order) else -1}
