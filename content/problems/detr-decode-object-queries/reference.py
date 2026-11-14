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

def decode_queries(logits, boxes, padding, threshold):
    array(logits,3);array(boxes,3);array(padding,2,np.bool_);real(threshold,0,1)
    b,q,k=logits.shape
    check(1<=b<=16 and 1<=q<=128 and 2<=k<=65 and boxes.shape==(b,q,4) and padding.shape==(b,q))
    check(np.all((boxes>=0)&(boxes<=1)))
    ex=np.exp(logits-logits.max(axis=-1,keepdims=True)); probs=ex/ex.sum(axis=-1,keepdims=True)
    labels=probs[...,:-1].argmax(axis=-1);scores=np.take_along_axis(probs,labels[...,None],axis=-1)[...,0]
    valid=(~padding)&(scores>=threshold)
    corners=np.concatenate((boxes[...,:2]-boxes[...,2:]/2,boxes[...,:2]+boxes[...,2:]/2),axis=-1)
    return dict(boxes=np.where(valid[...,None],np.clip(corners,0,1),0),scores=np.where(valid,scores,0),labels=np.where(valid,labels,-1).astype(np.int64),valid=valid)
