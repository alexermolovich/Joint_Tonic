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

def normalize_observations(raw,mapping,scales,timestamps):
    import re
    if type(raw)!=dict or type(mapping)!=dict or type(scales)!=dict or not 1<=len(raw)<=16 or not 1<=len(mapping)<=16 or set(scales)!=set(mapping):raise ValueError("invalid schema maps")
    name=lambda v:type(v)==str and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,31}',v) is not None
    if not all(name(k) for k in raw) or not all(name(k) and name(v) and v in raw for k,v in mapping.items()):raise ValueError("invalid field names")
    t=_array(timestamps,1)
    if not 1<=len(t)<=4096 or (t<0).any() or (np.diff(t)<=0).any():raise ValueError("invalid timestamps")
    arrays={k:_array(v,2) for k,v in raw.items()}
    if any(v.shape[0]!=len(t) or not 1<=v.shape[1]<=64 for v in arrays.values()):raise ValueError("unaligned raw fields")
    factors={k:_scalar(v,np.nextafter(0,1),1000) for k,v in scales.items()}
    return {'timestamps':t.copy(),'features':{k:arrays[v]*factors[k] for k,v in mapping.items()}}
