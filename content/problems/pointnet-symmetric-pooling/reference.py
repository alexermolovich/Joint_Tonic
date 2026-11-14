import numpy as np


def symmetric_point_pool(features, valid_mask=None):
    if not isinstance(features,np.ndarray) or (valid_mask is not None and not isinstance(valid_mask,np.ndarray)):
        raise TypeError("Expected NumPy arrays")
    if features.dtype not in (np.float32,np.float64) or features.ndim!=3 or min(features.shape)<1 or features.size>1_000_000 or not np.isfinite(features).all():
        raise ValueError("Invalid features")
    if valid_mask is None:
        return features.max(axis=1).copy()
    if valid_mask.dtype!=np.bool_ or valid_mask.shape!=features.shape[:2] or not valid_mask.any(axis=1).all():
        raise ValueError("Invalid point mask")
    return np.where(valid_mask[:,:,None],features,-np.inf).max(axis=1)
