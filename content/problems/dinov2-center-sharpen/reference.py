import numpy as np


def center_sharpen(logits,center,temperature):
    for x in (logits,center):
        if not isinstance(x,np.ndarray):raise TypeError("Expected NumPy arrays")
        if x.dtype!=np.float64 or not np.isfinite(x).all() or np.any(np.abs(x)>1e6):raise ValueError("Invalid teacher scores")
    if logits.ndim!=2 or not all(1<=v<=1024 for v in logits.shape) or logits.size>1_000_000 or center.shape!=(logits.shape[1],):
        raise ValueError("Invalid teacher shapes")
    if type(temperature) not in (int,float) or not 1e-4<=temperature<=1e4:raise ValueError("Invalid temperature")
    z=(logits-center)/temperature
    exp=np.exp(z-z.max(axis=1,keepdims=True))
    return exp/exp.sum(axis=1,keepdims=True)
