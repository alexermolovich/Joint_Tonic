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

def augmented_targets(rewards,next_values,terminated,view_valid,gamma):
    r=_array(rewards,1);v=_array(next_values,2);d=_array(terminated,1,"bool");m=_array(view_valid,2,"bool");g=_scalar(gamma,0,1)
    if not 1<=len(r)<=128 or v.shape[0]!=len(r) or not 1<=v.shape[1]<=64 or d.shape!=r.shape or m.shape!=v.shape:raise ValueError("view target contract")
    count=m.sum(axis=1,dtype=np.int64)
    if ((count==0)&~d).any():raise ValueError("nonterminal needs a view")
    mean=np.full(len(r),np.nan);np.divide(np.where(m,v,0.).sum(axis=1),count,out=mean,where=count>0)
    return {'targets':np.where(d,r,r+g*mean),'mean_next':mean,'counts':count}
