import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def detr_losses(logits, predicted_boxes, target_labels, target_boxes, assignment, eos_weight):
    z=_array(logits,2);p=_array(predicted_boxes,2);labels=_array(target_labels,1,"i");t=_array(target_boxes,2);idx=_array(assignment,1,"i")
    q,c=z.shape[0],z.shape[1]-1;m=len(t)
    if not 1<=q<=256 or not 1<=c<=64 or p.shape!=(q,4) or t.shape[1:]!=(4,) or m>q or labels.shape!=(m,) or idx.shape!=(m,) or np.any(labels<0) or np.any(labels>=c) or np.any(idx<0) or np.any(idx>=q) or len(np.unique(idx))!=m:raise ValueError("Loss shape/assignment")
    if type(eos_weight) not in (int,float) or not 0<eos_weight<=1:raise ValueError("Background weight")
    for b in (p,t):
        if np.any(b[:,:2]<0) or np.any(b[:,:2]>1) or np.any(b[:,2:]<1e-6) or np.any(b[:,2:]>1):raise ValueError("Boxes")
    classes=np.full(q,c,dtype=np.int64);classes[idx]=labels;weights=np.where(classes==c,eos_weight,1.)
    shifted=z-z.max(1,keepdims=True);logden=np.log(np.exp(shifted).sum(1));ce=np.sum(weights*(logden-shifted[np.arange(q),classes]))/weights.sum()
    l1=float(np.sum(np.abs(p[idx]-t))/max(m,1));g=0.
    if m:
        a=np.concatenate((p[idx,:2]-p[idx,2:]/2,p[idx,:2]+p[idx,2:]/2),axis=1);b=np.concatenate((t[:,:2]-t[:,2:]/2,t[:,:2]+t[:,2:]/2),axis=1)
        inter=np.prod(np.maximum(0,np.minimum(a[:,2:],b[:,2:])-np.maximum(a[:,:2],b[:,:2])),axis=1);union=np.prod(a[:,2:]-a[:,:2],1)+np.prod(b[:,2:]-b[:,:2],1)-inter
        enclosing=np.prod(np.maximum(a[:,2:],b[:,2:])-np.minimum(a[:,:2],b[:,:2]),axis=1);giou=inter/union-(enclosing-union)/enclosing;g=float(np.sum(1-giou)/m)
    return dict(classification=float(ce),l1=l1,giou=g,total=float(ce+5*l1+2*g))
