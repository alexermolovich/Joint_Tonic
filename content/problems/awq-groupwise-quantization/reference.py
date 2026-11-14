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

def groupwise_quantize_weights(weights, group_size, bits):
    w=_array(weights,2)
    if not all(1<=n<=1024 for n in w.shape) or type(group_size) is not int or not 1<=group_size<=w.shape[1] or w.shape[1]%group_size or type(bits) is not int or not 2<=bits<=8:raise ValueError('group/bits')
    g=w.reshape(w.shape[0],w.shape[1]//group_size,group_size);qmax=2**bits-1
    lo=np.minimum(g.min(axis=2),0.);hi=np.maximum(g.max(axis=2),0.)
    scales=np.maximum((hi-lo)/qmax,np.finfo(np.float64).tiny);scales=np.where(hi==lo,1.,scales)
    zeros=np.clip(np.rint(-lo/scales),0,qmax).astype(np.int64)
    q=np.clip(np.rint(g/scales[:,:,None])+zeros[:,:,None],0,qmax).astype(np.uint8)
    restored=(q.astype(np.float64)-zeros[:,:,None])*scales[:,:,None]
    return scales,zeros,q.reshape(w.shape),restored.reshape(w.shape)
