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

def normalize_action_spaces(actions,available,mean,std):
    a=_array(actions,3);v=_array(available,2,"bool");mu=_array(mean,2);sd=_array(std,2);b,h,d=a.shape
    if not 1<=b<=32 or not 1<=h<=256 or not 1<=d<=64 or any(x.shape!=(b,d) for x in [v,mu,sd]) or (sd<1e-6).any():raise ValueError("invalid action interface")
    mask=np.broadcast_to(v[:,None,:],a.shape).copy();out=np.where(mask,(a-mu[:,None,:])/sd[:,None,:],0.)
    return out,mask
