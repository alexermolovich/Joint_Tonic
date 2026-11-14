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

def quantize_training_actions(training,actions,bins):
    x=_array(training,2);a=_array(actions,2);k=_scalar(bins,2,256,True)
    if not 2<=len(x)<=10000 or not 1<=x.shape[1]<=32 or len(a)>10000 or a.shape[1]!=x.shape[1]:raise ValueError("action shapes")
    lo,hi=np.quantile(x,[.01,.99],axis=0,method='linear')
    if (hi<=lo).any():raise ValueError("degenerate training channel")
    z=np.clip(np.floor(k*np.clip((a-lo)/(hi-lo),0,1)),0,k-1).astype(np.int64)
    return {'lower':lo,'upper':hi,'codes':z,'decoded':lo+(z+.5)*(hi-lo)/k}
