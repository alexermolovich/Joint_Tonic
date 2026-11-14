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

def render_color_gradients(density, intervals, colors, background, target):
    array(density,2);array(intervals,2);array(colors,3);array(background,1);array(target,2)
    b,s=density.shape
    check(1<=b<=32 and 1<=s<=128 and intervals.shape==(b,s) and colors.shape==(b,s,3) and background.shape==(3,) and target.shape==(b,3))
    check(np.all((density>=0)&(density<=1000)) and np.all((intervals>=1e-9)&(intervals<=10)))
    for a in (colors,background,target):check(np.all((a>=0)&(a<=1)))
    tau=density*intervals;prefix=np.concatenate((np.zeros((b,1)),np.cumsum(tau,axis=1)),axis=1)
    trans=np.exp(-prefix);alpha=-np.expm1(-tau);weights=trans[:,:-1]*alpha
    contribution=weights[...,None]*colors;terminal=trans[:,-1,None]*background
    rgb=contribution.sum(axis=1)+terminal;g=2*(rgb-target)/(b*3)
    suffix=np.cumsum(contribution[:,::-1],axis=1)[:,::-1]-contribution
    derivative=intervals[...,None]*(trans[:,1:,None]*colors-suffix-terminal[:,None])
    return dict(rgb=rgb,loss=float(np.mean((rgb-target)**2)),density_gradient=np.sum(g[:,None]*derivative,axis=-1),color_gradient=weights[...,None]*g[:,None])
