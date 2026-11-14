import numpy as np


def alpha_compositing_weights(density,deltas):
    for a in (density,deltas):
        if not isinstance(a,np.ndarray):
            raise TypeError("Expected NumPy arrays")
        if a.dtype!=np.float64 or a.ndim!=2 or min(a.shape)<1 or a.size>1_000_000 or not np.isfinite(a).all() or np.any(a<0) or np.any(a>1e6):
            raise ValueError("Invalid ray intervals")
    if density.shape!=deltas.shape:
        raise ValueError("Ray shapes differ")
    q=density*deltas
    prefix=np.concatenate((np.zeros((q.shape[0],1)),np.cumsum(q[:,:-1],axis=1)),axis=1)
    weights=np.exp(-prefix)*(-np.expm1(-q))
    return weights,np.exp(-q.sum(axis=1))
