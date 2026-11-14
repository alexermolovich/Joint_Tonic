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

def sample_ddpm_actions(initial,predicted_noise,betas,step_noise):
    x=_array(initial,2);eps=_array(predicted_noise,3);b=_array(betas,1);z=_array(step_noise,3)
    if not 1<=len(b)<=64 or not all(1<=v<=64 for v in x.shape) or eps.shape!=(len(b),*x.shape) or z.shape!=eps.shape or (b<.0001).any() or (b>.1).any() or any((np.abs(v)>100).any() for v in [x,eps,z]): raise ValueError("invalid schedule or action tensors")
    al=1-b;ab=np.cumprod(al);states=[x.copy()]
    for k in range(len(b)-1,-1,-1):
        x=(x-b[k]/np.sqrt(1-ab[k])*eps[k])/np.sqrt(al[k])
        if k>0:x=x+np.sqrt(b[k]*(1-ab[k-1])/(1-ab[k]))*z[k]
        states.append(x.copy())
    return np.stack(states)
