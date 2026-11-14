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

def humanoid_release_gate(trials,successes,safety_incidents,p95_latency_ms,required,min_trials,min_success_rate,max_latency_ms):
    n=_array(trials,1,"int");k=_array(successes,1,"int");c=_array(safety_incidents,1,"int");t=_array(p95_latency_ms,1);r=_array(required,1,"bool");minimum=_scalar(min_trials,1,1e6,True);rate_min=_scalar(min_success_rate,0,1);deadline=_scalar(max_latency_ms)
    if not 1<=len(n)<=128 or any(v.shape!=n.shape for v in [k,c,t,r]) or not r.any() or (n<0).any() or (k<0).any() or (k>n).any() or (c<0).any() or (c>n).any() or (t<0).any():raise ValueError("release evidence")
    rates=np.full(len(n),np.nan);np.divide(k,n,out=rates,where=n>0);failed=[]
    for i in range(len(n)):
        reasons=[]
        if n[i]<minimum:reasons.append('insufficient_trials')
        if c[i]>0:reasons.append('safety_incident')
        if n[i]>0 and rates[i]<rate_min:reasons.append('low_success')
        if t[i]>deadline:reasons.append('latency')
        failed.append(reasons)
    passes=np.array([not v for v in failed],dtype=bool)
    return {'success_rate':rates,'slice_pass':passes,'failures':failed,'release':bool(passes[r].all())}
