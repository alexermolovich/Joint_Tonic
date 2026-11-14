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

def source_embodiment_metrics(source_ids,embodiment_ids,success,latency_ms,num_embodiments):
    s=_array(source_ids,1,"int");e=_array(embodiment_ids,1,"int");y=_array(success,1,"bool");t=_array(latency_ms,1);g=_scalar(num_embodiments,1,16,True)
    if len(s)>10000 or any(v.shape!=s.shape for v in [e,y,t]) or (s<0).any() or (s>2).any() or (e<0).any() or (e>=g).any() or (t<0).any():raise ValueError("evaluation slices")
    count=np.zeros((3,g),dtype=np.int64);rate=np.full((3,g),np.nan);lat=np.full((3,g),np.nan)
    for a in range(3):
        for b in range(g):
            use=(s==a)&(e==b);n=int(use.sum());count[a,b]=n
            if n:rate[a,b]=y[use].mean();lat[a,b]=np.sort(t[use])[(95*n+99)//100-1]
    return {'count':count,'success_rate':rate,'p95_latency_ms':lat,'overall_success':float(y.mean()) if len(y) else None,'worst_observed_success':float(np.nanmin(rate)) if len(y) else None}
