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

def soft_state_value(q_values,log_probabilities,valid,alpha):
    q=_array(q_values,2);p=_array(log_probabilities,2);m=_array(valid,2,"bool");a=_scalar(alpha,0,100)
    if not 1<=len(q)<=128 or not 1<=q.shape[1]<=256 or p.shape!=q.shape or m.shape!=q.shape or (np.abs(p)>100).any():raise ValueError("soft value contract")
    count=m.sum(axis=1,dtype=np.int64);out=np.zeros(len(q));np.divide(np.where(m,q-a*p,0.).sum(axis=1),count,out=out,where=count>0)
    return {'values':out,'counts':count}
