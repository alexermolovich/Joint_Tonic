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

def randomization_robustness(success,valid,baseline_index,min_pairs):
    s=_array(success,2,"bool");m=_array(valid,2,"bool")
    if not 1<=len(s)<=128 or s.shape[1]>4096 or m.shape!=s.shape or type(baseline_index) is not int or type(min_pairs) is not int:raise ValueError("comparison contract")
    base=_scalar(baseline_index,0,len(s)-1,True);minimum=_scalar(min_pairs,1,4096,True);n=m.sum(axis=1,dtype=np.int64);rate=np.divide((s&m).sum(axis=1),n,out=np.full(len(s),np.nan),where=n>0);paired=m&m[base];count=paired.sum(axis=1,dtype=np.int64);diff=s.astype(np.int64)-s[base].astype(np.int64);delta=np.divide(np.where(paired,diff,0).sum(axis=1),count,out=np.full(len(s),np.nan),where=count>0);comparable=count>=minimum;ids=np.flatnonzero(comparable);worst=int(ids[np.argmin(delta[ids])]) if len(ids) else -1
    return {'counts':n,'success_rate':rate,'paired_counts':count,'paired_delta':delta,'comparable':comparable,'worst_index':worst}
