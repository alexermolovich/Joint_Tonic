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

def imagine_latents(initial_state,actions,state_weight,action_weight,bias,reward_weight,reward_bias,continue_weight,continue_bias):
    x=_array(initial_state,2);a=_array(actions,3);w=_array(state_weight,2);u=_array(action_weight,2);b=_array(bias,1);rw=_array(reward_weight,1);cw=_array(continue_weight,1);rb=_scalar(reward_bias,-10,10);cb=_scalar(continue_bias,-10,10);bs,d=x.shape;h=a.shape[1];width=a.shape[2]
    if not 1<=bs<=32 or not 1<=d<=32 or not 0<=h<=64 or not 1<=width<=32 or a.shape[0]!=bs or w.shape!=(d,d) or u.shape!=(width,d) or any(v.shape!=(d,) for v in [b,rw,cw]) or any((np.abs(v)>10).any() for v in [x,a,w,u,b,rw,cw]):raise ValueError("imagined dynamics contract")
    states=np.empty((bs,h+1,d));states[:,0]=x;rewards=np.empty((bs,h));continuation=np.empty((bs,h))
    for k in range(h):
        states[:,k+1]=np.tanh(states[:,k]@w+a[:,k]@u+b);rewards[:,k]=states[:,k+1]@rw+rb;logits=states[:,k+1]@cw+cb;e=np.exp(-np.abs(logits));continuation[:,k]=np.where(logits>=0,1/(1+e),e/(1+e))
    return {'states':states,'rewards':rewards,'continuation':continuation}
