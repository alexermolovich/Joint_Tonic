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

def adaptation_step(features,base_weight,down,up,targets,learning_rate):
    x,w,a,c,y=[_array(v,2) for v in [features,base_weight,down,up,targets]];lr=_scalar(learning_rate,0,1);b,e=x.shape
    if not 1<=b<=128 or not 1<=e<=64 or w.shape[0]!=e or not 1<=w.shape[1]<=32 or a.shape[0]!=e or not 1<=a.shape[1]<=16 or c.shape!=(a.shape[1],w.shape[1]) or y.shape!=(b,w.shape[1]) or any((np.abs(v)>100).any() for v in [x,w,a,c,y]):raise ValueError("adapter schema")
    h=x@a;z=x@w+h@c;delta=z-y;grad=2*delta/delta.size
    return {'prediction':z,'loss':float(np.mean(delta*delta)),'down':a-lr*(x.T@grad@c.T),'up':c-lr*(h.T@grad)}
