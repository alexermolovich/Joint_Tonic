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

def gate_policy_update(success,safety_violation,assisted,valid,current_version,candidate_version,min_autonomous_trials,allowed_success_drop,max_violation_rate):
    s=_array(success,2,"bool");v=_array(safety_violation,2,"bool");h=_array(assisted,2,"bool");m=_array(valid,2,"bool")
    if any(type(x) is not int or not low<=x<=high for x,low,high in [(current_version,0,10**9),(candidate_version,0,10**9),(min_autonomous_trials,1,4096)]):raise ValueError("version or trial bound")
    drop=_scalar(allowed_success_drop,0,1);limit=_scalar(max_violation_rate,0,1)
    if s.shape[0]!=2 or s.shape[1]>4096 or v.shape!=s.shape or h.shape!=s.shape or m.shape!=s.shape:raise ValueError("autonomy evidence shape")
    evidence=m&~h;n=evidence.sum(axis=1,dtype=np.int64);sr=np.divide((s&evidence).sum(axis=1),n,out=np.full(2,np.nan),where=n>0);vr=np.divide((v&evidence).sum(axis=1),n,out=np.full(2,np.nan),where=n>0);checks=np.array([candidate_version>current_version,(n>=min_autonomous_trials).all(),sr[1]>=sr[0]-drop,vr[1]<=limit],bool)
    return {'counts':n,'success_rate':sr,'violation_rate':vr,'checks':checks,'accepted':bool(checks.all())}
