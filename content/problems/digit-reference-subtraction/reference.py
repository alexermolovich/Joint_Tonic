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

def tactile_difference(images,reference,roi,threshold):
    x=_array(images,4);r=_array(reference,3);m=_array(roi,2,"bool");tau=_scalar(threshold,0,1);b,h,w,c=x.shape
    if not 1<=b<=32 or not 1<=h<=64 or not 1<=w<=64 or not 1<=c<=3 or r.shape!=(h,w,c) or m.shape!=(h,w) or ((x<0)|(x>1)).any() or ((r<0)|(r>1)).any():raise ValueError("tactile image contract")
    difference=np.where(m[None,:,:,None],x-r,0.);change=np.abs(difference).mean(axis=-1)
    return {'difference':difference,'change':change,'mask':m[None,:,:]&(change>tau)}
