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

def estimate_context(history,valid,temporal_kernel,weight,bias):
    x=_array(history,3);m=_array(valid,2,"bool");k=_array(temporal_kernel,3);w=_array(weight,2);b=_array(bias,1);bs,h,f=x.shape;c=k.shape[2]
    if not 1<=bs<=32 or not 1<=h<=32 or not 1<=f<=32 or not 1<=c<=16 or not 1<=len(b)<=16 or m.shape!=(bs,h) or k.shape!=(3,f,c) or w.shape!=(h*c,len(b)) or (np.diff(m.astype(int),axis=1)<0).any() or any((np.abs(v)>100).any() for v in [x,k,w,b]):raise ValueError("adaptation block contract")
    padded=np.pad(np.where(m[...,None],x,0.),((0,0),(1,1),(0,0)));conv=np.zeros((bs,h,c))
    for offset in range(3):conv+=padded[:,offset:offset+h]@k[offset]
    activation=np.where(m[...,None],np.maximum(conv,0),0.);used=m.any(axis=1);z=activation.reshape(bs,h*c)@w+b
    return {'latent':np.where(used[:,None],z,0.),'used':used}
