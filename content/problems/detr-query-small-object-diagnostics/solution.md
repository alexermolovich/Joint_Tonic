# Solution

Normalize query features and compare pairwise cosine; compute prediction-target IoU and small-target coverage. O(Q²D+QM) time.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def diagnose_queries(features, predicted_boxes, target_boxes, cosine_limit, iou_limit, small_area):
    f=_array(features,2);p=_array(predicted_boxes,2);t=_array(target_boxes,2)
    if len(f)>256 or not 1<=f.shape[1]<=128 or p.shape!=(len(f),4) or t.shape[1:]!=(4,) or len(t)>256:raise ValueError("Diagnostic shapes")
    for b in (p,t):
        if np.any(b<0) or np.any(b>1) or np.any(b[:,2:]<=b[:,:2]):raise ValueError("Boxes")
    for x,lo,hi,strict in ((cosine_limit,-1,1,False),(iou_limit,0,1,True),(small_area,0,1,False)):
        if type(x) not in (int,float) or not lo<=x<=hi or (strict and x==lo):raise ValueError("Threshold")
    norms=np.linalg.norm(f,axis=1)
    if np.any(norms<1e-8):raise ValueError("Feature norm")
    u=f/norms[:,None];similar=np.clip(u@u.T,-1,1)>=cosine_limit;pairs=np.argwhere(np.triu(similar,1)).astype(np.int64)
    area_t=np.prod(t[:,2:]-t[:,:2],axis=1);covered=np.zeros(len(t),bool)
    if len(p):
        intersection=np.prod(np.maximum(0,np.minimum(p[:,None,2:],t[None,:,2:])-np.maximum(p[:,None,:2],t[None,:,:2])),axis=2)
        area_p=np.prod(p[:,2:]-p[:,:2],axis=1);iou=intersection/(area_p[:,None]+area_t[None,:]-intersection);covered=(iou>=iou_limit).any(0)
    return dict(similar_pairs=pairs,missed_small_indices=np.flatnonzero((area_t<=small_area)&~covered).astype(np.int64))
```
