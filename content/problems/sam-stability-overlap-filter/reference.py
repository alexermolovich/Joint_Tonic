import numpy as np


def filter_stable_masks(logits, quality, threshold, offset, stability_threshold, overlap_threshold):
    if not isinstance(logits,np.ndarray) or not isinstance(quality,np.ndarray):
        raise TypeError("logits and quality must be arrays")
    if logits.dtype!=np.float64 or quality.dtype!=np.float64 or logits.ndim!=3 or quality.ndim!=1:
        raise ValueError("float64 mask logits and ranking scores required")
    count,height,width=logits.shape
    if not 0<=count<=128 or not 1<=height<=512 or not 1<=width<=512 or logits.size>1000000 or quality.shape!=(count,):
        raise ValueError("mask dimensions")
    for array in (logits,quality):
        if not np.isfinite(array).all() or (np.abs(array)>1e6).any():
            raise ValueError("finite bounded arrays required")
    bounds=((threshold,-1000,1000),(offset,0,1000),(stability_threshold,0,1),(overlap_threshold,0,1))
    if any(type(value) not in (int,float) or not low<=value<=high for value,low,high in bounds) or offset<=0:
        raise ValueError("threshold contract")
    base=logits>threshold
    high=(logits>threshold+offset).sum(axis=(1,2))
    low=(logits>threshold-offset).sum(axis=(1,2))
    stability=np.divide(high,low,out=np.zeros(count,dtype=np.float64),where=low>0)
    eligible=np.flatnonzero(base.any(axis=(1,2)) & (stability>=stability_threshold))
    order=eligible[np.lexsort((eligible,-quality[eligible]))]
    kept=[]
    for candidate in order:
        duplicate=False
        for previous in kept:
            intersection=np.count_nonzero(base[candidate] & base[previous])
            union=np.count_nonzero(base[candidate] | base[previous])
            if intersection/union>overlap_threshold:
                duplicate=True
                break
        if not duplicate:
            kept.append(int(candidate))
    return np.array(kept,dtype=np.int64)

