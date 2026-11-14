# Solution

Use stable sigmoid, phrase-wise maxima, deterministic argmax, then convert selected boxes. Time O(QPT), storage O(QP).

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def decode_grounded_boxes(boxes, token_logits, phrase_map, image_size, threshold):
    b=_array(boxes,2);s=_array(token_logits,2);p=_array(phrase_map,2,"b")
    if b.shape[1:]!=(4,) or len(b)>2048 or s.shape[0]!=len(b) or not 1<=s.shape[1]<=512 or not 1<=len(p)<=128 or p.shape[1]!=s.shape[1] or np.any(~p.any(1)) or np.any(b<0) or np.any(b>1) or np.any(b[:,2:]<=0):raise ValueError("Box/phrase contract")
    if type(image_size) is not tuple or len(image_size)!=2 or any(type(x) is not int or not 1<=x<=100000 for x in image_size) or type(threshold) not in (int,float) or not 0<=threshold<=1:raise ValueError("Image/threshold")
    probability=np.exp(-np.logaddexp(0.,-s))
    scores=np.stack([probability[:,row].max(1) for row in p],axis=1)
    phrase=scores.argmax(1);best=scores[np.arange(len(b)),phrase];idx=np.flatnonzero(best>=threshold)
    corners=np.concatenate((b[idx,:2]-b[idx,2:]/2,b[idx,:2]+b[idx,2:]/2),axis=1)
    h,w=image_size;corners*=np.array([w,h,w,h])
    return dict(query_indices=idx.astype(np.int64),phrase_indices=phrase[idx].astype(np.int64),scores=best[idx],boxes_xyxy=corners)
```
