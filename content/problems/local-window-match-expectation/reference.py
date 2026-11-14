import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x,low,high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def refine_matches(queries,windows,coarse_targets,pixel_scale):
    q=_array(queries,2);w=_array(windows,4);centers=_array(coarse_targets,2);scale=_array(pixel_scale,1);b,d=q.shape;s=w.shape[1]
    if b>256 or not 1<=d<=64 or not 1<=s<=9 or s%2!=1 or w.shape!=(b,s,s,d) or w.size>1000000 or centers.shape!=(b,2) or scale.shape!=(2,) or np.any((scale<1e-3)|(scale>64)) or np.any(np.abs(q)>100) or np.any(np.abs(w)>100):raise ValueError("local matching contract")
    logits=np.einsum('bd,bijd->bij',q,w)/np.sqrt(d);flat=logits.reshape(b,s*s);e=np.exp(flat-flat.max(axis=1,keepdims=True));prob=e/e.sum(axis=1,keepdims=True);y,x=np.indices((s,s));grid=np.column_stack([x.ravel()-s//2,y.ravel()-s//2])*scale;offset=prob@grid;delta=grid[None,:,:]-offset[:,None,:];covariance=np.einsum('bk,bki,bkj->bij',prob,delta,delta)
    return dict(probabilities=prob.reshape(b,s,s),offsets=offset,refined=centers+offset,covariance=covariance)
