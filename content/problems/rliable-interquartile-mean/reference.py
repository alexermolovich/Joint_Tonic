import math

import numpy as np

def _float_array(x, ndim, bound=1e6):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=ndim:
        raise ValueError('Expected floating array with documented dimensions')
    y=x.astype(np.float64)
    if not np.all(np.isfinite(y)) or np.any(np.abs(y)>bound):
        raise ValueError('Invalid floating values')
    return y

def interquartile_score(scores):
    x=_float_array(scores,2)
    if not all(1<=v<=2048 for v in x.shape) or x.size>1000000:
        raise ValueError('Invalid score matrix')
    z=np.sort(x.ravel());k=z.size//4
    return float(np.mean(z[k:z.size-k]))
