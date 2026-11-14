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

def sample_video_triplets(lengths,uniforms):
    lengths=_array(lengths,1,"int");u=_array(uniforms,2);v=len(lengths);b=len(u)
    if not 2<=v<=1024 or ((lengths<1)|(lengths>100000)).any() or u.shape!=(b,6) or b>16384 or ((u<0)|(u>=1)).any():raise ValueError("video sampling contract")
    eligible=np.flatnonzero(lengths>=3)
    if not len(eligible):raise ValueError("no three-frame video")
    videos=eligible[np.floor(u[:,0]*len(eligible)).astype(np.int64)];size=lengths[videos]
    i=np.floor(u[:,1]*(size-2)).astype(np.int64);j=i+1+np.floor(u[:,2]*(size-i-2)).astype(np.int64);k=j+1+np.floor(u[:,3]*(size-j-1)).astype(np.int64)
    other=np.floor(u[:,4]*(v-1)).astype(np.int64);other+=other>=videos;negative=np.floor(u[:,5]*lengths[other]).astype(np.int64)
    return dict(video_ids=videos,frames=np.stack([i,j,k],axis=1),negative_video_ids=other,negative_frames=negative)
