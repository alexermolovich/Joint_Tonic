import numpy as np
import math

def array(x, ndim, dtype=np.float64):
    if not isinstance(x,np.ndarray) or x.dtype != np.dtype(dtype) or x.ndim != ndim or x.size>2000000:
        raise ValueError("Invalid array type, dtype, rank or size")
    if dtype != np.bool_ and (not np.isfinite(x).all() or np.any(np.abs(x.astype(float))>1e6)):
        raise ValueError("Nonfinite or out-of-range data")
    return x

def check(ok):
    if not ok: raise ValueError("Contract violation")

def real(x, low, high):
    check(type(x) in (int,float) and math.isfinite(x) and low<=x<=high)
    return x

def integer(x, low, high):
    check(type(x) is int and low<=x<=high)
    return x

def hierarchical_samples(edges, weights, quantiles):
    array(edges,2);array(weights,2);array(quantiles,2)
    b,s=weights.shape
    check(1<=b<=32 and 1<=s<=128 and edges.shape==(b,s+1) and quantiles.shape[0]==b and 1<=quantiles.shape[1]<=128)
    check(np.all((edges>=0)&(edges<=1000)) and np.all(np.diff(edges,axis=1)>=1e-9) and np.all(weights>=0) and np.all((quantiles>=0)&(quantiles<=1)))
    masses=weights+1e-5;pdf=masses/masses.sum(axis=1,keepdims=True)
    cdf=np.concatenate((np.zeros((b,1)),np.cumsum(pdf,axis=1)),axis=1);cdf[:,-1]=1
    out=np.empty_like(quantiles)
    for i in range(b):
        j=np.clip(np.searchsorted(cdf[i],quantiles[i],side='right')-1,0,s-1)
        fraction=(quantiles[i]-cdf[i,j])/(cdf[i,j+1]-cdf[i,j])
        out[i]=edges[i,j]+fraction*(edges[i,j+1]-edges[i,j])
    return out
