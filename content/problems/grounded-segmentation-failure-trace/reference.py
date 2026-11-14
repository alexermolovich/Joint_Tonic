import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def grounded_segmentation(phrase_scores, masks, mask_quality, min_phrase, min_quality):
    s=_array(phrase_scores,2);m=_array(masks,3,"b");q=_array(mask_quality,1)
    if len(s)>128 or not 1<=s.shape[1]<=128 or m.shape[0]!=len(s) or not (1<=m.shape[1]<=128 and 1<=m.shape[2]<=128) or q.shape!=(len(s),) or np.any(s<0) or np.any(s>1) or np.any(q<0) or np.any(q>1):raise ValueError("Pipeline shapes/ranges")
    if any(type(x) not in (int,float) or not 0<=x<=1 for x in (min_phrase,min_quality)):raise ValueError("Threshold")
    labels=s.argmax(1);best=s[np.arange(len(s)),labels];area=m.sum((1,2));status=[];keep=[];centers=[]
    for i in range(len(s)):
        reason='low_grounding' if best[i]<min_phrase else 'low_mask_quality' if q[i]<min_quality else 'empty_mask' if area[i]==0 else 'accepted'
        status.append(reason)
        if reason=='accepted':
            y,x=np.nonzero(m[i]);keep.append(i);centers.append([float(x.mean()+.5),float(y.mean()+.5)])
    idx=np.array(keep,dtype=np.int64)
    return dict(status=status,query_indices=idx,phrase_indices=labels[idx].astype(np.int64),areas=area[idx].astype(np.int64),centroids_xy=np.array(centers,dtype=np.float64).reshape(-1,2))
