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

def sample_dataset_mixture(sizes,weights,uniforms):
    n=_array(sizes,1,"int");w=_array(weights,1);u=_array(uniforms,2)
    if not 1<=len(n)<=128 or (n<1).any() or w.shape!=n.shape or (w<0).any() or w.sum()<=0 or u.shape[1]!=2 or len(u)>10000 or (u<0).any() or (u>=1).any():raise ValueError("invalid mixture")
    positive=np.flatnonzero(w>0);cdf=np.cumsum(w[positive]/w.sum());cdf[-1]=1.;g=positive[np.searchsorted(cdf,u[:,0],side='right')];i=np.floor(u[:,1]*n[g]).astype(np.int64)
    return g,i
