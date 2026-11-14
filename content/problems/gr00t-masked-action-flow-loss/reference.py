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

def masked_action_flow_loss(prediction,clean_actions,noise,valid):
    v=_array(prediction,3);a=_array(clean_actions,3);e=_array(noise,3);m=_array(valid,3,"bool");b,h,d=v.shape
    if not 1<=b<=32 or not 1<=h<=64 or not 1<=d<=32 or a.shape!=v.shape or e.shape!=v.shape or m.shape!=v.shape:raise ValueError("flow loss shapes")
    residual=np.where(m,v-(a-e),0.);sq=residual**2;count=int(m.sum());per_count=m.sum(axis=(1,2));per=np.zeros(b);np.divide(sq.sum(axis=(1,2)),per_count,out=per,where=per_count>0)
    return {'loss':float(sq.sum()/count) if count else 0.,'per_example':per,'gradient':2*residual/count if count else np.zeros_like(v)}
