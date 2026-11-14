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

def denoising_budget(candidate_steps,step_ms,overhead_ms,frequency_hz):
    s=_array(candidate_steps,1,"int");c=_scalar(step_ms,np.nextafter(0,1));o=_scalar(overhead_ms);f=_scalar(frequency_hz,.001,10000)
    if not 1<=len(s)<=128 or (s<1).any() or (s>10000).any():raise ValueError("invalid candidates")
    latency=o+c*s;valid=latency<=1000/f
    return {'latency_ms':latency,'feasible':valid,'selected_steps':int(s[valid].max()) if valid.any() else 0}
