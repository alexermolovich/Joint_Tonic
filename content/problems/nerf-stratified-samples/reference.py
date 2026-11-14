import numpy as np


def stratified_samples(near,far,draws):
    for x in (near,far,draws):
        if not isinstance(x,np.ndarray):raise TypeError("Expected NumPy arrays")
        if x.dtype!=np.float64 or not np.isfinite(x).all():raise ValueError("Expected finite float64")
    if near.ndim!=1 or not 1<=near.size<=4096 or far.shape!=near.shape or draws.ndim!=2 or draws.shape[0]!=near.size or not 1<=draws.shape[1]<=1024 or draws.size>1_000_000:
        raise ValueError("Invalid ray shapes")
    if np.any(near<0) or np.any(far>1e6) or np.any(far-near<1e-6) or np.any(draws<0) or np.any(draws>=1):
        raise ValueError("Invalid bounds or draws")
    s=draws.shape[1]
    return near[:,None]+(np.arange(s)[None,:]+draws)*((far-near)/s)[:,None]
