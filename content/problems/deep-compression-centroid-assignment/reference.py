import numpy as np

def _array(x, rank):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=rank or x.size>1000000 or not np.isfinite(x).all() or (x.size and np.max(np.abs(x))>1e6):
        raise ValueError('invalid numeric array')
    return x.astype(np.float64)

def _pair(x,w,limit=2048):
    x,w=_array(x,2),_array(w,2)
    if not all(1<=n<=limit for n in (*x.shape,*w.shape)) or x.shape[1]!=w.shape[0]:raise ValueError('shape')
    return x,w

def _real(v,lo=0,hi=1e6):
    if type(v) not in (int,float) or not lo<=v<=hi or not np.isfinite(v):raise ValueError('scalar')
    return float(v)

def assign_weight_centroids(weights, active, centroids):
    w,c=_array(weights,1),_array(centroids,1)
    if w.size>100000 or not 1<=c.size<=256 or w.size*c.size>10**7 or not isinstance(active,np.ndarray) or active.dtype!=np.bool_ or active.shape!=w.shape:raise ValueError('shape/mask')
    chosen=np.argmin(np.abs(w[:,None]-c[None,:]),axis=1)
    indices=np.where(active,chosen,-1).astype(np.int64)
    return indices,np.where(active,c[chosen],0.)
