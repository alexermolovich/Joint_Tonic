import numpy as np


def concat_local_global(local,global_features):
    for x in (local,global_features):
        if not isinstance(x,np.ndarray):raise TypeError("Expected feature arrays")
        if x.dtype not in (np.float32,np.float64) or x.size>1_000_000 or not np.isfinite(x).all():raise ValueError("Invalid features")
    if local.ndim!=3 or global_features.ndim!=2 or local.dtype!=global_features.dtype:raise ValueError("Invalid feature shape or dtype")
    b,n,d=local.shape;g=global_features.shape[1]
    if not 0<=b<=1024 or not 0<=n<=1024 or not 1<=d<=4096 or not 1<=g<=4096 or global_features.shape[0]!=b or b*n*(d+g)>1_000_000:
        raise ValueError("Invalid feature dimensions")
    return np.concatenate((local,np.broadcast_to(global_features[:,None,:],(b,n,g))),axis=2)
