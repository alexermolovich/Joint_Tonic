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

def embodiment_transfer_metrics(train_ids,test_ids,success,num_embodiments):
    t=_array(train_ids,1,"int");e=_array(test_ids,1,"int");y=_array(success,1,"bool");n=_scalar(num_embodiments,1,64,True)
    if len(t)>10000 or e.shape!=t.shape or y.shape!=t.shape or any((v<0).any() or (v>=n).any() for v in [t,e]):raise ValueError("invalid embodiment IDs")
    count=np.zeros((n,n),dtype=np.int64);good=np.zeros((n,n),dtype=np.int64);np.add.at(count,(t,e),1);np.add.at(good,(t,e),y)
    rate=np.full((n,n),np.nan);np.divide(good,count,out=rate,where=count>0);same=t==e
    return {'count':count,'success_rate':rate,'same_embodiment_rate':float(y[same].mean()) if same.any() else None,'transfer_rate':float(y[~same].mean()) if (~same).any() else None}
