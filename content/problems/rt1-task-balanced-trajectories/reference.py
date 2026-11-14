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

def sample_task_balanced(task_ids, uniforms):
    ids=_array(task_ids,1,"int");u=_array(uniforms,2)
    if not 1<=len(ids)<=10000 or (ids<0).any() or u.shape[1]!=2 or len(u)>10000 or (u<0).any() or (u>=1).any(): raise ValueError("invalid IDs or uniforms")
    group_map={}
    for i,t in enumerate(ids):group_map.setdefault(int(t),[]).append(i)
    groups=[group_map[t] for t in sorted(group_map)]
    return np.array([groups[int(a*len(groups))][int(b*len(groups[int(a*len(groups))]))] for a,b in u],dtype=np.int64)
