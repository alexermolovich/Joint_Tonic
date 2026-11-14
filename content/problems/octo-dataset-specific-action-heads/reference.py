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

def route_action_heads(readouts,dataset_ids,weights,biases,dimensions):
    x=_array(readouts,2);ids=_array(dataset_ids,1,"int");w=_array(weights,3);c=_array(biases,2);n=_array(dimensions,1,"int");b,e=x.shape;g,ew,d=w.shape
    if not 1<=b<=128 or not 1<=e<=64 or not 1<=g<=16 or not 1<=d<=32 or ew!=e or ids.shape!=(b,) or c.shape!=(g,d) or n.shape!=(g,) or (n<1).any() or (n>d).any() or (ids<0).any() or (ids>=g).any():raise ValueError("head schema")
    y=np.einsum('be,bed->bd',x,w[ids])+c[ids];mask=np.arange(d)[None,:]<n[ids,None]
    return np.where(mask,y,0.),mask
