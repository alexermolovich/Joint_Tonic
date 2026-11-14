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

def align_tactile_actions(frame_times,action_times,actions,max_age):
    t=_array(frame_times,1);s=_array(action_times,1);a=_array(actions,2);limit=_scalar(max_age,0,100)
    if len(t)>4096 or len(s)>4096 or a.shape[0]!=len(s) or not 1<=a.shape[1]<=16 or (t<0).any() or (s<0).any() or (np.diff(s)<=0).any() or (np.abs(a)>1).any():raise ValueError("action time contract")
    ids=np.searchsorted(s,t,side='right').astype(np.int64)-1;present=ids>=0;age=np.full(len(t),np.nan);age[present]=t[present]-s[ids[present]];valid=present&(age<=limit);out=np.zeros((len(t),a.shape[1]));out[valid]=a[ids[valid]]
    return {'indices':ids,'age':age,'valid':valid,'aligned':out}
