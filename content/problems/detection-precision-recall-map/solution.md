# Solution

Sort predictions per class, perform image-local overlap matching and integrate precision envelopes. O(NM+N log N+C) time, bounded synthetic arrays.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def detection_map(pred_boxes, scores, pred_labels, pred_images, target_boxes, target_labels, target_images, num_classes, iou_threshold):
    p=_array(pred_boxes,2);s=_array(scores,1);pl=_array(pred_labels,1,"i");pi=_array(pred_images,1,"i");t=_array(target_boxes,2);tl=_array(target_labels,1,"i");ti=_array(target_images,1,"i")
    if type(num_classes) is not int or not 1<=num_classes<=64 or type(iou_threshold) not in (int,float) or not 0<iou_threshold<=1:raise ValueError("Metric configuration")
    for b,l,im in ((p,pl,pi),(t,tl,ti)):
        if b.shape[1:]!=(4,) or len(b)>512 or l.shape!=(len(b),) or im.shape!=l.shape or np.any(b<0) or np.any(b>1) or np.any(b[:,2:]<=b[:,:2]) or np.any(l<0) or np.any(l>=num_classes) or np.any(im<0) or np.any(im>1000000):raise ValueError("Boxes/labels/images")
    if s.shape!=(len(p),) or np.any(s<0) or np.any(s>1):raise ValueError("Scores")
    ap=np.full(num_classes,np.nan);precisions=[];recalls=[]
    for cls in range(num_classes):
        pred=np.flatnonzero(pl==cls);pred=pred[np.lexsort((pred,-s[pred]))];target=np.flatnonzero(tl==cls);matched=set();hits=[]
        for i in pred:
            candidates=target[ti[target]==pi[i]];hit=False
            if len(candidates):
                boxes=t[candidates];intersection=np.prod(np.maximum(0,np.minimum(p[i,2:],boxes[:,2:])-np.maximum(p[i,:2],boxes[:,:2])),axis=1)
                union=np.prod(p[i,2:]-p[i,:2])+np.prod(boxes[:,2:]-boxes[:,:2],axis=1)-intersection;overlap=intersection/union;j=int(np.argmax(overlap));best=int(candidates[j])
                if overlap[j]>=iou_threshold and best not in matched:matched.add(best);hit=True
            hits.append(hit)
        cumulative=np.cumsum(hits,dtype=np.float64);precision=cumulative/np.arange(1,len(pred)+1);recall=cumulative/len(target) if len(target) else np.zeros(len(pred))
        precisions.append(precision);recalls.append(recall)
        if len(target):
            rr=np.r_[0.,recall,1.];pp=np.r_[0.,precision,0.];envelope=np.maximum.accumulate(pp[::-1])[::-1];ap[cls]=np.sum(np.diff(rr)*envelope[1:])
    observed=np.isfinite(ap)
    return dict(ap=ap,mean_ap=float(ap[observed].mean()) if observed.any() else 0.,precision=precisions,recall=recalls)
```
