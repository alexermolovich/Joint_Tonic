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

def offline_split_report(episode_ids,split_ids,source_ids):
    e=_array(episode_ids,1,"int");s=_array(split_ids,1,"int");src=_array(source_ids,1,"int")
    if len(e)>100000 or s.shape!=e.shape or src.shape!=e.shape or (e<0).any() or (src<0).any() or (s<0).any() or (s>2).any():raise ValueError("split contract")
    groups={}
    for source,episode,split in zip(src,e,s):groups.setdefault((int(source),int(episode)),set()).add(int(split))
    leaks=np.array(sorted(k for k,v in groups.items() if len(v)>1),dtype=np.int64).reshape(-1,2);counts=np.bincount(s,minlength=3).astype(np.int64);missing=np.flatnonzero(counts==0).astype(np.int64)
    return {'counts':counts,'leakage_pairs':leaks,'missing_splits':missing,'valid':bool(len(leaks)==0 and len(missing)==0)}
