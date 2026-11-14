import numpy as np

def stable_masked_softmax(logits, valid):
    if not isinstance(logits,np.ndarray) or logits.dtype!=np.float64 or logits.ndim!=2 or not 1<=logits.shape[0]<=256 or logits.shape[1]>2048 or logits.size>200000 or not np.isfinite(logits).all() or (np.abs(logits)>10000).any():raise ValueError('logits')
    if not isinstance(valid,np.ndarray) or valid.dtype!=np.bool_ or valid.shape!=logits.shape:raise ValueError('valid mask')
    if logits.shape[1]==0:return np.zeros_like(logits)
    masked=np.where(valid,logits,-np.inf);maximum=masked.max(axis=1,keepdims=True);maximum=np.where(valid.any(axis=1,keepdims=True),maximum,0.)
    weights=np.exp(masked-maximum);sums=weights.sum(axis=1,keepdims=True);out=np.zeros_like(logits)
    np.divide(weights,sums,out=out,where=sums>0)
    return out
