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

def encode_observation_window(images, proprio, image_valid, proprio_valid, vision_weight, proprio_weight, bias):
    array(images,5);array(proprio,3);array(image_valid,2,np.bool_);array(proprio_valid,2,np.bool_);array(vision_weight,2);array(proprio_weight,2);array(bias,1)
    b,t,c,h,w=images.shape;d=bias.size
    check(1<=b<=8 and 1<=t<=8 and 1<=c<=3 and 1<=h<=32 and 1<=w<=32 and 1<=d<=32)
    check(proprio.shape[:2]==(b,t) and 1<=proprio.shape[2]<=32 and image_valid.shape==proprio_valid.shape==(b,t) and vision_weight.shape==(c,d) and proprio_weight.shape==(proprio.shape[2],d))
    check(np.all((images>=0)&(images<=1)))
    used=image_valid&proprio_valid
    tokens=np.where(used[...,None],images.mean(axis=(-2,-1))@vision_weight+proprio@proprio_weight+bias,0)
    return dict(tokens=tokens,flat=tokens.reshape(b,t*d).copy(),used=used)
