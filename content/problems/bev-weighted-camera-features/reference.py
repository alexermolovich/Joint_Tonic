import numpy as np


def aggregate_camera_features(features,weights,valid):
    for x in (features,weights,valid):
        if not isinstance(x,np.ndarray):raise TypeError("Expected NumPy arrays")
    if features.dtype!=np.float64 or weights.dtype!=np.float64 or valid.dtype!=np.bool_ or features.ndim!=5 or not all(1<=v<=128 for v in features.shape) or features.size>1_000_000:
        raise ValueError("Invalid feature data")
    if weights.shape!=features.shape[:-1] or valid.shape!=weights.shape or not np.isfinite(features).all() or not np.isfinite(weights).all() or np.any(np.abs(features)>1e6) or np.any(weights<0) or np.any(weights>1e6):
        raise ValueError("Invalid weights or masks")
    used=np.where(valid,weights,0.)
    maximum=used.max(axis=(2,3),keepdims=True)
    observed=maximum[:,:,0,0]>0
    scaled=np.divide(used,maximum,out=np.zeros_like(used),where=maximum>0)
    total=scaled.sum(axis=(2,3),keepdims=True)
    normalized=np.divide(scaled,total,out=np.zeros_like(scaled),where=total>0)
    output=(normalized[:,:,:,:,None]*features).sum(axis=(2,3))
    return output,observed
