import math

import numpy as np

def _float_array(x, ndim, bound=1e6):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:
        raise ValueError('Expected floating array with documented dimensions')
    y=x.astype(np.float64)
    if not np.all(np.isfinite(y)) or np.any(np.abs(y)>bound):
        raise ValueError('Invalid floating values')
    return y

def _integer_array(x, ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:
        raise ValueError('Expected int64 array')
    return x

def stratified_profile(scores, thresholds, resample_indices):
    x=_float_array(scores,2);t=_float_array(thresholds,1);idx=_integer_array(resample_indices,3)
    if not all(1<=v<=256 for v in x.shape) or len(t)>128 or idx.shape[1:]!=x.shape or idx.shape[0]>512:
        raise ValueError('Invalid profile shapes')
    if idx.size>1000000 or idx.size*max(len(t),1)>20000000 or np.any(idx<0) or np.any(idx>=x.shape[1]):
        raise ValueError('Invalid resampling indices or work budget')
    profile=np.array([np.mean(x>q) for q in t],dtype=np.float64)
    replicates=np.empty((len(idx),len(t)),dtype=np.float64)
    rows=np.arange(x.shape[0])[:,None]
    for b in range(len(idx)):
        sampled=x[rows,idx[b]]
        replicates[b]=[np.mean(sampled>q) for q in t]
    return dict(profile=profile,replicates=replicates)
