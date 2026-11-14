import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def match_timestamps(reference, queries, tolerance):
    r,q,t=map(_real,(reference,queries,tolerance))
    if r.ndim!=1 or q.ndim!=1 or t.ndim!=0 or t<0 or np.any(np.diff(r)<=0): raise ValueError("Invalid time contract")
    out=np.full(q.shape,-1,dtype=np.int64)
    if not len(r): return out
    hi=np.searchsorted(r,q); left=np.clip(hi-1,0,len(r)-1); right=np.clip(hi,0,len(r)-1)
    idx=np.where(np.abs(q-r[left])<=np.abs(q-r[right]),left,right)
    valid=np.abs(q-r[idx])<=t
    out[valid]=idx[valid]
    return out
