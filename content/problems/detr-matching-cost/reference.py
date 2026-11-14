import numpy as np


def detr_matching_cost(class_probs, pred_boxes, target_labels, target_boxes, weights=(1.0,5.0,2.0)):
    for a in (class_probs,pred_boxes,target_labels,target_boxes):
        if not isinstance(a,np.ndarray):
            raise TypeError("Expected NumPy arrays")
    if class_probs.dtype!=np.float64 or class_probs.ndim!=2 or not 1<=class_probs.shape[0]<=300 or not 2<=class_probs.shape[1]<=1001:
        raise ValueError("Invalid probability shape or dtype")
    q,k=class_probs.shape[0],class_probs.shape[1]-1
    if not np.isfinite(class_probs).all() or np.any(class_probs<0) or np.any(class_probs>1) or not np.allclose(class_probs.sum(1),1,atol=1e-6,rtol=0):
        raise ValueError("Invalid class probabilities")
    if target_labels.dtype!=np.int64 or target_labels.ndim!=1 or target_labels.size>q or np.any(target_labels<0) or np.any(target_labels>=k):
        raise ValueError("Invalid target labels")
    for boxes, n in ((pred_boxes,q),(target_boxes,target_labels.size)):
        if boxes.dtype!=np.float64 or boxes.shape!=(n,4) or not np.isfinite(boxes).all():
            raise ValueError("Invalid boxes")
        if np.any(boxes[:,:2]<0) or np.any(boxes[:,:2]>1) or np.any(boxes[:,2:]<1e-6) or np.any(boxes[:,2:]>1):
            raise ValueError("Boxes outside supported range")
    if not isinstance(weights,tuple) or len(weights)!=3 or any(type(w) not in (int,float) or not 0<=w<=100 or not np.isfinite(w) for w in weights) or not any(weights):
        raise ValueError("Invalid cost weights")
    p0,p1=pred_boxes[:,:2]-pred_boxes[:,2:]/2,pred_boxes[:,:2]+pred_boxes[:,2:]/2
    t0,t1=target_boxes[:,:2]-target_boxes[:,2:]/2,target_boxes[:,:2]+target_boxes[:,2:]/2
    intersection=np.maximum(0,np.minimum(p1[:,None],t1)-np.maximum(p0[:,None],t0)).prod(-1)
    union=(p1-p0).prod(-1)[:,None]+(t1-t0).prod(-1)-intersection
    enclosure=(np.maximum(p1[:,None],t1)-np.minimum(p0[:,None],t0)).prod(-1)
    giou=intersection/union-(enclosure-union)/enclosure
    l1=np.abs(pred_boxes[:,None,:]-target_boxes[None,:,:]).sum(-1)
    return -weights[0]*class_probs[:,target_labels]+weights[1]*l1-weights[2]*giou
