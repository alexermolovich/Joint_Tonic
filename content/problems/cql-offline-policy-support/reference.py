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

def offline_action_support(logged_states,logged_actions,query_states,query_actions,max_distance):
    s=_array(logged_states,1,"int");a=_array(logged_actions,2);q=_array(query_states,1,"int");u=_array(query_actions,2);limit=_scalar(max_distance,0,10)
    if len(s)>1024 or len(q)>256 or a.shape[0]!=len(s) or u.shape[0]!=len(q) or not 1<=a.shape[1]<=16 or u.shape[1]!=a.shape[1] or (s<0).any() or (q<0).any() or (np.abs(a)>1).any() or (np.abs(u)>1).any():raise ValueError("support contract")
    ids=np.full(len(q),-1,np.int64);dist=np.full(len(q),np.nan)
    for j,state in enumerate(q):
        rows=np.flatnonzero(s==state)
        if len(rows):
            ds=np.linalg.norm(a[rows]-u[j],axis=1);k=int(np.argmin(ds));ids[j]=rows[k];dist[j]=ds[k]
    return {'nearest_index':ids,'distance':dist,'unsupported':(ids<0)|(dist>limit)}
