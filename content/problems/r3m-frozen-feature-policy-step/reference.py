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

def frozen_policy_step(features,robot_state,actions,train,evaluate,weight,bias,learning_rate):
    z=_array(features,2);state=_array(robot_state,2);a=_array(actions,2);t=_array(train,1,"bool");e=_array(evaluate,1,"bool");w=_array(weight,2);b=_array(bias,1);lr=_scalar(learning_rate,0,1);n,d=z.shape;p=state.shape[1];channels=a.shape[1]
    if not 1<=n<=4096 or not 1<=d<=64 or not 0<=p<=32 or not 1<=channels<=16 or state.shape!=(n,p) or a.shape!=(n,channels) or t.shape!=(n,) or e.shape!=(n,) or w.shape!=(d+p,channels) or b.shape!=(channels,) or (t&e).any() or not t.any() or any((np.abs(x)>10).any() for x in [z,state,w,b]) or (np.abs(a)>1).any():raise ValueError("frozen policy contract")
    x=np.concatenate([z,state],axis=1);residual=x[t]@w+b-a[t];before=float(np.mean(residual**2));scale=2/residual.size;gw=scale*x[t].T@residual;gb=scale*residual.sum(axis=0);updated=w-lr*gw;offset=b-lr*gb;prediction=x@updated+offset
    return dict(weight=updated,bias=offset,predictions=prediction,train_loss_before=before,train_loss_after=float(np.mean((prediction[t]-a[t])**2)),evaluation_loss=float(np.mean((prediction[e]-a[e])**2)) if e.any() else float('nan'))
