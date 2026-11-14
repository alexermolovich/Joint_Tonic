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

def control_latency_report(observed_ms, applied_ms, deadline_ms):
    o=_array(observed_ms,1);a=_array(applied_ms,1);d=_scalar(deadline_ms,np.nextafter(0,1))
    if not 1<=len(o)<=10000 or a.shape!=o.shape or (o<0).any() or (np.diff(o)<=0).any(): raise ValueError("invalid timestamps")
    delivered=a!=-1
    if (a[delivered]<o[delivered]).any(): raise ValueError("action precedes observation")
    latency=np.where(delivered,a-o,-1.)
    return {'latency_ms':latency,'dropout_rate':float((~delivered).mean()),'deadline_miss_rate':float(((~delivered)|(latency>d)).mean()),'mean_latency_ms':float(latency[delivered].mean()) if delivered.any() else None}
