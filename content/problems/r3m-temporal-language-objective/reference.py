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

def representation_objective(embeddings,language_logits,valid,weights):
    z=_array(embeddings,3);g=_array(language_logits,2);m=_array(valid,1,"bool");w=_array(weights,1);b,slots,d=z.shape
    if b>512 or slots!=4 or not 1<=d<=256 or g.shape!=(b,3) or m.shape!=(b,) or w.shape!=(4,) or (np.abs(z)>100).any() or (np.abs(g)>1000).any() or ((w<0)|(w>100)).any():raise ValueError("representation objective contract")
    scores=-np.linalg.norm(z[:,0,None,:]-z[:,1:,:],axis=-1)
    def nll(x):
        peak=np.max(x,axis=1);return peak+np.log(np.exp(x-peak[:,None]).sum(axis=1))-x[:,0]
    terms=np.stack([nll(scores),nll(g),np.abs(z[:,0]).sum(axis=1),np.linalg.norm(z[:,0],axis=1)],axis=1);terms[~m]=0;components=terms.sum(axis=0)/max(int(m.sum()),1)
    return dict(per_example=terms,components=components,loss=float(w@components))
