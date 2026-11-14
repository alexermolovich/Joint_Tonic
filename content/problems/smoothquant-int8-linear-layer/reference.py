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

def quantize_int8_layer(activations, weights):
    x,w=_pair(activations,weights,1024)
    if x.shape[0]*x.shape[1]*w.shape[1]>10**7:raise ValueError('work budget')
    sx=np.max(np.abs(x),axis=1,keepdims=True)/127
    sw=np.max(np.abs(w),axis=0,keepdims=True)/127
    sx=np.where(sx==0,1.,sx);sw=np.where(sw==0,1.,sw)
    qx=np.clip(np.rint(x/sx),-127,127).astype(np.int8)
    qw=np.clip(np.rint(w/sw),-127,127).astype(np.int8)
    y=(qx.astype(np.int64)@qw.astype(np.int64))*sx*sw
    return qx,qw,sx,sw,y
