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

def solver_trajectory_error(estimates,target,steps,latency_ms,max_rmse,deadline_ms):
    x=_array(estimates,3);y=_array(target,2);s=_array(steps,1,"int");t=_array(latency_ms,1);e=_scalar(max_rmse);d=_scalar(deadline_ms);k,h,a=x.shape
    if not 1<=k<=64 or not 1<=h<=256 or not 1<=a<=32 or y.shape!=(h,a) or s.shape!=(k,) or t.shape!=(k,) or (s<1).any() or (s>10000).any() or (t<0).any():raise ValueError("solver contract")
    delta=x-y;rmse=np.sqrt(np.mean(delta**2,axis=(1,2)));maximum=np.max(np.abs(delta),axis=(1,2));ok=(rmse<=e)&(t<=d);idx=np.flatnonzero(ok);selected=min(idx,key=lambda i:(t[i],s[i],i)) if len(idx) else -1
    return {'rmse':rmse,'max_abs_error':maximum,'feasible':ok,'selected_index':int(selected)}
