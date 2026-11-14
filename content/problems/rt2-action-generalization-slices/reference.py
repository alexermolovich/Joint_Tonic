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

def action_slice_metrics(valid,success,slice_ids,num_slices):
    v=_array(valid,1,"bool");y=_array(success,1,"bool");ids=_array(slice_ids,1,"int");s=_scalar(num_slices,1,128,True)
    if len(v)>10000 or y.shape!=v.shape or ids.shape!=v.shape or (ids<0).any() or (ids>=s).any():raise ValueError("invalid attempts")
    count=np.bincount(ids,minlength=s).astype(np.int64);bad=np.bincount(ids,weights=~v,minlength=s);good=np.bincount(ids,weights=v&y,minlength=s)
    inv=np.full(s,np.nan);rate=np.full(s,np.nan);np.divide(bad,count,out=inv,where=count>0);np.divide(good,count,out=rate,where=count>0)
    return {'count':count,'invalid_rate':inv,'success_rate':rate}
