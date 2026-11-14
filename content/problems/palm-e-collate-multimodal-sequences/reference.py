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

def collate_multimodal(sequences,modalities):
    if type(sequences)!=list or type(modalities)!=list or not 1<=len(sequences)<=32 or len(modalities)!=len(sequences):raise ValueError("aligned nonempty lists required")
    xs=[_array(x,2) for x in sequences];ms=[_array(x,1,"int") for x in modalities];e=xs[0].shape[1]
    if not 1<=e<=128 or any(x.shape[1]!=e or len(x)>256 or len(m)!=len(x) or (m<0).any() or (m>2).any() for x,m in zip(xs,ms)):raise ValueError("invalid sequences")
    lengths=np.array([len(x) for x in xs],dtype=np.int64);n=int(lengths.max());b=len(xs)
    if b*n*e>1000000:raise ValueError("padded batch too large")
    y=np.zeros((b,n,e));ids=np.full((b,n),-1,dtype=np.int64);present=np.zeros((b,n),dtype=bool)
    for i,(x,m) in enumerate(zip(xs,ms)):y[i,:len(x)]=x;ids[i,:len(x)]=m;present[i,:len(x)]=True
    return {'tokens':y,'modalities':ids,'present':present,'lengths':lengths}
