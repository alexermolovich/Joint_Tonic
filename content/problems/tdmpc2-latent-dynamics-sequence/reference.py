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

def latent_sequence(initial_state,actions,state_weight,action_weight,bias,group_size):
    z=_array(initial_state,2);a=_array(actions,3);w=_array(state_weight,2);u=_array(action_weight,2);bias=_array(bias,1);b,d=z.shape;h=a.shape[1];width=a.shape[2]
    if type(group_size) is not int:raise ValueError("group type")
    g=_scalar(group_size,1,32,True)
    if not 1<=b<=32 or not 1<=d<=32 or not 1<=width<=32 or h>64 or d%g or a.shape[0]!=b or w.shape!=(d,d) or u.shape!=(width,d) or bias.shape!=(d,) or any((np.abs(x)>10).any() for x in [z,a,w,u,bias]) or (z<0).any() or not np.allclose(z.reshape(b,d//g,g).sum(axis=-1),1,atol=1e-9,rtol=0):raise ValueError("simplex dynamics contract")
    states=np.empty((b,h+1,d));states[:,0]=z
    for t in range(h):
        raw=(states[:,t]@w+a[:,t]@u+bias).reshape(b,d//g,g);exp=np.exp(raw-raw.max(axis=-1,keepdims=True));states[:,t+1]=(exp/exp.sum(axis=-1,keepdims=True)).reshape(b,d)
    return states
