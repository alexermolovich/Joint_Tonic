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

def random_shift(images,padding,seed):
    x=_array(images,5)
    if type(padding) is not int or type(seed) is not int:raise ValueError("built-in integer required")
    p=_scalar(padding,0,8,True);seed=_scalar(seed,0,2**32-1,True);b,t,h,w,c=x.shape
    if not 1<=b<=16 or not 1<=t<=4 or not 1<=h<=64 or not 1<=w<=64 or not 1<=c<=3 or (x<0).any() or (x>1).any():raise ValueError("image contract")
    offsets=np.random.Generator(np.random.PCG64(seed)).integers(0,2*p+1,size=(b,2),dtype=np.int64)
    padded=np.pad(x,((0,0),(0,0),(p,p),(p,p),(0,0)),mode='edge');out=np.empty_like(x)
    for i,(row,col) in enumerate(offsets):out[i]=padded[i,:,row:row+h,col:col+w,:]
    return {'images':out,'offsets':offsets}
