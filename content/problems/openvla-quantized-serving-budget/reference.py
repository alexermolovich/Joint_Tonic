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

def serving_budget(parameter_count,bits,overhead_bytes,kv_bytes,latency_ms,memory_limit,deadline_ms):
    if type(parameter_count)!=int or not 1<=parameter_count<=10**12 or type(memory_limit)!=int or not 0<=memory_limit<=10**13:raise ValueError("memory scalar")
    b=_array(bits,1,"int");o=_array(overhead_bytes,1,"int");k=_array(kv_bytes,1,"int");l=_array(latency_ms,2);d=_scalar(deadline_ms,np.nextafter(0,1),1e6)
    if not 1<=len(b)<=128 or not np.isin(b,[4,8,16,32]).all() or o.shape!=b.shape or k.shape!=b.shape or (o<0).any() or (k<0).any() or l.shape[0]!=len(b) or not 1<=l.shape[1]<=4096 or (l<=0).any():raise ValueError("serving table")
    weights=(parameter_count*b+7)//8;total=weights+o+k;rank=(95*l.shape[1]+99)//100-1;p95=np.sort(l,axis=1)[:,rank].copy()
    return {'weight_bytes':weights,'total_bytes':total,'p95_latency_ms':p95,'feasible':(total<=memory_limit)&(p95<=d)}
