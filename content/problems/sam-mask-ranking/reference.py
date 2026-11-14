import numpy as np


def rank_masks(masks,predicted_iou,k):
    if not isinstance(masks,np.ndarray) or not isinstance(predicted_iou,np.ndarray):raise TypeError("Expected NumPy arrays")
    if masks.dtype!=np.bool_ or masks.ndim!=3 or not 0<=masks.shape[0]<=1024 or not all(1<=v<=512 for v in masks.shape[1:]) or masks.size>1_000_000:
        raise ValueError("Invalid candidate masks")
    n=masks.shape[0]
    if predicted_iou.dtype!=np.float64 or predicted_iou.shape!=(n,) or not np.isfinite(predicted_iou).all() or np.any(np.abs(predicted_iou)>1e6):
        raise ValueError("Invalid predicted quality")
    if type(k) is not int or not 0<=k<=n:raise ValueError("Invalid selection count")
    indices=np.argsort(-predicted_iou,kind="stable")[:k].astype(np.int64,copy=True)
    return masks[indices].copy(),indices,predicted_iou[indices].copy()
