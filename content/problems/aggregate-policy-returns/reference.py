import numpy as np
import math

def aggregate_policy_returns(returns, tail_fraction):
    if not isinstance(returns,np.ndarray) or returns.dtype!=np.float64 or returns.ndim!=2 or not 1<=returns.shape[0]<=64 or not 1<=returns.shape[1]<=10000 or returns.size>200000 or not np.isfinite(returns).all() or (np.abs(returns)>1e6).any():raise ValueError('episode returns')
    if type(tail_fraction) not in (int,float) or not 0<tail_fraction<=1 or not math.isfinite(tail_fraction):raise ValueError('tail fraction')
    sorted_returns=np.sort(returns,axis=1);q=tail_fraction*returns.shape[1];k=int(math.floor(q));a=q-k
    if k==0:tail=sorted_returns[:,0].copy()
    else:
        mass=sorted_returns[:,:k].sum(axis=1)
        if k<returns.shape[1]:mass=mass+a*sorted_returns[:,k]
        tail=mass/q
    return dict(mean=returns.mean(axis=1),worst=sorted_returns[:,0].copy(),lower_tail=tail)
