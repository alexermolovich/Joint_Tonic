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

def compare_quantized_candidates(activations, weights, candidates):
    x,w=_pair(activations,weights,256);c=_array(candidates,3)
    if c.shape[1:]!=w.shape or not 1<=c.shape[0]<=32 or c.shape[0]*x.shape[0]*x.shape[1]*w.shape[1]>10**7:raise ValueError('shape/work')
    delta=c-w[None,:,:];weight=np.mean(delta*delta,axis=(1,2));errors=x@delta;output=np.mean(errors*errors,axis=(1,2))
    return weight,output,int(np.argmin(output))
