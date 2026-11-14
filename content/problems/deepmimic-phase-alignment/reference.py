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

def phase_alignment(observed_phase,reference_phase,valid,threshold):
    o=_array(observed_phase,2);r=_array(reference_phase,2);m=_array(valid,2,"bool");tau=_scalar(threshold,0,.5)
    if not 1<=len(o)<=128 or not 1<=o.shape[1]<=256 or r.shape!=o.shape or m.shape!=o.shape or ((o<0)|(o>=1)).any() or ((r<0)|(r>=1)).any():raise ValueError("phase contract")
    error=(o-r+.5)%1-.5;counts=m.sum(axis=1,dtype=np.int64);mean=np.full(len(o),np.nan);np.divide(np.where(m,np.abs(error),0).sum(axis=1),counts,out=mean,where=counts>0)
    return {'error':np.where(m,error,np.nan),'misaligned':m&(np.abs(error)>tau),'mean_absolute':mean,'counts':counts}
