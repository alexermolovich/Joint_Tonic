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


def _sigmoid(z):
    e=np.exp(-np.abs(z))
    return np.where(z>=0,1/(1+e),e/(1+e))

def _field(features, intervals, background, weight, bias):
    raw=features@weight+bias
    density=np.maximum(raw[...,0],0)+np.log1p(np.exp(-np.abs(raw[...,0])))
    colors=_sigmoid(raw[...,1:]);tau=density*intervals
    trans=np.exp(-np.concatenate((np.zeros((features.shape[0],1)),np.cumsum(tau,axis=1)),axis=1))
    weights=trans[:,:-1]*(-np.expm1(-tau));contribution=weights[...,None]*colors
    terminal=trans[:,-1,None]*background
    rgb=contribution.sum(axis=1)+terminal
    return rgb,(raw,colors,trans,weights,contribution,terminal)

def train_tiny_field(train_features, train_intervals, train_targets, eval_features, eval_intervals, eval_targets, background, initial_weight, initial_bias, steps, learning_rate):
    for a,n in ((train_features,3),(train_intervals,2),(train_targets,2),(eval_features,3),(eval_intervals,2),(eval_targets,2),(background,1),(initial_weight,2),(initial_bias,1)):array(a,n)
    b,s,f=train_features.shape;r=eval_features.shape[0]
    check(1<=b<=16 and 1<=r<=16 and 1<=s<=32 and 1<=f<=16 and eval_features.shape==(r,s,f))
    check(train_intervals.shape==(b,s) and eval_intervals.shape==(r,s) and train_targets.shape==(b,3) and eval_targets.shape==(r,3) and background.shape==(3,) and initial_weight.shape==(f,4) and initial_bias.shape==(4,))
    for a in (train_features,eval_features,initial_weight,initial_bias):check(np.all(np.abs(a)<=2))
    for a in (train_intervals,eval_intervals):check(np.all((a>=.01)&(a<=2)))
    for a in (train_targets,eval_targets,background):check(np.all((a>=0)&(a<=1)))
    integer(steps,0,64);real(learning_rate,1e-6,.1)
    weight=initial_weight.copy();bias=initial_bias.copy();losses=np.empty(steps+1);norms=np.empty(steps)
    for step in range(steps+1):
        rgb,cache=_field(train_features,train_intervals,background,weight,bias)
        losses[step]=np.mean((rgb-train_targets)**2)
        if step==steps:break
        raw,colors,trans,weights,contribution,terminal=cache
        g=2*(rgb-train_targets)/(3*b)
        suffix=np.cumsum(contribution[:,::-1],axis=1)[:,::-1]-contribution
        density_gradient=np.sum(g[:,None]*train_intervals[...,None]*(trans[:,1:,None]*colors-suffix-terminal[:,None]),axis=-1)
        raw_density=density_gradient*_sigmoid(raw[...,0])
        raw_colors=weights[...,None]*g[:,None]*colors*(1-colors)
        raw_gradient=np.concatenate((raw_density[...,None],raw_colors),axis=-1)
        gw=np.einsum('bsf,bso->fo',train_features,raw_gradient);gb=raw_gradient.sum(axis=(0,1))
        norm=float(np.linalg.norm(np.concatenate((gw.ravel(),gb))));norms[step]=norm
        scale=max(1.,norm)
        weight-=learning_rate*gw/scale;bias-=learning_rate*gb/scale
    rgb,_=_field(eval_features,eval_intervals,background,weight,bias)
    return dict(weight=weight,bias=bias,train_loss=losses,gradient_norm=norms,eval_rgb=rgb,eval_mse=float(np.mean((rgb-eval_targets)**2)))
