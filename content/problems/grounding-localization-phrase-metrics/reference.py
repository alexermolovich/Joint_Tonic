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

def grounding_pair_metrics(predicted_boxes, target_boxes, predicted_phrases, target_phrases, valid, iou_threshold):
    array(predicted_boxes,2);array(target_boxes,2);array(predicted_phrases,1,np.int64);array(target_phrases,1,np.int64);array(valid,1,np.bool_);real(iou_threshold,0,1)
    n=valid.size;check(n<=4096 and predicted_boxes.shape==target_boxes.shape==(n,4) and predicted_phrases.shape==target_phrases.shape==(n,))
    for a in (predicted_boxes,target_boxes):check(np.all((a>=0)&(a<=1)) and np.all(a[:,2:]>a[:,:2]))
    for a in (predicted_phrases,target_phrases):check(np.all((a>=0)&(a<=100000)))
    ps=predicted_boxes[:,2:]-predicted_boxes[:,:2];ts=target_boxes[:,2:]-target_boxes[:,:2]
    scale=np.maximum(ps,ts)
    intersection=(np.maximum(0,np.minimum(predicted_boxes[:,2:],target_boxes[:,2:])-np.maximum(predicted_boxes[:,:2],target_boxes[:,:2]))/scale).prod(axis=1)
    union=(ps/scale).prod(axis=1)+(ts/scale).prod(axis=1)-intersection
    iou=np.where(valid,intersection/union,0);box=valid&(iou>=iou_threshold);phrase=valid&(predicted_phrases==target_phrases);grounded=box&phrase
    count=int(valid.sum())
    return dict(iou=iou,box_correct=box,phrase_correct=phrase,grounded_correct=grounded,count=count,localization_rate=float(box.sum()/count) if count else 0.,phrase_rate=float(phrase.sum()/count) if count else 0.,grounded_rate=float(grounded.sum()/count) if count else 0.)
