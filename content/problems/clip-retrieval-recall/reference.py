import numpy as np


def retrieval_recall(scores,k):
    if not isinstance(scores,np.ndarray):raise TypeError("Expected score array")
    if scores.dtype!=np.float64 or scores.ndim!=2 or scores.shape[0]!=scores.shape[1] or not 1<=scores.shape[0]<=2048 or not np.isfinite(scores).all() or np.any(np.abs(scores)>1e6):
        raise ValueError("Invalid scores")
    n=scores.shape[0]
    if type(k) is not int or not 1<=k<=n:raise ValueError("Invalid k")
    rows=np.argsort(-scores,axis=1,kind="stable")[:,:k]
    columns=np.argsort(-scores,axis=0,kind="stable")[:k,:]
    return {"image_to_text":float((rows==np.arange(n)[:,None]).any(1).mean()),
            "text_to_image":float((columns==np.arange(n)[None,:]).any(0).mean())}
