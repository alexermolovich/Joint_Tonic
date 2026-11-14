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
    check(type(x) in (int,float) and low<=x<=high and math.isfinite(x))
    return x

def integer(x, low, high):
    check(type(x) is int and low<=x<=high)
    return x

def class_token_logits(tokens, gamma, beta, weight, bias, epsilon):
    array(tokens,3);array(gamma,1);array(beta,1);array(weight,2);array(bias,1);real(epsilon,1e-8,1)
    b,l,d=tokens.shape;c=bias.size
    check(1<=b<=32 and 1<=l<=257 and 1<=d<=64 and 1<=c<=64 and gamma.shape==beta.shape==(d,) and weight.shape==(d,c))
    cls=tokens[:,0];centered=cls-cls.mean(axis=-1,keepdims=True)
    normalized=centered/np.sqrt((centered**2).mean(axis=-1,keepdims=True)+epsilon)
    return (normalized*gamma+beta)@weight+bias
