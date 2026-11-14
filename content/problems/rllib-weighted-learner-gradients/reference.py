import numpy as np

def _numeric(v,rank):
    if not isinstance(v,np.ndarray) or v.dtype not in (np.dtype('float32'),np.dtype('float64')) or v.ndim!=rank or v.size>10**6 or not np.isfinite(v).all() or (v.size and np.max(np.abs(v))>1e6):raise ValueError('numeric array')
    return v.astype(np.float64)

def _ints(v,rank=1):
    if not isinstance(v,np.ndarray) or v.dtype!=np.int64 or v.ndim!=rank:raise ValueError('integer array')
    return v

def aggregate_learner_gradients(mean_gradients, sample_counts):
    g=_numeric(mean_gradients,2);n=_ints(sample_counts)
    if g.shape[0]>4096 or not 1<=g.shape[1]<=256 or n.shape!=(g.shape[0],) or np.any(n<0) or np.any(n>10**6):raise ValueError('shape/counts')
    total=sum(int(x) for x in n)
    mean=np.sum(g*n.astype(np.float64)[:,None],axis=0)/total if total else np.zeros(g.shape[1],dtype=np.float64)
    return dict(mean=mean,norm=float(np.linalg.norm(mean)),total_samples=total,has_samples=bool(total))
