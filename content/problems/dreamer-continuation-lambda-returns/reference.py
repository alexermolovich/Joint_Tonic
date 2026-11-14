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

def imagined_lambda_returns(rewards,next_values,continuation,valid,gamma,lam):
    r=_array(rewards,2);v=_array(next_values,2);c=_array(continuation,2);m=_array(valid,2,"bool");g=_scalar(gamma,0,1);l=_scalar(lam,0,1);b,t=r.shape
    if not 1<=b<=64 or not 1<=t<=1024 or v.shape!=r.shape or c.shape!=r.shape or m.shape!=r.shape or ((c<0)|(c>1)).any() or (np.diff(m.astype(int),axis=1)>0).any():raise ValueError("imagined target contract")
    out=np.zeros_like(r)
    for k in range(t-1,-1,-1):
        future=np.where(m[:,k+1],out[:,k+1],v[:,k]) if k+1<t else v[:,k]
        out[:,k]=np.where(m[:,k],r[:,k]+g*c[:,k]*((1-l)*v[:,k]+l*future),0.)
    return out
