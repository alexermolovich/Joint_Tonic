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

def symlog_twohot(rewards,bins):
    x=_array(rewards,1);b=_array(bins,1);n=len(x);k=len(b)
    if n>4096 or not 2<=k<=255 or n*k>1000000 or (np.abs(b)>20).any() or (np.diff(b)<=0).any():raise ValueError("twohot target contract")
    y=np.sign(x)*np.log1p(np.abs(x));clipped=np.clip(y,b[0],b[-1]);hi=np.clip(np.searchsorted(b,clipped,side='right'),1,k-1);lo=hi-1;upper=(clipped-b[lo])/(b[hi]-b[lo]);out=np.zeros((n,k));rows=np.arange(n);out[rows,lo]=1-upper;out[rows,hi]=upper;mean=out@b
    return {'symlog':y,'targets':out,'reconstructed':np.sign(mean)*np.expm1(np.abs(mean))}
