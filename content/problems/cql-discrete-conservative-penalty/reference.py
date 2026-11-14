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

def conservative_penalty(q_values,logged_actions,valid,alpha):
    q=_array(q_values,2);a=_array(logged_actions,2,"int");m=_array(valid,1,"bool");alpha=_scalar(alpha,0,100)
    b,n=q.shape
    if not 1<=b<=128 or not 1<=n<=256 or a.shape[0]!=b or not 1<=a.shape[1]<=128 or m.shape!=(b,) or (np.abs(q)>1e4).any() or (a<0).any() or (a>=n).any():raise ValueError("conservative penalty contract")
    peak=q.max(axis=1);exp=np.exp(q-peak[:,None]);prob=exp/exp.sum(axis=1,keepdims=True)
    raw=peak+np.log(exp.sum(axis=1))-np.take_along_axis(q,a,axis=1).mean(axis=1)
    freq=np.zeros_like(q)
    for i in range(b):np.add.at(freq[i],a[i],1/a.shape[1])
    count=int(m.sum());grad=np.where(m[:,None],alpha*(prob-freq)/max(count,1),0.)
    return {'loss':float(alpha*raw[m].mean()) if count else 0.,'per_state':np.where(m,raw,0.),'gradient':grad}
